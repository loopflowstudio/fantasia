"""Validated training recipes and durable execution records."""

from typing import Annotated, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, model_validator

from manabot.infra.hypers import AgentHypers, MatchHypers, ObservationSpaceHypers
from manabot.sim.local_update import LocalSearchConfig


class ArtifactReference(TypedDict):
    """Immutable local bytes admitted by content digest."""

    path: str
    sha256: str
    bytes: int


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Schedule(Strict):
    initial: float = Field(ge=0)
    decay: float = Field(default=0, ge=0)
    power: float = Field(default=1, ge=0)

    def at(self, progress: float) -> float:
        return (
            self.initial
            * (1 + self.decay * min(1.0, max(0.0, progress))) ** -self.power
        )


class Learning(Strict):
    gradient: Literal["ppo"] = "ppo"
    gamma: float = Field(default=1, ge=0, le=1)
    policy_lambda: float = Field(default=0.95, ge=0, le=1)
    value_lambda: float = Field(default=1, ge=0, le=1)
    retained_fraction: float = Field(default=0.5, gt=0, le=1)
    min_advantage: float = Field(default=0, ge=0)
    reference: Literal["uniform", "action_type_uniform"] = "uniform"
    learning_rate: Schedule = Schedule(initial=2.5e-4, decay=9)
    tau: Schedule = Schedule(initial=0.01, decay=9)
    collection_kl: float = Field(default=0.1, ge=0)
    clip: float = Field(default=0.1, gt=0)
    value_weight: float = Field(default=0.5, ge=0)
    max_grad_norm: float = Field(default=0.5, gt=0)
    epochs: int = Field(default=4, ge=1)
    minibatches: int = Field(default=4, ge=1)
    ema: float | None = Field(default=None, ge=0, lt=1)


class AtaraxosMoveLearning(Strict):
    """Supplement S3.4 move update; MTG reference and batch sizes are adaptations.

    Iteration schedules, one epoch and no advantage normalization belong to
    this method, rather than inheriting the PPO control's elapsed-time recipe.
    """

    gradient: Literal["ataraxos_move"]
    policy_lambda: float = Field(default=0.5, ge=0, le=1)
    value_lambda: float = Field(default=0.8, ge=0, le=1)
    advantage_quantile: float = Field(default=0.75, ge=0, le=1)
    min_advantage: float = Field(default=0.01, ge=0)
    reference: Literal["uniform", "action_type_uniform"] = "action_type_uniform"
    clip: float = Field(default=0.2, gt=0, lt=1)
    collection_kl: float = Field(default=0.1, ge=0)
    learning_rate_scale: float = Field(default=0.5, gt=0)
    learning_rate_power: float = Field(default=1.1, ge=0)
    learning_rate_min: float = Field(default=5e-6, gt=0)
    learning_rate_max: float = Field(default=1e-4, gt=0)
    tau_scale: float = Field(default=0.05, ge=0)
    tau_power: float = Field(default=0.3, ge=0)
    max_grad_norm: float = Field(default=0.267, gt=0)
    ema: float | None = Field(default=0.999, ge=0, lt=1)

    @model_validator(mode="after")
    def valid_learning_rate_bounds(self) -> "AtaraxosMoveLearning":
        if self.learning_rate_min > self.learning_rate_max:
            raise ValueError("learning rate minimum exceeds maximum")
        return self

    def rates(self, iteration: int) -> tuple[float, float]:
        """One-based completed collection/update iteration, including skips."""
        if iteration < 1:
            raise ValueError("Ataraxos iteration must be positive")
        rate = self.learning_rate_scale / iteration**self.learning_rate_power
        return (
            min(self.learning_rate_max, max(self.learning_rate_min, rate)),
            self.tau_scale / iteration**self.tau_power,
        )


class Execution(Strict):
    device: Literal["cpu"] = "cpu"
    precision: Literal["float32"] = "float32"
    workers: Literal[1] = 1
    threads: int = Field(default=1, ge=1, le=4)
    wall_seconds: float = Field(default=300, gt=0)
    memory_bytes: int = Field(default=32 * 1024**3, gt=0)


class Stage(Strict):
    id: str = Field(pattern=r"^[a-z][a-z0-9-]*$")
    execution: Execution = Execution()


class CollectSearch(Stage):
    operation: Literal["collect_search"]
    policy: Literal["uniform-prior-determinized-puct"] = (
        "uniform-prior-determinized-puct"
    )
    target: Literal["visit_distribution"] = "visit_distribution"
    games: int = Field(ge=2)
    simulations: int = Field(default=64, ge=1)
    worlds: int = Field(default=4, ge=1)
    max_steps: int = Field(default=2000, ge=1)


class CollectLocalUpdate(Stage):
    """Freeze an admitted raw/EMA policy for exact-range local targets."""

    operation: Literal["collect_local_update"]
    policy: str
    weights: Literal["raw", "ema"] = "raw"
    games: int = Field(ge=2)
    max_steps: int = Field(default=2000, ge=1)
    search: LocalSearchConfig = LocalSearchConfig()


class TrainSupervised(Stage):
    operation: Literal["train_supervised"]
    trainer: Literal["search_supervised"] = "search_supervised"
    optimizer: Literal["adam"] = "adam"
    trainable: Literal["policy"] = "policy"
    target: Literal[
        "visit_distribution", "local_soft", "local_argmax", "local_allocation"
    ] = "visit_distribution"
    datasets: list[str] = Field(min_length=1)
    initial: str | None = None
    epochs: int = Field(default=10, ge=1)
    batch_size: int = Field(default=128, ge=1)
    learning_rate: float = Field(default=0.001, gt=0)


class FrozenOpponent(Strict):
    """Exact admitted policy bytes used only for opponent-seat inference."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, frozen=True)
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class TrainSelfPlay(Stage):
    operation: Literal["train_self_play"]
    trainer: Literal["net_opponent"] = "net_opponent"
    optimizer: Literal["adam"] = "adam"
    trainable: Literal["policy_value"] = "policy_value"
    behavior: Literal["current-self", "frozen"] = "current-self"
    opponent: FrozenOpponent | None = None
    initial: str | None = None
    updates: int = Field(default=2, ge=1)
    streams: int = Field(default=4, ge=2)
    transitions: int = Field(default=256, ge=1)
    learning: Learning | AtaraxosMoveLearning = Learning()

    @model_validator(mode="after")
    def frozen_opponent(self) -> "TrainSelfPlay":
        if (self.behavior == "frozen") != (self.opponent is not None):
            raise ValueError("frozen behavior requires exactly one frozen opponent")
        if self.behavior == "frozen" and self.streams % 2:
            raise ValueError(
                "frozen opponent training requires even streams for both decks"
            )
        return self


class CollectBelief(Stage):
    """Freeze one admitted policy artifact before collecting private labels."""

    operation: Literal["collect_belief"]
    policy: str
    weights: Literal["raw", "ema"] = "raw"
    games: int = Field(ge=3)
    max_steps: int = Field(default=2000, ge=1)


class TrainBelief(Stage):
    """Fit only the sampler; policy weights are never updated by belief NLL."""

    operation: Literal["train_belief"]
    dataset: str
    steps: int = Field(default=32, ge=1)
    batch_size: int = Field(default=32, ge=1)
    hidden_size: int = Field(default=32, ge=2)
    learning_rate: float = Field(default=0.001, gt=0)
    history_dropout: float = Field(default=0, ge=0, le=1)
    evaluation_samples: int = Field(default=32, ge=1)


class TrainCompound(Stage):
    """Complete-game self-play with explicit decoder credit units."""

    operation: Literal["train_compound"]
    initial: str | None = None
    updates: int = Field(default=1, ge=1)
    games_per_update: int = Field(default=2, ge=1)
    max_commands: int = Field(default=4000, ge=1)
    grouping: Literal["sequential", "grouped"] = "grouped"
    estimator: Literal["outcome", "bootstrapped"] = "outcome"
    skip_trivial: bool = True
    learning: Learning = Learning(retained_fraction=1, epochs=1)

    @model_validator(mode="after")
    def supported_learning(self) -> "TrainCompound":
        if self.learning.reference != "uniform" or self.learning.ema is not None:
            raise ValueError(
                "compound stages require conditional uniform reference and raw weights"
            )
        return self


Operation = Annotated[
    CollectSearch
    | CollectLocalUpdate
    | TrainSupervised
    | TrainSelfPlay
    | TrainCompound
    | CollectBelief
    | TrainBelief,
