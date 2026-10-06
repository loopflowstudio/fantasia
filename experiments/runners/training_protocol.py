"""Frozen protocol for the bounded training-regime workflow studies."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EvaluationProtocol(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)
    schema_version: Literal[2] = 2
    study: Literal[
        "learning-speed",
        "ataraxos-ablations",
        "omitted-controls",
        "compound-decisions",
        "training-calibration",
        "capacity-calibration",
        "model-capacity",
        "value-models",
        "value-token-screen",
    ]
    purpose: Literal["workflow-smoke", "calibration", "scientific", "screening"] = (
        "workflow-smoke"
    )
    evaluation_variants: tuple[Literal["raw", "ema"], ...] = ("raw",)
    regime_digests: tuple[str, ...]
    training_seeds: tuple[int, ...] = (197,)
    paired_deals: tuple[int, ...] = (910001,)
    anchor_deals: tuple[int, ...] = (920001,)
    checkpoint_count: int = Field(default=2, ge=2)
    cost_cutoffs_seconds: tuple[float, ...] = ()
    early_progress_seconds: float | None = Field(
        default=None, gt=0, exclude_if=lambda v: v is None
    )
    progress_score: float | None = Field(
        default=None, ge=0, le=1, exclude_if=lambda v: v is None
    )
    anchors: tuple[Literal["random", "scripted-greedy", "puct-64"], ...] = ("random",)
    endpoint_paired_deals: tuple[int, ...] = ()
    endpoint_anchor_deals: tuple[int, ...] = ()
    endpoint_seed_pairs: tuple[tuple[int, int], ...] = ()
    seat_deck_legs: Literal[4] = 4
    inference: Literal["stochastic-policy-cpu-one-thread"] = (
        "stochastic-policy-cpu-one-thread"
    )
    game_seconds: float = Field(default=120, gt=0, le=120)
    max_commands: int = Field(default=10000, gt=0, le=10000)
    process_seconds: float = Field(default=900, gt=0, le=168 * 3600)
    selection: Literal[
        "all-completed-cutoffs-raw", "all-completed-cutoffs-raw-and-ema"
    ] = "all-completed-cutoffs-raw"
    uncertainty: Literal["cross-seed-unavailable", "paired-seed-descriptive"] = (
        "cross-seed-unavailable"
    )
    incomplete: Literal["fail-retain-all-attempts"] = "fail-retain-all-attempts"

    @model_validator(mode="after")
    def disjoint(self) -> "EvaluationProtocol":
        if (self.study == "value-token-screen") != (self.purpose == "screening"):
            raise ValueError(
                "value-token-screen requires its distinct screening purpose"
            )
        if self.purpose == "screening" and (
            len(self.training_seeds) != 3
            or self.anchors != ("scripted-greedy",)
            or self.checkpoint_count != 2
            or len(self.anchor_deals) != 25
            or self.paired_deals
            or self.endpoint_paired_deals
            or self.endpoint_anchor_deals
            or self.endpoint_seed_pairs
            or self.cost_cutoffs_seconds
            or self.process_seconds != 28800
            or self.uncertainty != "paired-seed-descriptive"
        ):
            raise ValueError(
                "screen requires three seeds, two checkpoints, 25 four-leg scripted deals and eight hours"
            )
        if self.study == "model-capacity" and (
            self.early_progress_seconds is None or self.progress_score is None
        ):
            raise ValueError("capacity requires an early window and threshold")
