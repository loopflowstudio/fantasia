"""Active training and evaluation budgets, independent of worker placement.

ActiveTrainingBudget derives nominal milestones and watchdog reserves for one
self-play run. TrainingRegime/TrainingRun still own execution and actual clocks;
these projections neither change iteration schedules nor implement recovery.
"""

import math

from pydantic import ConfigDict, Field, model_validator

from manabot.training.models import Strict


class ActiveTrainingBudget(Strict):
    model_config = ConfigDict(frozen=True)

    training_hours: float = Field(gt=0)
    checkpoint_hours: float = Field(gt=0)
    evaluation_seconds: float = Field(gt=0)
    terminal_cohorts: int = Field(ge=1)
    stage_overhead_seconds: float = Field(gt=0)
    run_overhead_seconds: float = Field(ge=0)

    @property
    def active_seconds(self) -> float:
        return self.training_hours * 3600

    @property
    def checkpoint_seconds(self) -> float:
        return self.checkpoint_hours * 3600

    @property
    def milestones(self) -> tuple[float, ...]:
        """Interior cadence points plus the endpoint, exactly once.

        Runtime exports occur after complete updates and may skip nominal points
        or overshoot the endpoint. Those actual coordinates remain authoritative.
        """
        interior = math.ceil(self.active_seconds / self.checkpoint_seconds) - 1
        return tuple(self.checkpoint_seconds * i for i in range(1, interior + 1)) + (
            self.active_seconds,
        )

    @property
    def evaluation_cohorts(self) -> int:
        # Initialization + interior checkpoints + separately reserved final cohorts.
        return len(self.milestones) + self.terminal_cohorts

    @property
    def evaluator_seconds(self) -> float:
        return self.evaluation_cohorts * self.evaluation_seconds

    @property
    def stage_seconds(self) -> float:
        # Initialization gates learning. Exports/setup/whole-update overshoot consume
        # the explicit overhead reserve, never the active training allocation.
        return self.active_seconds + self.evaluation_seconds + self.stage_overhead_seconds

    @property
    def run_seconds(self) -> float:
        return self.stage_seconds + self.run_overhead_seconds

    @property
    def evaluation_tail_seconds(self) -> float:
        # An interior export can arrive just before the terminal update. Reserve
        # its remaining allowance as well as every terminal cohort.
        pending = int(len(self.milestones) > 1)
        return (self.terminal_cohorts + pending) * self.evaluation_seconds

    @model_validator(mode="after")
    def bounded_projection(self) -> "ActiveTrainingBudget":
        if not math.isfinite(self.run_seconds):
            raise ValueError("derived training duration must be finite")
        if self.active_seconds / self.checkpoint_seconds > 100_000:
            raise ValueError("preparation exceeds 100000 checkpoint milestones")
        if self.evaluation_seconds > self.checkpoint_seconds:
            raise ValueError("evaluation allowance exceeds cadence of the single evaluator")
        return self
