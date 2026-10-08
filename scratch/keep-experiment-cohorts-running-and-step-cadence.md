# Step-based MLOps — accepted direction, 2026-10-08

Jack Heart requested this implementation and autonomous delivery after PR268.
PR268 merged at 22f28522; PR269 independently repairs opaque startup diagnostics.
The exact failed main clean-machine job passed one rerun in 50.726 seconds;
its original timeout remains evidence, without a confirmed causal diagnosis.

A step is one completed self-play collection/learning iteration, including an
empty-filter iteration, not one optimizer call or environment transition.
Absolute updates include inherited continuation offsets; segment-local counts
remain separate. Ataraxos already consumes absolute iteration. Operational
leases, costs, credentials, watchdogs, report freshness and upload timers stay
in seconds. The live scientific cohort and queued 100k continuation retain
source 45940fe3/69594494 and their frozen hourly monitoring configuration.

Implement through existing TrainingRegime/TrainingRun, ExperimentSchedule,
PlannedRun, Job/CohortEntry, CheckpointQueue and reports. New monitoring cadence
uses a positive integer checkpoint_updates with zero-anchored exact boundaries.
Legacy explicit checkpoint_seconds remains readable/executable for frozen
records; it is no longer an authoring default. Interval and target are frozen
from measured throughput before launch, never recomputed during training.
Capacity jobs use the same step interval and expose common exact milestones.

A monitoring boundary exports once, terminal raw owns the exact endpoint, and
continuation begins strictly after the inherited boundary. Exact CPU recovery
keeps committed prior monitoring artifacts/coordinates and the same cadence.
The queue must deduplicate inherited checkpoints across attempt sources and
restart, while retaining failed attempts without speculative retries. Explicit
initialization admission is distinct from the scientific cadence; new step
continuation must not silently schedule another inherited-boundary evaluation.
Unsupported combinations fail before launching instead of waiting forever.

Reports lead with exact matched update coordinates and keep transitions,
optimizer steps/exposures, active time, wall time and dollars available. Existing
notebooks remain create-once and historical missing counters stay unavailable.
Other learning families retain their own named epoch/game units; do not present
those as sample-equivalent self-play steps or silently change frozen recipes.

Delete — do not maintain: hourly authoring defaults/help/examples and duplicate
endpoint monitoring in the new cadence path. Preserve explicit legacy fields,
immutable baseline files, frozen reports, operational timers and failure evidence.

Delivery slices: (1) cadence ownership and API/CLI/deploy execution/recovery with
focused milestone tests; (2) prospective experiment authoring/calibration guidance,
matched capacity/report/notebook defaults and remaining coordinate accounting.
Retain the full target across slices; neither completion implies a new campaign.

Verification planned: real tiny update loops, off-grid continuation and recovery,
queue restarts, positive/mutually exclusive intervals, frozen JSON identities,
exact capacity milestone intersection, notebook edit preservation, focused
Python/remote suites and CI. No paid validation or live cohort edit is needed.

Check: affected training gate 84 passed; isolated remote 162 passed/2 skipped, historical field-order failure repaired and JobSpec rerun 15 passed; exact cadence/admission final check pending. Ruff/diff checks passed. PR269 merged 01fd9029.
