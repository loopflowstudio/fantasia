"""Serial six-run cohort driver; remote jobs own learning and billing after submit.

Restart observes the same IDs. Failed or ambiguous attempts stop new admission;
there are no replacement jobs or CUDA process resumes. Report failures do not
cancel learning. This retained operational script is hashed before the first rent.
"""

import fcntl
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path.cwd()))
from experiments.runners.cuda_capacity import FourHourPreparation
from manabot.arena.models import canonical_sha256, file_sha256
from manabot.remote.deploy import current_source
from manabot.remote.job_client import fetch_job, job_status, load_job
from manabot.remote.provider import RunPod
from manabot.training.execution import atomic_json
from manabot.training.models import TrainingRun

ROOT = Path(__file__).resolve().parent
REPO = Path.cwd()
PRIOR = 0.5359766177137693 + 3.0  # Retain the whole shared proof reservation.


def emit(event: str, **values: object) -> None:
    print(json.dumps({"event": event, "at": time.time(), **values}), flush=True)


def project(generation: Path, job: Path) -> None:
    """Regenerate a JSON-only view; the returned generation stays immutable."""
    view = job / "view"
    if view.exists():
        shutil.rmtree(view)
    view.mkdir()
    for pattern in ("run.json", "monitor.json", "attempt.json"):
        for source in generation.rglob(pattern):
            target = view / source.relative_to(generation)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    budget_path = ROOT / "report-cost.json"
    spent = (
        json.loads(budget_path.read_text())["seconds"] if budget_path.exists() else 0.0
    )
    if spent >= 3600:
        emit("report_budget_exhausted", job=job.name)
        return
    began = time.monotonic()
    report = job / "report"
    report.mkdir(exist_ok=True)
    # Bounded child owns optional W&B/network work; it cannot hold the cohort.
    with (job / "report.log").open("ab") as log:
        try:
            subprocess.run(
                ["uv", "run", "--no-sync", "python", str(ROOT / "report.py"), str(job)],
                stdout=log,
                stderr=log,
                timeout=min(120, 3600 - spent),
                check=True,
            )
        except (subprocess.SubprocessError, OSError) as error:
            emit("report_failure", job=job.name, error=type(error).__name__)
        finally:
            atomic_json(
                budget_path, {"seconds": spent + time.monotonic() - began, "cap": 3600}
            )


def main() -> None:
    plan = FourHourPreparation.model_validate_json(
        (ROOT / "preparation.json").read_text()
    )
    assert plan.monitoring.require_initial_admission
    assert current_source(REPO) == plan.source
    pr = json.loads(
        subprocess.check_output(
            ["gh", "pr", "view", "255", "--json", "state,headRefOid"],
            text=True,
        )
    )
    assert pr["state"] == "MERGED" and pr["headRefOid"] == plan.source.commit, pr
    provider = RunPod()
    charged = PRIOR
    admission = ROOT / "admission.json"
    if not admission.exists():
        assert not provider.list(), "Unexpected existing rental; reconcile first"
        atomic_json(
            admission,
            {
                "at": time.time(),
                "source": plan.source.model_dump(mode="json"),
                "preparation_sha256": file_sha256(ROOT / "preparation.json"),
                "protocol_sha256": canonical_sha256(
                    plan.protocol.model_dump(mode="json")
                ),
                "controller_sha256": file_sha256(Path(__file__)),
                "report_sha256": file_sha256(ROOT / "report.py"),
                "credential_admission": file_sha256(
                    REPO / ".runs/etu103-issuer-admission-20261007.json"
                ),
                "projected_dollars": plan.projected_dollars,
                "cap_dollars": 30,
                "initial_cohort_gates_learning": True,
                "training_hours": 24,
                "local_evaluator": False,
                "retries": False,
            },
        )
    frozen = json.loads(admission.read_text())
    assert frozen["controller_sha256"] == file_sha256(Path(__file__))
    assert frozen["report_sha256"] == file_sha256(ROOT / "report.py")
    assert frozen["preparation_sha256"] == file_sha256(ROOT / "preparation.json")
    for index, deployment in enumerate(plan.deployments):
        job_id = f"etu103-four-hour-{deployment.seed}-{index}"
        job = ROOT / job_id
        job.mkdir(exist_ok=True)
        marker = job / "submit-intent.json"
        if not marker.exists():
            assert current_source(REPO) == plan.source, "Frozen checkout changed"
            quote = provider.prices()["NVIDIA L4"]
            assert 0 < quote <= deployment.mix.hourly_ceiling
            assert not provider.list(), "Prior resource deletion is unconfirmed"
            remaining = sum(d.projected_dollars for d in plan.deployments[index:])
            assert charged + remaining + 0.6 + 1 <= 30
            atomic_json(
                marker,
                {
                    "at": time.time(),
                    "index": index,
                    "job_id": job_id,
                    "quote": quote,
                    "charged_with_proof_reserve": charged,
                },
            )
            emit(
                "submit",
                job=job_id,
                seed=deployment.seed,
                capacity=deployment.regime.id,
            )
            with (job / "submit.log").open("ab") as log:
                try:
                    result = subprocess.run(
                        [
                            "uv",
                            "run",
                            "--no-sync",
                            "manabot",
                            "deploy",
                            "--plan",
                            str(ROOT / f"deployment-{index}.json"),
                            "--job-id",
                            job_id,
                            "--monitoring",
                            str(ROOT / "monitoring.json"),
                            "--checkpoint-seconds",
                            "3600",
                        ],
                        stdout=log,
                        stderr=log,
                        timeout=1000,
                    )
                    emit("submit_returned", job=job_id, code=result.returncode)
                except subprocess.TimeoutExpired:
                    emit("acceptance_unknown", job=job_id)
        spec = load_job(job_id)
        fetched = 0
        last_fetch = 0.0
        evaluations = -1
        while True:
            status = job_status(spec, provider=provider)
            atomic_json(job / "status.json", status.model_dump(mode="json"))
            record = status.record
            emit(
                "status",
                job=job_id,
                phase=record.phase if record else "setup",
                updates=record.updates if record else 0,
                evaluations=record.evaluations_completed if record else 0,
                generation=record.generation if record else 0,
                provider=status.provider_state,
            )
            stopped = record is not None and record.phase in {
                "completed",
                "failed",
                "cancelled",
                "deadline",
            }
            if (
                record
                and record.manifest
                and record.generation != fetched
                and (
                    stopped
                    or record.evaluations_completed != evaluations
                    or time.monotonic() - last_fetch >= 900
                )
            ):
                try:
                    generation = fetch_job(spec, job / "returned")
                    fetched = record.generation
                    evaluations = record.evaluations_completed
                    last_fetch = time.monotonic()
                    atomic_json(job / "latest.json", {"generation": str(generation)})
                    project(generation, job)
                    emit("verified_generation", job=job_id, path=str(generation))
                except Exception as error:
                    emit("fetch_failure", job=job_id, error=type(error).__name__)
                    if stopped:
                        raise
            if status.cleanup is not None:
                charged += status.cleanup.estimated_dollars
                atomic_json(
                    ROOT / "costs.json",
                    {
                        "charged_with_full_proof_reserve": charged,
                        "actual_shared_prior_dollars": 0.6518216411512489,
                        "through_job": job_id,
                        "cleanup": status.cleanup.model_dump(mode="json"),
                    },
                )
                if (
                    not record
                    or record.phase != "completed"
                    or not record.artifacts_complete
                ):
                    raise RuntimeError(
                        f"{job_id}: stopped attempt; no replacement or later admission"
                    )
                latest = json.loads((job / "latest.json").read_text())["generation"]
                run = TrainingRun.model_validate_json(
                    (Path(latest) / "run/run.json").read_text()
                )
                active = sum(
                    s.collection_seconds + s.learning_seconds for s in run.stages
                )
                assert run.status == "completed" and active >= 14400
                assert record.evaluations_completed == 6
                emit("run_complete", job=job_id, active_seconds=active, charged=charged)
                break
            if time.time() > spec.deadline + 180:
                raise RuntimeError(
                    f"{job_id}: deletion unconfirmed; no later admission"
                )
            time.sleep(30)
    emit("cohort_complete", charged_with_full_proof_reserve=charged)


if __name__ == "__main__":
    with (ROOT / "controller.lock").open("a+b") as lease:
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        main()
