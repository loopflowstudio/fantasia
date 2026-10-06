"""ETU-118 declaration and bounded positive-control execution.

Experiment resolves recipes; execute_regime/VerifyStore own actual learning.
The shared asynchronous monitor is Allies/Lessons-only, so injected-root scoring
is explicit here. Every selected action is re-executed from its original root.
"""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import signal
import time

import numpy as np
from pydantic import JsonValue
import torch

from experiments.runners.run_value_models import smoke_baseline
from manabot.arena.models import file_sha256
from manabot.env import Match
from manabot.env.target_practice import resolve_target, target_root
from manabot.sim.flat_mc import AgentMatchupPlayer, load_checkpoint_agent
from manabot.training.execution import atomic_json, execute_regime
from manabot.training.experiments import Baseline, Experiment
from manabot.training.models import TrainingRegime, TrainSelfPlay
from manabot.verify.store import VerifyStore

SEEDS = (11801, 11802, 11803)
DEALS = tuple(range(1_911_180_000, 1_911_180_064))


def declaration(*, frozen: bool = False) -> Experiment:
    base = smoke_baseline()
    base.id = "lethal-target-frozen" if frozen else "lethal-target-learning"
    base.agent.value_aggregation = "masked_mean"
    base.wall_seconds = 780
    stage = deepcopy(base.stages[0])
    assert isinstance(stage, TrainSelfPlay)
    stage.root = "lethal-target-v1"
    stage.trainable = "none" if frozen else "policy_value"
    stage.updates = 100
    stage.transitions = 16
    stage.execution.wall_seconds = 760
    base.stages = [stage]
    base = TrainingRegime.model_validate(base.model_dump())
    return Experiment(name=base.id, baseline=Baseline.capture(base.id, base))


def evaluate(checkpoint: Path, regime: TrainingRegime) -> list[dict[str, JsonValue]]:
    agent, space = load_checkpoint_agent(str(checkpoint))
    player = AgentMatchupPlayer(agent)
    rows: list[dict[str, JsonValue]] = []
    for deal in DEALS:
        for seat in (0, 1):
            env = target_root(Match(regime.match), space, deal, seat)
            before = env._engine.state_digest()
            obs = space.encode(env.last_raw_obs)
            with torch.no_grad():
                logits, _ = agent(
                    {k: torch.from_numpy(v).unsqueeze(0) for k, v in obs.items()}
                )
                probabilities = logits.softmax(-1)[0]
            if not torch.isfinite(probabilities).all() or not torch.isclose(
                probabilities.sum(), torch.tensor(1.0)
            ):
                raise ValueError("invalid legal distribution")
            if (probabilities[2:] != 0).any():
                raise ValueError("policy assigned probability outside legal support")
            torch.manual_seed(deal + seat)
            action = player.act(env, obs)
            winner = resolve_target(env, action)
            after = env._engine.state_digest()
            replay = target_root(Match(regime.match), space, deal, seat)
            if (
                replay._engine.state_digest() != before
                or resolve_target(replay, action) != winner
                or replay._engine.state_digest() != after
            ):
                raise ValueError("target-root exact replay diverged")
            rows.append(
                {
                    "deal": deal,
                    "seat": seat,
                    "action": action,
                    "winner": winner,
                    "win": winner == seat,
                    "probabilities": probabilities[:2].tolist(),
                    "root": before,
                    "terminal": after,
                    "replay": True,
                }
            )
    return rows


def _expire(signum: int, frame: object) -> None:
    raise TimeoutError("ETU-118 declared attempt allowance exhausted")


def run(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    started = time.monotonic()
    result: dict[str, JsonValue] = {"status": "running", "attempts": [], "seconds": 0.0}
    attempts: list[dict[str, JsonValue]] = []
    result["attempts"] = attempts
    signal.signal(signal.SIGALRM, _expire)
    try:
        with VerifyStore(out / "verify.sqlite") as store:
            for seed in SEEDS:
                initial_state: dict[str, torch.Tensor] | None = None
                initial_rows: list[dict[str, JsonValue]] | None = None
                for frozen in (False, True):
                    remaining = 3600 - (time.monotonic() - started)
                    if remaining <= 0:
                        raise TimeoutError("ETU-118 aggregate allowance exhausted")
                    signal.setitimer(signal.ITIMER_REAL, min(900, remaining))
                    tick = time.monotonic()
                    regime = declaration(frozen=frozen).resolve().cases[0].regime
                    attempt: dict[str, JsonValue] = {
                        "seed": seed,
                        "frozen": frozen,
                        "status": "running",
                    }
                    attempts.append(attempt)
                    atomic_json(out / "result.json", result)
                    try:
                        training = execute_regime(
                            regime,
                            seed,
                            out / f"{seed}-{'frozen' if frozen else 'learning'}",
                            store,
                        )
                        attempt["run_id"] = training.id
                        if training.status != "completed":
                            raise RuntimeError(training.error)
                        artifacts = training.stages[0].artifacts
                        initial = Path(artifacts["initial_raw"]["path"])
                        final = Path(artifacts["raw"]["path"])
                        init_agent, _ = load_checkpoint_agent(str(initial))
                        final_agent, _ = load_checkpoint_agent(str(final))
                        if initial_state is None:
                            initial_state = deepcopy(init_agent.state_dict())
                            initial_rows = evaluate(initial, regime)
                            attempt["initial"] = initial_rows
                        if any(
                            not torch.equal(value, initial_state[key])
                            for key, value in init_agent.state_dict().items()
                        ):
                            raise ValueError("paired initialization changed")
                        unchanged = all(
                            torch.equal(value, initial_state[key])
                            for key, value in final_agent.state_dict().items()
                        )
                        if unchanged != frozen:
                            raise ValueError(
                                "unexpected frozen/learned weight identity"
                            )
                        scored = evaluate(final, regime)
                        if frozen and scored != initial_rows:
                            raise ValueError(
                                "frozen control differs from initialization"
                            )
                        attempt.update(
                            status="completed",
                            checkpoint_sha256=file_sha256(final),
                            initial_sha256=file_sha256(initial),
                            rows=scored,
                        )
                    except BaseException as error:
                        attempt.update(
                            status="failed", error=f"{type(error).__name__}: {error}"
                        )
                        raise
                    finally:
                        signal.setitimer(signal.ITIMER_REAL, 0)
                        attempt["seconds"] = time.monotonic() - tick
                        result["seconds"] = time.monotonic() - started
                        atomic_json(out / "result.json", result)
        result["status"] = "completed"
    except BaseException as error:
        result.update(status="failed", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        result["seconds"] = time.monotonic() - started
        atomic_json(out / "result.json", result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--run", type=Path)
    args = parser.parse_args()
    if args.plan:
        atomic_json(
            args.plan,
            {
                "seeds": list(SEEDS),
                "held_out_deals": list(DEALS),
                "attempt_seconds": 900,
                "aggregate_seconds": 3600,
                "minimum_win_rate_each_seed": 0.85,
                "minimum_gain_each_seed": 0.25,
                "recipes": [
                    declaration(frozen=f).resolve().receipt() for f in (False, True)
                ],
            },
        )
    elif args.run:
        run(args.run)
    else:
        parser.error("select --plan or --run")


if __name__ == "__main__":
    main()
