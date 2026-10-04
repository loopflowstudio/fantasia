"""Run bounded regime studies or regenerate their saved analysis offline."""

import argparse
from pathlib import Path
import signal
import time

import torch

from manabot.arena.match import SELECTED_SUITE, play_cell
from manabot.arena.models import ArenaKey, PlayerRegistration, canonical_sha256
from manabot.sim.flat_mc import load_checkpoint_agent
from manabot.training.execution import atomic_json, execute_regime
from manabot.training.models import CollectSearch, TrainingRegime, TrainSelfPlay
from manabot.verify.store import VerifyStore
from experiments.runners.training_protocol import EvaluationProtocol

ROOT = Path(__file__).resolve().parents[2]
STUDIES = {
    "learning-speed": ["search-distillation", "direct-self-play"],
    "ataraxos-ablations": [
        "rl-control",
        "separate-estimators",
        "advantage-filtering",
        "coordinated-decay",
        "combined",
    ],
}


def registration(run, stage, variant="raw"):
    artifact = stage.artifacts[variant]
    agent, _ = load_checkpoint_agent(artifact["path"])
    identity = run.identities
    return PlayerRegistration(
        player_id=f"{run.regime.id}-{stage.id}-{variant}",
        display_name=run.regime.id,
        role="challenger",
        runner_kind="checkpoint",
        player_spec={
            "kind": "checkpoint",
            "deterministic": False,
            "device": "cpu",
            "batch_size": 1,
        },
        compute_class_id="policy-cpu-one-thread-one-pass",
        information_boundary="acting-viewer",
        world=run.regime.world,
        content_suite=SELECTED_SUITE,
        observation_abi_sha256=identity["observation_abi_sha256"],
        action_abi_sha256=identity["action_abi_sha256"],
        matchup_sha256=identity["matchup_sha256"],
        checkpoint_sha256=artifact["sha256"],
        checkpoint_bytes=artifact["bytes"],
        parameter_count=sum(p.numel() for p in agent.parameters()),
        training_seed=run.seed,
        artifact_id=f"{run.id}/{stage.id}/{variant}",
        player_seed_derivation_id="arena-pair-deal-player-v1",
    )


def run_study(study, out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    protocol = EvaluationProtocol(study=study)
    atomic_json(out / "protocol.json", protocol.model_dump(mode="json"))
    result = {
        "study": study,
        "profile": "smoke",
        "status": "running",
        "runs": [],
        "measurements": [],
        "comparisons": [],
        "seed": protocol.training_seed,
        "protocol_sha256": canonical_sha256(protocol.model_dump(mode="json")),
        "limits": "900 seconds total; one training seed; one four-leg deal block per comparison; no strength claim",
    }

    def save():
        result["seconds"] = time.perf_counter() - start
        atomic_json(out / "study.json", result)

    def deadline(*_):
        raise TimeoutError("study exceeded its 15-minute process deadline")

    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, protocol.process_seconds)
    save()
    try:
        runs = []
        with VerifyStore(out / "training.sqlite") as store:
            for name in STUDIES[study]:
                recipe = TrainingRegime.model_validate_json(
                    (ROOT / "experiments/regimes" / f"{name}.json").read_text()
                )
                recipe.agent.hidden_dim = 16
                recipe.agent.num_attention_heads = 2
                for stage in recipe.stages:
                    if isinstance(stage, CollectSearch):
                        stage.simulations = 4
                        stage.worlds = 1
                    elif isinstance(stage, TrainSelfPlay):
                        stage.transitions = 64
                        stage.updates = 2
                        stage.learning.epochs = 1
                    else:
                        stage.epochs = 1
                run = execute_regime(recipe, protocol.training_seed, out / name, store)
                runs.append(run)
                result["runs"].append(
                    {"id": run.id, "path": str(out / name / "run.json")}
                )
                save()
        key = ArenaKey(
            world=runs[0].regime.world,
            content_suite=SELECTED_SUITE,
            viewer_boundary="acting-viewer",
            arena_version="training-regime-smoke-v1",
            rating_model_version="unrated",
            rating_prior_sha256=canonical_sha256({}),
            anchor_cohort_sha256=canonical_sha256([]),
            evaluation_compute_envelope_id="policy-cpu-one-thread-one-pass",
        )
        checkpoints = {
            run.id: [s for s in run.stages if "raw" in s.artifacts] for run in runs
        }
        for cutoff in range(protocol.checkpoint_count):
            baseline = runs[0]
            for candidate in runs[1:]:
                a_stage, b_stage = (
                    checkpoints[baseline.id][cutoff],
                    checkpoints[candidate.id][cutoff],
                )
                a, b = registration(baseline, a_stage), registration(candidate, b_stage)
                arena_out = out / f"arena-{cutoff}-{candidate.regime.id}"
                arena_out.mkdir()
                tick = time.perf_counter()
                rows, trace, replay = play_cell(
                    key=key,
                    player_a=a,
                    player_b=b,
                    deal_seeds=protocol.paired_deals,
                    game_seconds=protocol.game_seconds, max_commands=protocol.max_commands,
                    out_dir=arena_out,
                    checkpoint_paths={
                        a.player_id: a_stage.artifacts["raw"]["path"],
                        b.player_id: b_stage.artifacts["raw"]["path"],
                    },
                )
                atomic_json(arena_out / "rows.json", rows)
                atomic_json(
                    arena_out / "registrations.json", [a.model_dump(), b.model_dump()]
                )
                result["comparisons"].append(
                    {
                        "cutoff": cutoff,
                        "a": baseline.regime.id,
                        "b": candidate.regime.id,
                        "rows": rows,
                        "trace": trace,
                        "replay": replay,
                        "evaluation_seconds": time.perf_counter() - tick,
                    }
                )
                for run, stage, is_a in (
                    (baseline, a_stage, True),
                    (candidate, b_stage, False),
                ):
                    cumulative = []
                    for item in run.stages:
                        cumulative.append(item)
                        if item.id == stage.id:
                            break
                    valid = all(
                        row["failure"] is None
                        and row["terminated"]
                        and row["replay_passed"]
                        for row in rows
                    )
                    score = (
                        sum(
                            row["score_a"] if is_a else 1 - row["score_a"]
                            for row in rows
                        )
                        / len(rows)
                        if valid
                        else None
                    )
                    result["measurements"].append(
                        {
                            "regime": run.regime.id,
                            "seed": run.seed,
                            "checkpoint": stage.artifacts["raw"],
                            "cutoff": cutoff,
                            "opponent": candidate.regime.id
                            if is_a
                            else baseline.regime.id,
                            "training_seconds": run.setup_seconds + sum(s.seconds for s in cumulative),
                            "decisions": sum(
                                s.environment_decisions for s in cumulative
                            ),
                            "games": sum(s.games for s in cumulative),
                            "score": score,
                            "complete": valid,
                        }
                    )
                save()
                if not replay["passed"] or any(
                    row["failure"] is not None or not row["terminated"] for row in rows
                ):
                    raise RuntimeError(
                        "incomplete arena cohort; retained attempts cannot establish a score"
                    )
        identity = runs[0].identities
        anchor = PlayerRegistration(
            player_id="random-smoke-anchor",
            display_name="Uniform random",
            role="anchor",
            runner_kind="code",
            player_spec={"kind": "random"},
            source_sha256=identity["engine_source_sha256"],
            compute_class_id="random-cpu",
            information_boundary="acting-viewer",
            world=runs[0].regime.world,
            content_suite=SELECTED_SUITE,
            observation_abi_sha256=identity["observation_abi_sha256"],
            action_abi_sha256=identity["action_abi_sha256"],
            matchup_sha256=identity["matchup_sha256"],
            player_seed_derivation_id="arena-pair-deal-player-v1",
        )
        for run in runs:
            cumulative = []
            cutoff = 0
            for stage in run.stages:
                cumulative.append(stage)
                if "raw" not in stage.artifacts:
                    continue
                candidate = registration(run, stage)
                arena_out = out / f"anchor-{run.regime.id}-{cutoff}"
                arena_out.mkdir()
                tick = time.perf_counter()
                rows, trace, replay = play_cell(
                    key=key,
                    player_a=candidate,
                    player_b=anchor,
                    deal_seeds=protocol.anchor_deals,
                    game_seconds=protocol.game_seconds, max_commands=protocol.max_commands,
                    out_dir=arena_out,
                    checkpoint_paths={
                        candidate.player_id: stage.artifacts["raw"]["path"]
                    },
                    comparison_seed_aliases={candidate.player_id: "candidate"},
                )
                atomic_json(arena_out / "rows.json", rows)
                atomic_json(
                    arena_out / "registrations.json",
                    [candidate.model_dump(), anchor.model_dump()],
                )
                valid = all(
                    r["failure"] is None and r["terminated"] and r["replay_passed"]
                    for r in rows
                )
                result["comparisons"].append(
                    dict(
                        cutoff=cutoff,
                        a=run.regime.id,
                        b=anchor.player_id,
                        rows=rows,
                        trace=trace,
                        replay=replay,
                        evaluation_seconds=time.perf_counter() - tick,
                    )
                )
                result["measurements"].append(
                    dict(
                        regime=run.regime.id,
                        seed=run.seed,
                        checkpoint=stage.artifacts["raw"],
                        cutoff=cutoff,
                        opponent=anchor.player_id,
                        training_seconds=run.setup_seconds + sum(s.seconds for s in cumulative),
                        decisions=sum(s.environment_decisions for s in cumulative),
                        games=sum(s.games for s in cumulative),
                        score=sum(r["score_a"] for r in rows) / len(rows)
                        if valid
                        else None,
                        complete=valid,
                    )
                )
                save()
                if not valid:
                    raise RuntimeError("incomplete anchor cohort")
                cutoff += 1
        result["status"] = "completed"
        save()
    except BaseException as error:
        result["status"] = "failed"
        result["error"] = f"{type(error).__name__}: {error}"
        save()
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", choices=STUDIES, default="learning-speed")
    parser.add_argument("--profile", choices=["smoke"], default="smoke")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--report-only", type=Path)
    args = parser.parse_args()
    from manabot.training.analysis import report

    if args.report_only:
        report(args.report_only.resolve())
        return
    if args.out is None:
        parser.error("--out is required")
    torch.set_num_threads(1)
    out = args.out.resolve()
    try:
        run_study(args.study, out)
    finally:
        if (out / "study.json").exists():
            report(out)


if __name__ == "__main__":
    main()
