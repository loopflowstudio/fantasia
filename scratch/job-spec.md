# JobSpec simplification — accepted 2026-10-07

Jack Heart requested one declarative JobSpec and an admitted Job. Machine owns
hardware; JobSpec owns lifetime, spending and access. Experiment.jobs binds
JobRun cases/seeds/evaluation; compile_jobs and prepare_job use the existing
compiler and lifecycle. One schema-2 plan contains one spec.

Delete — do not maintain: LaunchSpec, HardwareMix public inputs/unions/projection,
RemoteJobSpec naming, --mix/--launch, and compatibility for the unshipped draft.
Only private schema-1 persistence readers preserve actual historical semantics.
The calibration-era two-stage freeze authoring function is retired instead of
silently changing its scientific protocol to fit current single-stage admission.
Its saved CapacityPlans and pinned execution remain readable; new authoring uses
Experiment.jobs. No ETU-103 checkout, evidence or scientific spending changed.

Retained limits: no worker credential renewal, portable CUDA continuation,
immediate STS revocation or in-place extension. Existing bounded submissions,
pause reserves and CPU recovery remain supported.

Validation: `uv run --extra dev --extra artifacts pytest tests/remote/ ...` — 101 remote passed, one CUDA-host skip; 58 allocation/recovery/Experiment/capacity checks passed; affected Ruff/format and diff checks passed. The initial reserve assertion failure was corrected and the remote suite rerun.
