# ETU-106 delivery — 2026-10-05

Jack Heart authorized software delivery, landing and necessary local checks,
with recovery from retained exports preferred over retraining. Focused value-model
software is complete: historical/masked mean and one/two-layer width-64 shared
value tokens, independently crossed with scalar/WDL. Defaults and historical
initialization remain compatible. ETU-104's general implementation is separate;
recent-event inputs remain next, and recurrent memory is deferred.

The original 36.12-second failed smoke remains unchanged at
`.runs/etu106-value-smoke`. Evaluation-only recovery at
`.runs/etu106-value-recovery` reused the original plan and checkpoints, normalized
only arena IDs and retained separate source/runner provenance. All 120 games in
30 cells exact-replayed; all 16 raw checkpoints played both deck/seat assignments.
Combined charged time was 382.86 seconds of the original 900-second ceiling.
No retraining, scientific campaign or ETU-91 mutation occurred.

Delegated read-only technical review found registration/recovery blockers, now
fixed, and a historical-initialization evidence gap closed with direct base-code
comparison. This is not human review approval. Durable details, assumptions,
commands and evidence limits are in experiments/value-models.md and Wave memory.

Remaining: LF preparation, required CI and authoritative merge reconciliation.
Keep the Task open for subsequent architecture-feature work; do not mark scientific
or human-challenger outcomes complete. ETU-104's software dependency clears on merge.

Check: 42 focused model checks and 16 recovery/study checks pass; 120/120 games
exact-replayed; original evidence unchanged; offline report/metrics/cost comparison
regenerate byte-identically; historical initialization matches base bytes.
