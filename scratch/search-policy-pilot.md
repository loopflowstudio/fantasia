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

## Resumption and second pilot — preregistered 2026-10-15

Jack Heart reported the computer available again. Continue the stated repair and
rerun sequence here; preserve the October 14 attempts. The narrow repairs bind
attacker lowering to the original declaration batch and charge collection time
even when collection/replay fails. A native regression covers both another actor's
next declaration and the same actor's next-turn declaration. Before repair it
reproduced WrongDecision; both boundaries must pass after repair. Replay the
retained failed root as well as existing regressions. No new game rules or policy
interface are selected.

New recipes: `experiments/regimes/search-policy-pilot-20261015-{flat,compound}.json`.
New output root: `.runs/search-policy-pilot-20261015`. Each retains seed 141001,
four training iterations, single CPU worker/thread, 4 GiB memory rejection
threshold, 300-second stage / 360-second run watchdog, and last-complete-raw
selection. Flat now uses 64 transitions **per stream** × four streams = 256
rows/iteration. Both use four minibatches per epoch. Compound still collects two
complete games/iteration; its complete-game targets are unchanged. These changes
are development recipe adjustments, not an isolated representation contrast.

Predict both final raw exports will be produced under the unchanged memory/time
limits, all eight compound training games will replay, and the two exports will
complete and replay eight development arena games. Use the same two reserved deal
seeds and four deck/seat legs as originally specified. The thin
`experiments/runners/search_policy_pilot.py` driver reads VerifyStore, verifies
bytes/runtime, records registrations, and calls the existing `play_cell`; it
introduces no new policy or game execution implementation. Per-game cap remains
60 seconds / 4,000 Commands; outer evaluation cap 600 seconds. Retain all failures
and do not run arena unless both training runs complete. No strength prediction.

Total training/evaluation watchdog allowance remains 1,320 seconds for this new
pair; repairs/builds/tests are preparation, not charged as training. Run debug
Rust and relevant Python checks before training. No paid resources, learned
beliefs, ETU-118 substitution, main cohort, or search scale-up is selected here.

## Second pilot result — completed 2026-10-15

Preregistration and repair commit: `2e9faa29` (full source identity in each run).
Both runs completed and exported final raw checkpoints. All eight compound
training games replayed during collection. The paired arena completed all eight
games and replayed all **1,140 Commands**, with zero recorded integrity or replay
mismatches. Its development score was **compound 4, flat 4**. Two deals, one
training seed, four iterations and unequal training costs do not estimate a
method's strength or establish equivalence.

| Recipe | Run ID | Run wall seconds | Stage CPU seconds | Sampled peak RSS | Final parameters |
|---|---|---:|---:|---:|---:|
| Flat | `390e13ae273c45a89ef0f3bbe5b7c788` | 5.470 | 5.430 | 751,255,552 bytes | 138,434 |
| Compound | `6035e82ec9f74284aa88120d30f995d7` | 46.593 | 46.411 | 1,993,441,280 bytes | 180,422 |

The flat run collected nine completed games, 1,024 learner rows and 1,024 optimizer
exposures across four iterations (16 minibatch optimizer steps). Collection took
3.551 seconds and learning 1.389 seconds. The compound run collected eight games,
1,805 Commands, 2,050 factor rows and 2,050 optimizer exposures. Collection plus
replay took 9.281 seconds and learning 36.811 seconds. The different work units,
parameter counts and estimators remain confounds; an update is not a compute unit.
The full arena driver took 18.483 seconds, including 1.197 seconds for replay.
Total training-run plus arena wall time was 70.545 seconds, within the allocation.

Final raw checkpoint identities:

- Flat: `flat/fit-raw.pt`, SHA-256
  `02af43435df44a24de4b301c6a4bed099fc151f452a2c5b47643e71b2b71a40d`.
- Compound: `compound/fit-raw.pt`, SHA-256
  `022af12801debb3aedde99f5c89f46b5469e2ebcdc77e04e412b301bce565dc9`.

Paths above are relative to `.runs/search-policy-pilot-20261015`. Its
`training.sqlite` owns run records; `arena/protocol.json` binds the admitted
checkpoint players, `arena/rows.json` holds game outcomes, and
`arena/traces/pilot-compound__pilot-flat.commands.jsonl.gz` retains Commands.
`pilot-evidence.json` binds the local artifacts and run identities; manifest SHA-256:
`56b1cdb8f68070c6610f159a0ceabe4efdaa92f9b5de5fdae8f1f89dc460198d`.
New engine source SHA-256:
`5ad56a72608b5679e5da5f178358009d3a84d1cb621ca72b297afd576120df95`.
No original artifact was rewritten or relabeled under this identity.

Repair validation: the new native regression failed before the repair and passed
after it, covering both opponent and same-actor later declarations. The three
original complete game traces replayed (106, 217 and 89 Commands), as did the
79-Command failed prefix. Both legal root submissions now lower to one Command
without mutating the root; see `original-reproduction.json`. All **394 debug Rust
tests** and **57 relevant Python tests** passed. The learned-search test was
explicitly deselected; no learned belief fitting was run. Ruff and Rust formatting
checks passed. Failed-collection timing is now included and its existing regression
passes.

This closes the repaired integration/cost pilot, not the main search experiment.
The larger paired training comparison still needs a frozen compute allocation and
recipe. Recursive action-reference and compound-aware PUCT admission, plus exact
ETU-118 artifact access, remain the recorded prerequisites for their search cells.
The two new checkpoints are development artifacts and must not be described as
strength-trained replacements for ETU-118.

## Flat attack-action aliasing — confirmed 2026-10-15

Jack Heart raised a reported flat-policy attack/decline bug after the pilot. Code
inspection confirms that `Observation::for_player` preserves `declared=true/false`,
but both `manabot/env/observation.py::_encode_actions` and native
`observation_encoder.rs::encode_actions` omit it. Both choices have the same
DeclareAttacker type and the same permanent focus. `Agent._gather_informed_actions`
and the shared per-row policy head therefore assign identical logits, regardless
of trained weights. The ordinary stochastic flat policy cannot learn an attack
preference at this binary prompt: it produces 50/50. This is distinct from the
compound Command-lowering bug repaired above.

A read-only, one-thread, 30-second-capped probe loaded the exact final flat
checkpoint and replayed the first arena game's prefix. At decision index 20,
match `search-policy-calibration-20261015:pilot-compound__pilot-flat:1910141001:0`,
the flat player's raw options have `declared=[true,false]` and focus `[93]` for
both. Encoded action and focus rows are exactly equal. Both logits are
`0.0017222746973857284`, yielding probabilities `[0.5,0.5]`.

The compound decoder has separate include/exclude logits and does not share this
particular alias. The eight-game 4–4 score remains an accurate record of what ran,
and the integration/replay result stands, but the current flat arm cannot support
a fair representation/strength comparison. Correct and version the flat input
contract, add a distinguishing-action regression, and retrain before selecting
it for that comparison. More training on the existing encoding cannot fix this.
Historical ETU-118 checkpoints need an explicit encoding audit; do not assume a
new encoder can be applied to their bytes unchanged. No code or artifact bytes
were changed by this diagnostic.
