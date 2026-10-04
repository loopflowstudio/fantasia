# Held-out filter analysis

2026-10-04. Jack Heart authorized bounded implementation and delivery after PR210;
scientific acceptance stays open. ETU-95 is independently active; ETU-91 is frozen.

Add `collect_selection` to TrainingRegime, using a prior admitted self-play raw/EMA
checkpoint or an explicit TrainingRun/stage dependency in the same VerifyStore.
Freeze unique deal seeds, action seeds, assignments and development/held-out splits
in the recipe before collection. Both seats use one fixed identified policy.
Save complete-game typed rows and semantic receipt journals as ordinary artifacts;
retain partial failed journals and costs, fail the cohort on any unfinished game.
No training or threshold fitting occurs on this population. Whole-game held-out
means reserved from this diagnostic's development partition and unused for updates;
it does not prove absence of coincident deals in historical training RNG streams.

Reuse transition GAE and selection masks. Offline diagnostic filter scope is each
partition's complete population, in game/seat/decision order (not historical live
minibatches). Distances count same-viewer transitions to real terminal; terminal=0.
Retain lambda-target residuals separately from signed/absolute sampled terminal
outcome residuals and discounted Monte Carlo residuals. Categorical expected-value
residuals use signed loss/draw/win expectation; no categorical calibration claim.
Report within action/distance strata retained/excluded summaries and game-cluster
bootstrap intervals, conditional on the frozen policy. No causal benefit or true
expected-value error claim, no extra training replicates from rows or seats.

Demo: generate a small semantic self-play + four-game collection recipe, execute
via `manabot train --regime`, regenerate report offline from its TrainingRun and
content-checked artifacts. Tests cover analytic targets/distances, immutable splits,
complete real games, missing/corrupt evidence, and retained capped-game failures.
No predecessor is removed. Reuse TrainingRun, ArtifactReference, receipt replay and
selection diagnostics; no new execution store. No Rust changes or long runs.

Implementation now provides typed complete-game artifacts, executor collection and
replay, partition-local analysis, external Run checkpoint reuse and report-only
regeneration. The existing censored batch diagnostics remain intact. No static
reconstruction of old campaign rows is attempted. Gate will run affected training
suites and the documented four-game CLI example; CI owns its platform matrix.
