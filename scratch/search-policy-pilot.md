# Search policy calibration — 2026-10-14

Jack Heart accepted compound-policy training and comparison with non-compound
policies, then requested “lets pursue the experiments.” This supersedes the
initial research-only execution boundary for this bounded pilot. No paid resources,
learned beliefs, publication, or changes to existing experiments are selected.

## Preregistered question and decision

Can both existing training paths produce reloadable w4 policies, and can the
ordinary arena compare them through complete, exactly replayable games at local
CPU cost? This is a cost/integration pilot, not a representation or strength test.

Predict: both runs complete four optimizer iterations within 300 seconds each;
the compound run completes and replays all eight collected games; both exported
policies complete and replay all eight development arena games without an illegal
action or boundary failure. There is no directional win-rate prediction at this
training scale. A failed run or game prevents scale-up; preserve its artifacts.

## Frozen small allocation

- One sequential pair, seed 141001 for both, separate fresh initializations.
  `experiments/regimes/search-policy-pilot-flat.json` and
  `experiments/regimes/search-policy-pilot-compound.json` are the
  executable TrainingRegimes. One CPU worker/thread, 4 GiB process cap, 300-second
  stage watchdog and 360-second run cap each. No GPU or external service.
- Same w4 curated main decks/sideboards, observation limits, 64-dimensional
  semantic encoder, PPO, constant LR .00025 and tau .01, gamma/lambdas 1,
  one epoch, one minibatch, no filtering or EMA, final raw checkpoint only.
- Flat: four updates of 256 transitions over four streams. Compound: four
  updates of two complete games, sequential factor credit, terminal-outcome
  estimator, 4,000 Commands/game maximum. Same update count is a calibration
  convenience, **not matched compute** or matched target semantics.
- If both runs complete, compare compound versus flat with the existing arena
  `play_cell`, stochastic checkpoint players, deal seeds 1910141001 and
  1910141002, four deck/seat legs each. Eight development games, 60 seconds/game,
  4,000 Commands/game, replay every game. Outer evaluation cap 600 seconds.
- Training plus evaluation caps total 1,320 seconds; allow at most another
  300 seconds for relevant existing tests. Native build is preparation and
  measured separately. Stop on caps; no automatic longer retries.

Use existing `execute_regime`/VerifyStore and arena instruments. Save training
runs in `.runs/search-policy-pilot-20261014/{flat,compound}`, store in its
`training.sqlite`, and arena evidence in its `arena` subdirectory. Keep the
recipes and this protocol in git before training. Preserve source, native,
world, input, checkpoint, seed and parameter-count identities in run receipts.

## Interpretation and next experiments

The strongest confound is learning semantics: truncated transition PPO and
complete-game factor PPO differ in sample units, targets, regularization, and
parameter count. This pilot calibrates two recipes; it cannot isolate compound
representation. Use measured collection/learning/replay time to size the later
three-seed-pair comparison before launching it. Do not select seeds from results.

The search sequence remains shared-root KL-only / offer-uniform MMD /
recursive-uniform MMD, then raw-policy and PUCT game comparisons at measured
compute. All search uses the physical-compatible deal prior. Recursive reference
and compound-aware PUCT require their own verified adapters; neither is silently
replaced by a flat reference/head. This pilot does not assert they are available.
ETU-118 remains the intended frozen practical benchmark, pending artifact access
and current-world admission. No ETU-118 win-rate result can come from this pilot.
