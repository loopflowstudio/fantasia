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

## October 14 result — stopped at failure gate

Full original protocol and diagnosis are preserved at
`3235a5ca48640bb98cf45e410b8a4fb4dcca2445:scratch/search-policy-pilot.md`.
Preregistration was `e256afae`; artifacts remain unchanged in
`.runs/search-policy-pilot-20261014`, owned by its `training.sqlite`.

| Family | Run ID | Wall s | Completed games | Outcome |
|---|---|---:|---:|---|
| Flat | `b1aa85344ba149d39f991d925f89fbd3` | 7.097 | 9 | 4 GiB watchdog; sampled RSS 5,796,560,896 bytes |
| Compound | `6768f0be670a4c3ab0b3dd1bf8519402` | 9.484 | 3 | WrongDecision during game four |

Neither selected a final checkpoint; no arena ran. Flat collected 256 rows per
stream, not per batch: four streams gave 1,024 rows. Compound's 79-Command partial
trace reconstructs an optional sole attacker. Declining advances natively to the
opponent's next-turn attacker declaration; lowering incorrectly continued by
prompt kind alone. Selecting the attacker succeeded; both probes preserved root
state. Failed collection timing was also omitted: 24 tests passed, one timing
regression failed. These were integration failures, not strength evidence.
Exact traces, checksums, cost breakdowns and diagnostic outputs remain bound by
`pilot-evidence.json`, SHA-256
`d88cf719678e243552eb29d09886b49a578e42a6f66dde9b22c5d09ac6c15e69`.
No paid resources were used. The next protocol repaired this boundary/timing and
reduced flat batch demand; no failed attempt was overwritten.

## October 15 second-pilot protocol

Jack Heart resumed the announced repair/rerun sequence. Preregistration/repair
commit `2e9faa29` binds the `search-policy-pilot-20261015-{flat,compound}.json`
recipes and existing-arena driver. Same seed 141001, four iterations each, one
CPU worker/thread, 4 GiB rejection threshold, stage/run watchdogs 300/360 seconds.
Flat: four streams × 64 transitions; compound: two complete games/iteration.
Both: four minibatches, fixed LR/tau, final raw selection. Output root:
`.runs/search-policy-pilot-20261015`. Eight development games on the original two
deal seeds × four deck/seat legs, 60 seconds/4,000 Commands each, 600-second outer
cap; no strength prediction. Total training/evaluation allowance 1,320 seconds.
Both training exports and all replays must succeed; failures stop scale-up.
Complete prospective text remains in the archived note cited above.

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

## w5 declaration repair and preregistered rerun — 2026-10-15

Jack Heart accepted fixing the flat encoder and retraining before comparison.
The repair adds signed declaration polarity to both Python and native action
encoders, bumps WORLD_VERSION to w5 and POLICY_INPUT_VERSION to 2, and excludes
polarity from action-type histograms/references. Old inputs are rejected; no
historical recipe, artifact or result is migrated. Both families initialize fresh.

Question: does the repaired flat input learn either declaration, and do both
fresh w5 policies export, reload and complete exactly replayable games? Predict
both complete under the unchanged second-pilot budgets; no directional win-rate
prediction. Four-iteration training remains integration calibration, not strength.

Executable recipes: `search-policy-pilot-w5-20261015-{flat,compound}.json` in
`experiments/regimes`. Same seed 141001, CPU thread/worker 1, 4 GiB threshold,
300-second stage and 360-second run caps. Flat four streams × 64 transitions,
compound two complete games per iteration, four iterations/four minibatches each.
Both use final raw checkpoints. No learned beliefs. Output root is
`.runs/search-policy-pilot-w5-20261015`, with its own VerifyStore and arena.
After both succeed, run the existing arena driver on the same two development
deals × four legs (eight games), 60 seconds/4,000 Commands per game, outer cap
600 seconds. Training/evaluation total allowance 1,320 seconds. Stop at failure;
no scale-up or strength inference. Commit this protocol and code before training.

Validation so far: 395 debug Rust tests pass. The first broad Python invocation
failed collection for missing optional extras/module-name collision; the corrected
invocation reached 302 passes, 29 failures, one skip and one missing-fixture error
before its 30-failure cap. Most failures use frozen w4 recipes rejected by the
new runtime; the frozen capacity architecture also necessarily changes. These
historical-study test migrations are not a passing full-suite claim. Focused w5
fixtures cover the changed training/arena path. Existing w4 recipes remain intact.

Focused validation: 160 unique tests now pass (156 initially, four repaired
fixture failures plus their 15 neighboring tests rerun successfully). Covers both
encoders, vector buffers, flat/compound learning, checkpoint admission and arena
replay. Exact old flat pilot bytes reject with incompatible w5 binding. Rust
formatting, Ruff and diff whitespace checks pass. Full-suite migration remains
a separate recorded limitation; no historical evidence was rewritten.
