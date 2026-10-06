# Ataraxos-scale ordinary models

ETU-115 · 2026-10-06 · Implemented from Jack Heart's Task direction.
Software and short laptop measurements are authorized; no scientific cohort,
rented compute or ETU-107 design approval is inferred.

## Implemented outcome

AgentSpec owns positive attention depth and optional feedforward width. Unset
expansion is omitted from serialization and retains heads × width. Explicit
historical expansion canonicalizes to the same architecture identity; recipe
provenance retains the authored choice. Attention-off rejects custom expansion;
compound depth remains one. Existing initialization, weight names and equations
are preserved. Frozen six-model pre-change weights/receipts and the complete
default capacity-plan digest were captured before editing at the unchanged
`fd7437df` implementation. Weight hash checks are runtime/platform-specific;
architecture/recipe identities are portable.

`with_capacity` supports arbitrary positive depth and optional expansion;
omission preserves the baseline and explicit None resets it. The existing
ladder adds 384/8/1536 through `include_ataraxos=True`. ETU-103's three default
cases and scientific cohort are unchanged. ETU-107's implementation-time Task snapshot was a proposal awaiting review;
this work changes no decoder, decision, or policy-scoring contract.
ETU-114 retains device/stage execution ownership.

The calibration CLI adds `--scale`: isolated child probes, ordinary CPU
TrainingRegime fixtures, real shared semantic input, source/configuration
receipts, typed timing/memory records, retained failures and bounded deadlines.
The current command uses a continuous budget clock and persists setup failures.
No new training authority or device backend was introduced.

## Measured result and repairs

The [durable report](../docs/evidence/ataraxos-scale-2026-10-06.md) and adjacent
JSON own exact measurements, recipes, hashes and evidence limits. Full outputs
remain retained under `.runs/etu115-scale`. The large semantic
scalar-token model has 16,815,746 parameters and 203 attention slots. All four
rungs trained/exported. All eight CPU/MPS batch-4 float32 probes completed.

The fixture comparison originally mixed train/eval modes and failed after
successful exports. The fixed verifier uses eval mode for both models. Separate
read-only verification recovered all four existing exports with changed weights,
positive exposures and exact output equality; no training/timing repeated.
The original failed attempts remain retained. Elapsed through recovery was
208.09 seconds within the 900-second allocation. Large CPU forward/update rates
were 53/11 samples/s; MPS 117/16. Host load changed sharply and first-fixture
setup overlapped the tail of focused tests. No scaling/strength conclusion.

Two streams replace the planned one because ordinary executor admission requires
two; the fixture still has one update and eight learner transitions. Static
parameter/gradient/Adam estimates are distinct from sampled RSS/MPS allocator
readings. No activation-peak or large-batch fit guarantee. Default attention is
202 visible slots plus one value token, correcting the Task estimate of
270–300; actions/events are not attention rows.
Naive padding removal changes historical pooling and focus/ownership indexes.
No packing or observation capacity/world change was implemented.

## Reconciled status — 2026-10-06

Implementation and bounded measurement acceptance have retained evidence. The
large rung is opt-in to preserve ETU-103's default cohort and recipe identities.
The four original verifier failures remain failures; recovery separately proves
reload without replacing their records. MPS evidence covers model execution only;
ETU-114 still owns training-stage device support. No new product decision is needed.

Gate owns broader affected-suite verification and retained-evidence review.
Publication and landing remain later Flow operations. Chapter strength and
human-play outcomes remain outside this bounded software task.

Check: prior `uv run pytest -q tests/model/test_capacity_compatibility.py tests/training/test_scale_probe.py tests/training/test_architecture_recipes.py` — 11 passed; reconciliation inspected code and retained evidence without rerunning timings; broader verification remains with gate.
