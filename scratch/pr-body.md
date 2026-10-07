Training targets no longer need to be derived from rental duration. A reusable LaunchSpec binds a step-target TrainingRegime to machine hours, cost and artifact scope, and the existing deploy path uses one absolute deadline for worker permissions and shutdown.

## What changes

- Adds LaunchSpec, Machine and AccessScope; Experiment binds explicit case/seed launches to monitoring protocols. Fractional and 720-hour plans use the same model without changing update targets or iteration schedules.
- Connects `manabot deploy --launch` compilation/submission to the existing job client and supervisor. Collection stops at `pause_at`, leaving checkpoint, upload and cleanup reserves. The executor exports raw/EMA/Adam and reports an incomplete target as paused; only reaching the target completes it.
- Adds an allocation-deadline deny to worker STS policies. Issuer credentials stay on the launcher. CPU recovery-enabled recipes can explicitly continue paused updates on the same host; paused checkpoints remain available for monitoring without entering completed-target final cohorts.
- Removes FourHourPreparation/prepare_four_hour and the fixed preparation CLI. Frozen v1 serialized identities and active-time semantics remain readable. ETU-103's live checkout and source `68e0fbe9265a689891615274123587d653b5e66b` are untouched.

Bounded RunPod launches are supported. Long allocations fail admission before renting because renewable credentials and portable CUDA recovery are missing. Cancellation stops compute but does not immediately revoke copied STS credentials; artifact access ends at the allocation deadline. In-place extensions are rejected rather than updating only part of the enforcement. No paid rental or scientific campaign ran.

## API example

```python
from manabot.remote.plan import LaunchSpec
from manabot.training.checkpoint_queue import MonitoringBudget
from manabot.training.experiment_execution import LaunchRun
from manabot.training.experiments import Baseline, Experiment

# regime already specifies one self-play stage's updates and iteration schedules.
launch = LaunchSpec(machine=machine, lifetime_hours=4, spending_limit=3)
experiment = Experiment(
    name="fixed-target",
    baseline=Baseline.capture("recipe", regime),
    launches=(LaunchRun(
        case="fixed-target", seed=197, launch=launch,
        monitoring=MonitoringBudget(seconds=600, attempt_seconds=120),
        checkpoint_seconds=3600,
    ),),
)
plan, = experiment.compile_launches(source)  # pure; no rental
```

The [remote-job guide](docs/remote-jobs.md#step-targets-and-machine-allocations) includes the full example, CLI commands, ownership and provider limits.

## Checks

Offline CLI compilation and fake-provider submission; fractional/month construction and cost/refusal checks; matching permission/guardian deadlines; native CPU pause/recovery versus uninterrupted learning; interrupted-collection and export-reserve exhaustion; frozen v1 digest checks. Final remote/allocation suite: 101 passed, one CUDA-host skip. The affected broader suites passed after repairing ten stale error-message assertions; 48 recovery/Experiment/runner follow-up checks passed. Focused Ruff and diff checks passed. These are software fixtures, not live IAM or month-long operational proof.
