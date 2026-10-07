"""The rental owns one learner, bounded checkpoint evaluation and durable uploads.

The provider starts this after pinned-source bootstrap. An immutable execution claim
prevents container restart from silently restarting training. The shell guardian is
independent of this process and retains the original absolute billing deadline.
"""

import os
from pathlib import Path
import signal
import subprocess
import time
from typing import Callable

from manabot.infra.artifacts import StoredArtifact
from manabot.training.checkpoint_queue import CheckpointQueue
from manabot.training.models import TrainingRun

from .job_client import _bound_resource
from .job_store import JobStore, S3JobStore, StoredValue
from .jobs import RemoteJobRecord, RemoteJobSpec, Resource
from .snapshots import publish_snapshot


def stop_process(process: subprocess.Popen[bytes]) -> None:
    """Stop the entire learner process group before taking final evidence."""
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)


def supervise(
    spec: RemoteJobSpec, store: JobStore, root: Path, pod_id: str,
    *, command: list[str] | None = None,
    publish: Callable[..., StoredArtifact] = publish_snapshot,
) -> RemoteJobRecord:
    """Execute once. Injection points support real-process offline lifecycle tests."""
    resource_value = store.read("training.json")
    if resource_value is None:
        raise ValueError("client has not admitted this rental; reconcile submission")
    resource = Resource.model_validate_json(resource_value.data)
    _bound_resource(spec, resource)
    if resource.pod.id != pod_id:
        raise ValueError("supervisor is running on the wrong rental")
    if not store.create("runtime/execution-claim.json", spec.identity.encode()):
        raise ValueError("job already started; CUDA process recovery is unsupported")
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    now = time.time()
    record = RemoteJobRecord(spec_sha256=spec.identity, pod_id=pod_id, phase="accepted",
                             accepted_at=now, heartbeat_at=now)
    previous: StoredValue | None = None

    def persist() -> None:
        nonlocal previous, record
        record = record.model_copy(update={"heartbeat_at": time.time()})
        data = record.model_dump_json().encode()
        okay = store.create("runtime/record.json", data) if previous is None else store.replace("runtime/record.json", data, previous.etag)
        if not okay:
            raise RuntimeError("remote job record ownership changed")
        previous = store.read("runtime/record.json")
        if previous is None or previous.data != data:
            raise RuntimeError("remote job record acknowledgement unavailable")

    persist()
    learner: subprocess.Popen[bytes] | None = None
    queue: CheckpointQueue | None = None
    recipe = root.parent / "regime.json"
    recipe.write_text(spec.plan.regime.model_dump_json(indent=2))
    run_path = root / "run/run.json"
    try:
        if store.read("cancel.json") is not None:
            record = record.model_copy(update={"phase": "cancelled", "cancel_acknowledged_at": time.time()})
        elif time.time() >= spec.work_deadline:
            record = record.model_copy(update={"phase": "deadline"})
        else:
            if spec.monitoring is not None:
                queue = CheckpointQueue(root / "monitoring", spec.monitoring)
            with (root / "training.log").open("ab") as log:
                learner = subprocess.Popen(command or [
                    "uv", "run", "--no-sync", "manabot", "train", "--regime", str(recipe),
                    "--seed", str(spec.plan.seed), "--out", str(root / "run"),
                    "--checkpoint-seconds", str(spec.checkpoint_seconds),
                ], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            record = record.model_copy(update={"phase": "running"})
            persist()
            last_upload = float("-inf")
            while True:
                if store.read("cancel.json") is not None:
                    record = record.model_copy(update={"phase": "cancelled", "cancel_acknowledged_at": time.time()})
                    break
                if time.time() >= spec.work_deadline:
                    record = record.model_copy(update={"phase": "deadline"})
                    break
                sources = [run_path] if run_path.exists() else []
                if queue is not None:
                    queue.tick(sources, launch=time.time() + queue.config.attempt_seconds < spec.work_deadline)
                if sources:
                    run = TrainingRun.model_validate_json(run_path.read_bytes())
                    record = record.model_copy(update={"run_id": run.id, "updates": sum(s.updates for s in run.stages)})
                if time.time() - last_upload >= spec.publish_seconds:
                    try:
                        manifest = publish(spec, root, record.generation + 1, complete=False)
                        record = record.model_copy(update={"generation": record.generation + 1, "manifest": manifest})
                    except Exception as error:
                        record = record.model_copy(update={"error": f"snapshot upload failed ({type(error).__name__})"})
                    last_upload = time.time()
                if queue is not None:
                    record = record.model_copy(update={"evaluations_completed": sum(a.status == "completed" for a in queue.attempts), "evaluator_seconds": queue.charged_seconds})
                persist()
                if learner.poll() is not None:
                    if learner.returncode != 0:
                        record = record.model_copy(update={"phase": "failed", "error": f"learner exited {learner.returncode}"})
                        break
                    if queue is None or (queue.process is None and (queue.pending == 0 or queue.config.seconds - queue.charged_seconds < queue.config.attempt_seconds)):
                        if not run_path.exists() or TrainingRun.model_validate_json(run_path.read_bytes()).status != "completed":
                            record = record.model_copy(update={"phase": "failed", "error": "learner exited without completed TrainingRun"})
                        elif queue is not None and any(a.status != "completed" for a in queue.attempts):
                            record = record.model_copy(update={"phase": "failed", "error": "milestone evaluation incomplete"})
                        else:
                            record = record.model_copy(update={"phase": "completed"})
                        break
                time.sleep(1)
    except Exception as error:
        record = record.model_copy(update={"phase": "failed", "error": f"supervisor failed ({type(error).__name__})"})
    finally:
        if learner is not None:
            stop_process(learner)
            (root / "training-exit.txt").write_text(str(learner.returncode))
        if queue is not None:
            queue.close()
        terminal = record.phase
        record = record.model_copy(update={"phase": "finalizing"})
        try:
            persist()
            manifest = publish(spec, root, record.generation + 1, complete=True)
            record = record.model_copy(update={"generation": record.generation + 1, "manifest": manifest, "artifacts_complete": True})
        except Exception as error:
            record = record.model_copy(update={"error": f"final upload incomplete ({type(error).__name__})", "artifacts_complete": False})
        record = record.model_copy(update={"phase": terminal})
        try:
            persist()
        except Exception:
            # Last durable generation remains explicit. Guardian still deletes.
            pass
    return record


def main() -> None:
    store = S3JobStore(os.environ["MANABOT_JOB_PREFIX"])
    raw = store.read("spec.json")
    if raw is None:
        raise ValueError("remote job intent missing")
    spec = RemoteJobSpec.model_validate_json(raw.data)
    pod_id = os.environ["RUNPOD_POD_ID"]
    # A lost create response can delay admission; a fresh submitter can reconcile
    # it without starting another rental. Never train before price admission.
    while store.read("training.json") is None and time.time() < spec.work_deadline:
        time.sleep(2)
    try:
        supervise(spec, store, Path("/workspace/evidence"), pod_id)
    finally:
        # No account key is forwarded. The same pod-scoped identity as guardian.
        subprocess.run(["runpodctl", "remove", "pod", pod_id], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=20, check=False)


if __name__ == "__main__":
    main()
