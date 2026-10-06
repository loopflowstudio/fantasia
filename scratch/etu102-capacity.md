# ETU-102 capacity plan — reconciled 2026-10-05

Jack Heart authorized independent software completion, publication and landing
after auditing merged PRs 222/223. Those PRs already supply validated AgentSpec
width/depth/heads, baseline-preserving equations and the with_capacity ladder.
They remain the sole architecture configuration owner.

Implemented: versioned derived architecture identities, total/trainable component
counts, TrainingRun identity, PPO/BC checkpoint receipts and ordinary reload
admission. Ladder tests cover scalar/WDL shapes, legal masks, exact reload output,
equal-shaped metadata contradictions and receipt-free historical admission.

The bounded calibration reuses TrainingRegime and the existing arena. The retained
attempt at `90c55627` completed in 212.56 seconds with six raw checkpoints and
40 exact-replayed games. Its failed default-calibration test remains archived;
[the calibration guide](../docs/training-calibration.md) owns commands and evidence.
The later compression at `b75a7016` shares canonical run lookup and derives probe
deadlines from the resolved allowance; probe receipts expose actual loop counts
and batch size. It does not change architecture identities or model equations.

Remaining: delivery verification and publication/landing of the final revision
through the caller's delivery operation. No further software mechanism or product
decision was identified in this reconciliation. Scientific capacity comparisons,
uncontended timing, demo admission and chapter strength remain separate work;
ETU-91 and its retained evidence are untouched. Sampled RSS is a lower bound,
and per-checkpoint inference batches do not provide matched-input scaling evidence.

`uv run pytest tests/training/test_calibration.py tests/model/test_capacity.py -q` — 14 passed in 31.14 s; focused Ruff and diff checks passed. Broader acceptance remains with gate/CI; no capacity study was run.
