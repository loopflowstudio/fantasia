"""Allocation admission over synthetic receipts; no training or strength evidence."""

from pathlib import Path
import shutil

import pytest

from experiments.runners import sustained_baseline as baseline
from manabot.arena.models import canonical_sha256, file_sha256
from manabot.training.checkpoint_queue import MonitoringBudget
from manabot.training.execution import atomic_json
from manabot.training.experiment_execution import (
    ExperimentRun,
    ExperimentSchedule,
    RegimeAttempt,
)
from manabot.training.models import StageRecord, TrainingRun
from manabot.verify.store import VerifyStore


def calibration_fixture(root: Path) -> ExperimentRun:
    root.mkdir()
    schedule = ExperimentSchedule(
        seeds=baseline.CALIBRATION_SEEDS,
        hardware="etu118-laptop",
        wall_seconds=1200,
        process_seconds=1200,
        active_runtime=True,
        monitoring=MonitoringBudget(
            seconds=450, attempt_seconds=75, active_runtime=True
        ),
    )
    regime = (
        baseline.declaration(
            baseline.recipe((baseline.CALIBRATION_UPDATES,), 240), schedule
        )
        .resolve()
        .cases[0]
        .regime
    )
    record = ExperimentRun(
        id="synthetic-calibration",
        intent={"schedule": schedule.model_dump(mode="json")},
        intent_sha256="a" * 64,
        hardware=baseline.hardware().resources[0],
        runtime=baseline._runtime(),
        status="completed",
        elapsed_seconds=384,
        process_seconds=384,
        notebook=str(root / "notebook.ipynb"),
    )
    with VerifyStore(root / "experiment.sqlite") as store:
        for index, seed in enumerate(baseline.CALIBRATION_SEEDS):
            out = root / f"seed-{seed}"
            out.mkdir()
            state = out / "fixture.pt.gz"
            state.write_bytes(b"synthetic storage fixture")
            run = TrainingRun(
                id=f"fixture-{seed}",
                regime=regime,
                regime_digest=canonical_sha256(regime.model_dump(mode="json")),
                seed=seed,
                seed_streams={},
                identities={},
                status="completed",
                seconds=2 * baseline.CALIBRATION_UPDATES,
                recovery_artifact={
                    "path": str(state),
                    "sha256": file_sha256(state),
                    "bytes": state.stat().st_size,
                },
                stages=[
                    StageRecord(
                        id="update-64",
                        status="completed",
                        optimizer_exposures=64,
                        diagnostics=[
                            {"coordinates": {"training_seconds": 2 * update}}
                            for update in range(1, baseline.CALIBRATION_UPDATES + 1)
                        ],
                    )
                ],
            )
            store.save_training_run(run)
            atomic_json(out / "run.json", run.model_dump(mode="json"))
            record.attempts.append(
                RegimeAttempt(
                    ordinal=index,
                    case="current-baseline",
                    seed=seed,
                    path=str(out),
                    allowance_seconds=240,
                    process_seconds=2 * baseline.CALIBRATION_UPDATES,
                    run_id=run.id,
                    status="completed",
                )
            )
        store.save_experiment_run(record)
    atomic_json(root / "experiment.json", record.model_dump(mode="json"))
    return record


def test_horizon_uses_retained_time_and_rejects_changed_authority(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "calibration"
    record = calibration_fixture(root)
    disk = shutil.disk_usage(tmp_path)._replace(free=10**12)
    monkeypatch.setattr(baseline.shutil, "disk_usage", lambda path: disk)
    plan = baseline.freeze(root, tmp_path / "plan.json", 3000)
    assert plan.milestones[-1] == 25600
    assert (
        plan.preparation_seconds
        + plan.schedule.process_seconds
        + plan.final_reserve_seconds
        == 604800
    )
    assert plan.regime.agent.value_aggregation == "masked_mean"
    assert all(
        stage.learning == plan.regime.stages[0].learning for stage in plan.regime.stages
    )
    plan.admit()
    with pytest.raises(FileExistsError):
        baseline.freeze(root, tmp_path / "plan.json", 3000)
    altered = plan.model_dump(mode="json")
    altered["schedule"]["process_seconds"] += 1
    with pytest.raises(ValueError, match="allocation"):
        baseline.SustainedPlan.model_validate(altered)
    record.elapsed_seconds = 1
    atomic_json(root / "experiment.json", record.model_dump(mode="json"))
    with pytest.raises(ValueError, match="VerifyStore"):
        baseline.freeze(root, tmp_path / "changed.json", 3000)


def test_insufficient_disk_does_not_shorten_into_a_toy_horizon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "calibration"
    calibration_fixture(root)
    disk = shutil.disk_usage(tmp_path)._replace(free=baseline.DISK_RESERVE)
    monkeypatch.setattr(baseline.shutil, "disk_usage", lambda path: disk)
    with pytest.raises(ValueError, match="no serious horizon"):
        baseline.freeze(root, tmp_path / "plan.json", 3000)
    assert not (tmp_path / "plan.json").exists()
