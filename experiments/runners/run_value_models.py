"""Resolve the bounded value-model factorial through the existing study executor.

Generation is deterministic and does not train. Only the smoke profile is
allocated; scientific scoring needs a separately reviewed protocol.
"""

import argparse
from pathlib import Path

from experiments.runners.run_training_regimes import run_study
from experiments.runners.training_protocol import EvaluationProtocol, ResolvedStudy
from manabot.arena.models import canonical_sha256
from manabot.training.analysis import report
from manabot.training.models import TrainingRegime, TrainSelfPlay

ROOT = Path(__file__).resolve().parents[2]


def smoke_plan() -> ResolvedStudy:
    template = TrainingRegime.model_validate_json(
        (ROOT / "experiments/regimes/ataraxos-move-scalar.json").read_text()
    )
    recipes: list[TrainingRegime] = []
    for aggregation, depth in (
        ("historical_mean", 1),
        ("masked_mean", 1),
        ("value_token", 1),
        ("value_token", 2),
    ):
        for kind in ("scalar", "categorical_wdl"):
            recipe = template.model_copy(deep=True)
            recipe.id = f"value-{aggregation}-{depth}-{kind}"
            recipe.agent = recipe.agent.model_validate(
                {
                    **recipe.agent.model_dump(),
                    "hidden_dim": 64,
                    "num_attention_heads": 4,
                    "value_aggregation": aggregation,
                    "attention_layers": depth,
                    "value_kind": kind,
                }
            )
            recipe.wall_seconds = 60
            for stage in recipe.stages:
                assert isinstance(stage, TrainSelfPlay)
                stage.execution.wall_seconds = 30
            recipes.append(TrainingRegime.model_validate(recipe.model_dump()))
    return ResolvedStudy(
        protocol=EvaluationProtocol(
            study="value-models",
            regime_digests=tuple(
                canonical_sha256(recipe.model_dump(mode="json")) for recipe in recipes
            ),
            training_seeds=(1061,),
            paired_deals=(910106,),
            anchor_deals=(920106,),
            process_seconds=900,
        ),
        recipes=tuple(recipe.model_dump(mode="json") for recipe in recipes),
        allocation_seconds=900,
        prior_campaign_seconds=0,
        calibration_evidence="ETU-106 bounded workflow only; strength unresolved",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("smoke",), default="smoke")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write-plan", type=Path)
    action.add_argument("--out", type=Path)
    action.add_argument("--report-only", type=Path)
    args = parser.parse_args()
    if args.report_only:
        report(args.report_only)
    elif args.write_plan:
        with args.write_plan.open("x") as stream:
            stream.write(smoke_plan().model_dump_json(indent=2) + "\n")
    else:
        run_study("value-models", args.out.resolve(), smoke_plan())


if __name__ == "__main__":
    main()
