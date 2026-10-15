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

## Result — stopped at the preregistered failure gate

Preregistration commit: `e256afae6ec5f6b143014e15f6d05ca41556b841`.
Both runs failed; neither selected a final checkpoint. The eight-game arena did
not run. No strength, win-rate, or compute-matched treatment claim follows.
Neither the main training cohort nor the search cohort launched.

| Recipe | Run ID | Run seconds | Completed games | Learner rows / exposures | Sampled peak RSS | Outcome |
|---|---|---:|---:|---:|---:|---|
| Flat | `b1aa85344ba149d39f991d925f89fbd3` | 7.097 | 9 | 1,024 / 1,024 | 5,796,560,896 bytes | Memory watchdog after first update |
| Compound | `6768f0be670a4c3ab0b3dd1bf8519402` | 9.484 | 3 | 482 / 366 | 3,091,234,816 bytes | Command lowering failed in fourth game |

Source: authoritative VerifyStore rows in
`.runs/search-policy-pilot-20261014/training.sqlite`, retrieved by these IDs.
Total recorded training-run wall time: 16.581 seconds; stage CPU time:
6.872 + 9.421 seconds. Native build reported 12.83 seconds separately. Setup,
probes and tests are not training time. RSS is sampled once per second, so the
4 GiB rejection threshold is not a hard instantaneous limit. No paid resources.

### Flat batch semantics

The prospective phrase “256 transitions over four streams” was underspecified:
the implementation collects **256 per stream**, hence 1,024 learner rows per
iteration. The receipt records one optimizer update, 2,189 environment decisions,
3.691 seconds collection and 1.383 seconds learning before rejection. Reducing the
batch and/or increasing minibatches is a candidate repair, not yet tested. Do not
silently increase the memory cap or reinterpret these rows as 256.

### Compound continuation boundary

The three completed games replayed exactly. Replaying the 79 Commands retained
in `compound/fit-game-3.jsonl` reconstructs revision 80, actor 0, with one optional
attacker, Compassionate Healer. Post-failure diagnostics separated an unsupported
prompt from a continuation-boundary defect:

- Selecting the attacker lowers to one canonical Command successfully.
- Selecting no attackers raises `PyAgentError: current decision has no structured
  offer support`. Both lowering attempts leave the root digest unchanged.
- Executing the native decline action directly succeeds and advances to **actor
  1's** attacker declaration (First-Time Flyer). Automatic trivial steps skipped
  the intervening windows.

This matches `managym/src/agent/structured_offer.rs`,
`apply_legacy_command_inner`, `AtomicCommand::DeclareAttackers`: the loop continues
while the prompt kind is DeclareAttacker, then rejects a changed actor. The
declaration boundary must account for native advancement, not merely prompt kind.
A repair must also distinguish later declarations by the same actor; changing
only the actor check is not a complete demonstrated solution.

These are exploratory diagnostics, not preregistered strength evidence. Outputs:
`compound/failed-root.json` and `compound/lowering-probe.json`. The failed sampled
submission was not itself logged; testing both legal subsets isolates the failing
option without claiming a recorded model token trace.

The three successful games contain 372 compound decisions, 482 factors and 412
canonical Commands. One optimizer batch consumed 366 factors from the first two
games; the third game was collected for the next batch before failure. These units
are not interchangeable with flat transitions/exposures.

### Existing checks and timing limitation

The existing compound test module plus the two analytic local-update tests yielded
**24 passed, 1 failed in 2.05 seconds**. The failure is
`tests/training/test_compound.py::test_failed_regime_registers_incomplete_attempt_without_checkpoint`:
it expects positive failed-collection time but observes zero. The compound branch
of `manabot/training/execution.py` adds collection elapsed time only after success;
the exception path bypasses it. Consequently compound collection time (1.872 s)
excludes the failed fourth game. Total run time retains this cost. Do not price
failed attempts from collection time alone. Raw output: `tests.log`.

### Evidence and next execution boundary

Both recipes were validated. Dependencies were installed with
`uv sync --frozen --python 3.12 --extra dev --extra play`; native bindings were
built from this checkout. Engine source SHA-256:
`586453419d1db9b85d11e3f89cf739d52dc1b7e8831684baf72f72d1b4758138`.
The local `pilot-evidence.json` binds identities, run exports, logs, traces and
diagnostics by SHA-256; its digest is
`d88cf719678e243552eb29d09886b49a578e42a6f66dde9b22c5d09ac6c15e69`.
Artifacts remain local and private; a path alone does not transfer them.

The pilot answered the integration question negatively and hit its stop condition.
Keep both attempts unchanged. Before a newly preregistered pilot: repair and
regression-test declaration lowering at this exact boundary, account for failed
collection time, and reduce flat batch memory demand. Only then admit a fresh
pair and the eight-game comparison. ETU-118 retrieval, recursive action-reference
implementation, and compound-aware PUCT admission remain distinct prerequisites
for later search cells. No production source was changed during this pilot.
