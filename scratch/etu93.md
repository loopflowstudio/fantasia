# ETU-93 omitted controls

2026-10-04. Jack Heart authorized implementation and landing, bounded proofs only.
ETU-91 is immutable. Scientific budgets and technique retention remain unresolved.

Extend existing Learning/AtaraxosMoveLearning and executor: independently select
inclusive quantile versus top-count filtering, actor-only versus actor+critic
selection, and EMA behavior with saved collection probabilities and same-model
bootstrap. Preserve existing defaults. Add stratified raw/selected advantage and
critic residual diagnostics with observed terminal distance (unknown tails censored).
Generate typed independent contrast recipes without launching scientific work.
Reuse TrainingRun/VerifyStore and arena; no new identity or result store.

Demo: generate omitted-control recipes, execute a bounded EMA-behavior/actor-only
real-game recipe and reload raw/EMA exports. Tests must establish selection ties,
empty actor selection with critic updates, terminal/reset censoring and actual
EMA collection likelihoods. No architecture auxiliaries or expensive scoring.
No deletion targets: extend existing owners.

Implemented and reconciled: shared selection diagnostics, explicit actor support,
EMA behavior and bootstrap, separate recipe generator, variant-aware arena and
uncertainty. No new scientific allocation. Gate: 98 training tests passed;
bounded behavior proof completed 48 replayed games in 116.83 s. Final metadata
validation tests pending. Scientific acceptance and independent terminal-return
residuals for censored episodes remain open at the durable protocol.
