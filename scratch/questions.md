# Research assumptions — 2026-10-14

- Accepted direction from Jack Heart: no learned beliefs in this experiment set.
  Every search arm uses the physical-compatible deal prior. Proposed policies
  are ETU-118 final raw 10,000-update seeds 11851–11853, with seed 11851 for the
  pilot, pending exact artifact and semantic admission. Subsequent direction adds
  compound-policy training and comparison with non-compound policies as a subgoal;
  its main run budget remains unset. No belief training is
  selected. Recursive uniformity is an action reference, not a hidden-world model.

- The assigned parallel contribution is this checkout's MMD search family. The
  handoff selects one bounded pass; no additional agents or Tasks are needed.
- “Current selection” is ambiguous now that local search already implements full
  MMD. Compare the existing local selector as an identity control, and a clearly
  named Q-argmax control on identical local evidence. Keep actual flat/PUCT players
  as separate evidence-generator strata; do not call their different traces a
  matched root-update comparison.
- Exact Task reads report disconnected sync and stale planning. Use their cached
  descriptions as historical evidence, with repository code/receipts as the
  substantive evidence. The manifest's `.lf/wave/intelligence` directory is absent;
  the supplied brief/handoff suffice. Do not repair planning or expand scope.
- The initial research-only environment restriction is superseded by Jack Heart's
  subsequent instruction, “lets pursue the experiments.” Execute the bounded local
  calibration in `scratch/search-policy-pilot.md`; main-cohort allocation remains
  separate. Dependencies and native bindings may be built in this checkout.
- Reversible execution assumption: begin with one fresh CPU training pair and a
  development arena, with no paid resources or learned beliefs. Existing ETU-118
  artifacts are not at `/Users/jack/src/etude/.runs/etu118-mini-20261007-1` on this
  host; do not substitute fresh checkpoints for that frozen benchmark.
- The bounded pair has now executed and both attempts failed. See
  `scratch/search-policy-pilot.md` for receipts and the exact compound declaration
  boundary reproduction. Its failure gate stopped arena and scale-up. No final
  pilot checkpoints, strength results, or win-rate estimates exist.
- October 15 resumption assumption: “computer is back” continues the announced
  repair-and-rerun sequence. Make the bounded correctness/timing repairs and run
  a newly preregistered pilot with smaller batches; leave the failed attempts
  unchanged. Main-cohort compute remains unallocated.
- The October 15 repaired pilot completed: both final raw checkpoints exported,
  eight paired arena games finished and replayed, with a 4–4 development score.
  This supersedes the missing-pilot-checkpoint gap for the new attempts only;
  ETU-118 access and main search/training prerequisites remain unresolved.
- Additional admission blocker: flat action encoding drops attack/decline's
  `declared` flag. Confirmed on the exact pilot checkpoint as identical logits and
  50/50 probabilities. Repair/version the input contract and retrain before a
  fair flat-versus-compound strength comparison; preserve the pilot as integration
  evidence only. See the diagnostic in `scratch/search-policy-pilot.md`.

## Pre-execution limit for a mathematical probe

One offline `uv run --no-project --python 3.12 python` process, standard library
only, at most 10 seconds (SIGALRM), one process, no GPU/network/training/engine
execution, no artifact/checkpoint reads. Evaluate five fixed algebraic fixtures
plus a 1,001-point two-action objective grid. Print only results and measured
process/wall seconds. This checks the derivation, not the production NumPy code.
If the offline interpreter is unavailable, stop the probe without installation.
