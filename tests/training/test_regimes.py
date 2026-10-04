"""Training contracts, credit boundaries, and experiment controls."""

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from manabot.training.execution import execute_regime, validate_regime
from manabot.training.models import StageRecord, TrainingRegime, TrainingRun
from manabot.training.objectives import reference_distribution, selected_rows
from manabot.verify.store import VerifyStore

ROOT = Path(__file__).resolve().parents[2]


def recipe(name="direct-self-play"):
    return TrainingRegime.model_validate_json(
        (ROOT / "experiments/regimes" / f"{name}.json").read_text()
    )


def test_all_recipes_validate_and_reject_future_references():
    for path in (ROOT / "experiments/regimes").glob("*.json"):
        validate_regime(TrainingRegime.model_validate_json(path.read_text()))
    raw = recipe().model_dump()
    raw["stages"][0]["initial"] = "policy-1"
    with pytest.raises(ValueError, match="earlier"):
        TrainingRegime.model_validate(raw)
    raw = recipe().model_dump()
    raw["stages"][0]["operation"] = "belief"
    with pytest.raises(ValueError):
        TrainingRegime.model_validate(raw)
    raw = recipe()
    raw.world = "invalid"
    with pytest.raises(ValueError, match="world"):
        validate_regime(raw)


def test_reference_has_full_support_and_is_permutation_invariant():
    obs = {
        "actions_valid": torch.tensor([[1.0, 1.0, 1.0, 0.0]]),
        "actions": torch.tensor(
            [[[1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]]
        ),
    }
    probs = reference_distribution(obs, "action_type_uniform")
    torch.testing.assert_close(probs, torch.tensor([[0.25, 0.25, 0.5, 0.0]]))
    permutation = torch.tensor([2, 0, 3, 1])
    moved = reference_distribution(
        {k: v[:, permutation] for k, v in obs.items()}, "action_type_uniform"
    )
    torch.testing.assert_close(moved, probs[:, permutation])
    assert selected_rows(torch.zeros(4), 0.25, 0.01).numel() == 0


def test_store_exports_committed_run_and_preserves_old_schema(tmp_path):
    with VerifyStore(tmp_path / "store.sqlite") as store:
        run = TrainingRun(
            id="fixture",
            regime=recipe(),
            regime_digest="test",
            seed=1,
            seed_streams={},
            identities={},
            stages=[StageRecord(id="policy-0")],
        )
        store.save_training_run(run)
        run.status = "failed"
        assert store.training_run(run.id).status == "pending"
        store.save_training_run(run)
        assert store.training_run(run.id).status == "failed"
        assert store.con.execute("SELECT count(*) FROM runs").fetchone()[0] == 0


def test_deadline_retains_failed_attempt(tmp_path):
    value = recipe()
    value.wall_seconds = 1e-9
    with VerifyStore(tmp_path / "store.sqlite") as store:
        with pytest.raises(TimeoutError):
            execute_regime(value, 197, tmp_path / "run", store)
        result = json.loads((tmp_path / "run/run.json").read_text())
        assert result["status"] == "interrupted"
        assert result["stages"][0]["status"] == "interrupted"
        assert result["seconds"] > 0


def test_named_treatments_execute_real_optimizer_batches():
    from types import SimpleNamespace

    from manabot.env import ObservationSpace
    from manabot.infra.hypers import AgentHypers
    from manabot.model.agent import Agent
    from manabot.sim.net_opponent import RolloutBatch
    from manabot.training.objectives import update_iteration

    torch.set_num_threads(1)
    space = ObservationSpace()
    agent = Agent(space, AgentHypers(hidden_dim=8, num_attention_heads=2))
    obs = space.encoder.allocate(2)
    obs["actions_valid"][:, :2] = 1
    obs["agent_player_valid"][:] = 1
    obs["opponent_player_valid"][:] = 1
    obs["actions"][:, 0, 0] = 1
    obs["actions"][:, 1, 1] = 1
    with torch.no_grad():
        logits, values = agent({k: torch.as_tensor(v) for k, v in obs.items()})
        probs = logits.softmax(-1).numpy()
    batch = RolloutBatch(
        obs={k: v[:, None] for k, v in obs.items()},
        actions=np.zeros((2, 1), dtype=np.int64),
        logprobs=np.log(probs[:, 0, None]),
        rewards=np.array([[0.0], [1.0]], dtype=np.float32),
        dones=np.array([[False], [True]]),
        values=values.numpy().reshape(2, 1),
        next_obs={k: v[:1] for k, v in obs.items()},
        next_done=np.ones(1, dtype=bool),
        probabilities=probs[:, None],
    )
    from manabot.sim.net_opponent import NetOpponentTrainer

    trainer = SimpleNamespace(
        agent=agent,
        experiment=SimpleNamespace(device="cpu"),
        optimizer=torch.optim.Adam(agent.parameters()),
        _obs_to_tensors=NetOpponentTrainer._obs_to_tensors,
    )
    for path in (ROOT / "experiments/regimes").glob("*.json"):
        stage = TrainingRegime.model_validate_json(path.read_text()).stages[0]
        if stage.operation != "train_self_play":
            continue
        result = update_iteration(
            trainer, batch, stage.learning, 0.5, np.random.default_rng(7)
        )
        assert result["optimizer_exposures"] > 0
        assert np.isfinite(result["loss"])
