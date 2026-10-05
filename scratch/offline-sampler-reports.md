# Offline sampler reports

2026-10-04: Jack Heart authorized software delivery without new training.

One command reads immutable whole-game datasets and an optional admitted sampler,
then writes JSON with per-split physical/learned quality at declared sample counts.
Reuse sampling_fit metrics and existing artifact admission; no search or Rules
changes. A supplied training dataset binds learned bytes; foreign evaluation data
must match schema/world and is identified separately. Prior-only reporting needs
no model artifact. Statistical results replay with fixed inputs/seed/runtime;
latency and Python allocation peaks are measured, not deterministic bytes.

Unsupported arbitrary queries, exact-posterior error, native peak memory, and
strength are explicit report fields. No support enumeration or optimizer runs.
Whole-game membership is retained; overlapping foreign train games fail admission.

Acceptance: deterministic saved fixtures exercise CLI, artifact mismatch, foreign
identity, label isolation, and widened count spaces. Additive capability: no
predecessor to delete. Gate runs focused tests and Ruff; CI owns broader checks.

Implemented the typed saved-artifact command, prior-only mode, digest-bound
learned admission, per-split sensitivity rows and explicit unsupported metrics.
Compression reused the existing arm evaluator instead of duplicating formulas.
CI now includes the report acceptance suite. No native or search files changed.

Gate: 15 focused sampler/report checks passed (3 fitting/cohort checks excluded);
a subsequent invalid-draw case brought the report suite to 7 passing checks.
Ruff and diff checks passed. Fixed-weight report tests run no optimizer; the
broader existing sampler suite includes a bounded toy-learning regression.
