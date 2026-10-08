# Step accounting and reports — 2026-10-08

Jack Heart authorized this second slice and autonomous delivery. PR270 merged at fc9c8aeb with all ten checks passing; this serial PR
completes the counter/report/calibration slice.
The first slice passed 84 affected training checks, 10 final cadence checks and
15 repaired JobSpec checks after the isolated remote suite exposed legacy
serialization order. The frozen live cohort and continuation stay unchanged.

This slice records absolute versus segment-local collect/learn iterations,
completed optimizer calls and sample exposures using TrainingRun's existing
owners. Empty filtering advances iterations but not optimizer work. Rejected
partial updates retain separate numerical-failure receipts. Historical unknown
counts remain unavailable; no inference from exposures or Adam parameter steps.
Portable imports retain measured ancestor counts; exact CPU recovery retains
the committed prefix. No learner rate formulas change.

StepCalibration is a saved-pilot projection in experiment_execution, not another
scheduler or admission owner. It converts requested active hours once into
frozen counts. Capacity declarations share exact intervals. New notebooks lead
with matched updates, then samples/active time; edited notebooks remain intact.
RunControl defaults to iteration_fraction for new authoring, while serialized
baselines and TrainingRegime's legacy reader/default are preserved.

Limits: new cadence requires one ordinary self-play stage; other learning units
remain explicit legacy clocks. CUDA continuation, 100k completion and final
science remain live operational work, not acceptance supplied by these proofs.

Check: accounting/report/learning-state/monitoring/authoring suite 65 passed;
final cadence, complete-state PPO/Ataraxos recovery and frozen JobSpec checks
31 passed. Ruff and diff checks passed. No new rental or live configuration edit.

Read-only compatibility: the actual six-job cohort has identity
1e14b16404e9a7e152b3a28a252a3ad27e15091dae87fc54c4793f602197c88c
under both installed Mini source and this reader; its six hourly intervals remain
3600 seconds, with no new step cadence injected.
