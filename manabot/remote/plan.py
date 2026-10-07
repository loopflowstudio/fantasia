"""Pure deployment planning. Rental declarations, never host CPU counts, own placement.

DeploymentPlan retains the input bytes and a fully resolved TrainingRegime. Source
identity is supplied by the CLI so compilation itself needs no provider or GPU.
"""

import hashlib
import math
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from manabot.infra.artifacts import split_s3_uri
from manabot.training.models import TrainingRegime, TrainSelfPlay

MAX_JOB_SECONDS = 12 * 3600


class Frozen(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class Machine(Frozen):
    """Provider shape and price ceilings, without an authority duration."""

    schema_version: Literal[1] = 1
    provider: Literal["runpod"] = "runpod"
    role: Literal["training"] = "training"
    gpu_count: Literal[1] = 1
    gpu_types: tuple[str, ...] = Field(min_length=1)
    workers: Literal[1] = 1
    thread_limit: int = Field(default=4, ge=1, le=4)
    vcpus: int = Field(ge=1)
    memory_gb: int = Field(ge=1)
    container_gb: int = Field(default=30, ge=10)
    volume_gb: int = Field(default=20, ge=1)
    image: str = Field(pattern=r"^[a-zA-Z0-9./_-]+@sha256:[a-f0-9]{64}$")
    hourly_ceiling: float = Field(gt=0)
    storage_hourly_allowance: float = Field(default=0.02, ge=0)


class HardwareMix(Machine):
    """Frozen v1 deployment input; new declarations use LaunchSpec."""

    dollar_cap: float = Field(gt=0)
    wall_seconds: int | float = Field(ge=60)
    setup_seconds: int = Field(default=300, ge=1)
    transfer_seconds: int = Field(default=300, ge=1)
    cleanup_seconds: int = Field(default=120, ge=30)

    @property
    def projected_dollars(self) -> float:
        return (
            (self.hourly_ceiling + self.storage_hourly_allowance)
            * self.wall_seconds
            / 3600
        )

    @model_validator(mode="after")
    def budget(self) -> "HardwareMix":
        if self.projected_dollars > self.dollar_cap:
            raise ValueError("rental allowance exceeds dollar cap")
        if (
            self.setup_seconds + self.transfer_seconds + self.cleanup_seconds
            >= self.wall_seconds
        ):
            raise ValueError("reserves consume rental allowance")
        return self


class AccessScope(Frozen):
    """Artifact namespace only. Issuer and provider credentials stay on the launcher."""

    destination: str = "s3://etudefantasia/manabot/jobs"

    @model_validator(mode="after")
    def literal_prefix(self) -> "AccessScope":
        _, prefix = split_s3_uri(self.destination)
        if not prefix or any(c in prefix for c in "*?[]") or ".." in prefix.split("/"):
            raise ValueError("access scope requires a literal private S3 prefix")
        return self


class LaunchSpec(Frozen):
    """One machine allocation; hours include setup, checkpoint, upload and cleanup.

    Construction is planning, not execution admission. Long allocations cannot
    execute on the current RunPod adapter without renewal and portable recovery.
    No throughput estimate or learning target belongs here.
    """

    machine: Machine
    lifetime_hours: float = Field(gt=0)
    spending_limit: float = Field(gt=0)
    access: AccessScope = AccessScope()
    setup_seconds: int = Field(default=300, ge=1)
    checkpoint_seconds: int = Field(default=120, ge=1)
    upload_seconds: int = Field(default=300, ge=1)
    cleanup_seconds: int = Field(default=120, ge=30)

    @property
    def lifetime_seconds(self) -> float:
        return self.lifetime_hours * 3600

    @property
    def projected_dollars(self) -> float:
        return self.mix().projected_dollars

    def mix(self) -> HardwareMix:
        """Compile the existing placement input; never author a second duration."""
        return HardwareMix(
            **self.machine.model_dump(),
            wall_seconds=self.lifetime_seconds,
            dollar_cap=self.spending_limit,
            setup_seconds=self.setup_seconds,
            transfer_seconds=self.checkpoint_seconds + self.upload_seconds,
            cleanup_seconds=self.cleanup_seconds,
        )

    @model_validator(mode="after")
    def budget(self) -> "LaunchSpec":
        self.mix()
        return self

    def admit(self, now: float) -> "Allocation":
        if self.lifetime_seconds > MAX_JOB_SECONDS - 60:
            raise ValueError(
                "RunPod allocation unavailable: renewable worker credentials and "
                "durable complete-state CUDA recovery across replacement workers "
                "are not implemented (single STS session limit: twelve hours)"
            )
        return Allocation(launch=self, admitted_at=now)

    def admit_execution(self) -> None:
        """Admit the bounded adapter; long renewal/replacement remains unsupported."""
        self.admit(0)


class Allocation(Frozen):
    """Absolute authority receipt. Every cutoff is derived from one admission."""

    launch: LaunchSpec
    admitted_at: float = Field(ge=0)

    @property
    def deadline(self) -> float:
        # The guardian uses Unix seconds; round down once for both enforcement owners.
        return math.floor(self.admitted_at + self.launch.lifetime_seconds)

    @property
    def pause_at(self) -> float:
        return (
            self.deadline
            - self.launch.checkpoint_seconds
            - self.launch.upload_seconds
            - self.launch.cleanup_seconds
        )

    @property
    def checkpoint_deadline(self) -> float:
        return self.deadline - self.launch.upload_seconds - self.launch.cleanup_seconds

    def renewal_cutoff(self, now: float) -> float:
        if now >= self.deadline:
            raise ValueError("allocation has expired; renewal forbidden")
        # This bound is useful to adapters but does not implement a renewer.
        return self.deadline

    def extend(self, lifetime_hours: float) -> "Allocation":
        raise ValueError(
            "RunPod extension unavailable: persisted intent, guardian and issued "
            "session policies cannot be updated atomically; original deadline remains"
        )


class Source(Frozen):
    commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    tree: str = Field(pattern=r"^[0-9a-f]{40}$")
    lock_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class DeploymentPlan(Frozen):
    schema_version: Literal[1, 2] = 1
    launch: LaunchSpec | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    input_json: str
    input_sha256: str
    regime: TrainingRegime
    mix: HardwareMix
    source: Source
    seed: int = Field(ge=0)
    projected_dollars: float

    @model_validator(mode="after")
    def consistent(self) -> "DeploymentPlan":
        if digest(self.input_json.encode()) != self.input_sha256:
            raise ValueError("input regime digest differs")
        if self.schema_version == 1 and self.mix.dollar_cap >= 5:
            raise ValueError(
                "frozen v1 deployment requires a dollar cap below five; use LaunchSpec"
            )
        if (self.schema_version == 2) != (self.launch is not None):
            raise ValueError("LaunchSpec requires deployment schema 2")
        if self.launch is not None and self.mix != self.launch.mix():
            raise ValueError("placement differs from LaunchSpec")
        expected = resolve(self.input_json, self.mix, launch=self.launch)
        if (
            expected != self.regime
            or self.projected_dollars != self.mix.projected_dollars
        ):
            raise ValueError("resolved deployment differs from input and mix")
        return self


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve(
    input_json: str, mix: HardwareMix, *, launch: LaunchSpec | None = None
) -> TrainingRegime:
    regime = TrainingRegime.model_validate_json(input_json)
    if regime.recovery_max_microsteps is not None:
        raise ValueError("remote recovery is unsupported")
    if regime.agent.compound_decisions or regime.agent.belief_count_buckets:
        raise ValueError("remote deployment requires ordinary self-play")
    if launch is not None:
        if len(regime.stages) != 1 or regime.schedule_clock != "iteration_fraction":
            raise ValueError(
                "LaunchSpec requires one step-target stage with iteration_fraction schedules"
            )
        if any(
            isinstance(stage, TrainSelfPlay) and stage.active_seconds is not None
            for stage in regime.stages
        ):
            raise ValueError(
                "LaunchSpec requires update targets; active-time recipes are frozen v1 records"
            )
    for stage in regime.stages:
        if not isinstance(stage, TrainSelfPlay) or stage.opponent is not None:
            raise ValueError("remote deployment requires self-contained self-play")
        if stage.execution.memory_bytes > mix.memory_gb * 1024**3:
            raise ValueError("declared rental memory is below the stage requirement")
        stage.execution.device = "cuda"
        stage.execution.threads = min(
            stage.execution.threads, mix.thread_limit, mix.vcpus, 4
        )
    reserves = mix.setup_seconds + mix.transfer_seconds + mix.cleanup_seconds
    if launch is None and regime.wall_seconds + reserves > mix.wall_seconds:
        raise ValueError("run watchdog and reserves exceed rental allowance")
    if (
        launch is None
        and sum(stage.execution.wall_seconds for stage in regime.stages)
        > regime.wall_seconds
    ):
        raise ValueError("stage watchdogs exceed run allowance")
    return TrainingRegime.model_validate(regime.model_dump())


def compile_plan(
    input_json: str, mix: HardwareMix | LaunchSpec, source: Source, seed: int
) -> DeploymentPlan:
    launch = mix if isinstance(mix, LaunchSpec) else None
    placement = launch.mix() if launch is not None else mix
    assert isinstance(placement, HardwareMix)
    return DeploymentPlan(
        schema_version=2 if launch is not None else 1,
        launch=launch,
        input_json=input_json,
        input_sha256=digest(input_json.encode()),
        regime=resolve(input_json, placement, launch=launch),
        mix=placement,
        source=source,
        seed=seed,
        projected_dollars=placement.projected_dollars,
    )
