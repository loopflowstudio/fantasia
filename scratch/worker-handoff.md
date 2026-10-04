# ETU-89 / ETU-90 / ETU-91 worker handoff

Jack Heart directed three workers on 2026-10-04, superseding the prior single
writer. The preserved implementation checkpoint is
`38c164ebc03f01a3a1f312f0198e33dbef154f2f` (parent
`3f2975334e6fa2f1a36683d3686a7ecc2d68ffe9`). Runtime `.lf/tmp`, generated `.runs`,
native binaries and local orchestration files are excluded. No publication or
landing occurred. The coordinating session owns creating the stacked checkouts
and launching ETU-90 and ETU-91 workers. ETU-89 continues infrastructure only.

## File and API ownership

- **ETU-89:** `manabot/training/models.py`, `execution.py`, `__init__.py`,
  `manabot/cli.py`, `manabot/verify/store.py`,
  `manabot/sim/search_supervised.py`, `manabot/sim/distill.py` (collection
  deadline/termination metadata and ordinary artifact integration),
  `docs/training-regimes.md`, `tests/training/test_regimes.py`,
  `tests/sim/test_search_supervised.py`. Own schema validation, explicit stage
  references, persistence/exports, phase costs, budgets, continuation and
  ETU-75 checkpoint-contract integration. Existing `test_named_treatments...`
  in the infrastructure test file is retained; ETU-90 should add its independent
  tests in a separate file rather than edit this shared file.
- **ETU-90:** `manabot/training/objectives.py`, `manabot/sim/net_opponent.py`,
  `managym/src/agent/vector_env.rs`,
  `managym/src/python/vector_env_bindings.rs`,
  `tests/sim/test_net_opponent.py`, and new focused RL tests.
  Own pause/terminal/next-state correctness, full behavior distributions,
  estimators/filter/KL/schedules, and EMA correctness. ETU-89 will consume their
  API; changes needed to infrastructure-owned configuration or EMA wiring
  should be coordinated explicitly rather than edited concurrently.
- **ETU-91:** `experiments/regimes/*.json`,
  `experiments/runners/run_training_regimes.py`, `training_protocol.py`,
  `manabot/training/analysis.py`,
  `experiments/study/training-regimes.ipynb`,
  `experiments/training-regimes.md`, `ataraxos-mtg-ablations.md`,
  `training-regime-followups.md`, study evidence/report artifacts and new study
  tests. Own notebook dependencies in `pyproject.toml`/`uv.lock` if needed.
  The regime files already contain main recipes, five core arms, and named
  horizon/reference/filter/KL/EMA contrasts. Do not silently turn pilot counts
  into the draft expensive experiment.

Shared interfaces at the checkpoint:

- `validate_regime(regime)`; `execute_regime(regime, seed, out, store)` creates a
  new directory and returns a `TrainingRun`; `export_training_run(id, store,
  out)` derives JSON from VerifyStore. Three operation variants are
  `CollectSearch`, `TrainSupervised`, `TrainSelfPlay`. Each stage ID names its
  output. Supervised datasets and initial references must point backwards;
  live self-play continuation cannot branch from an older collector.
- `SeatRoutedCollector.collect(agent, num_steps, deadline_monotonic=None)`
  returns end-marker batches, full legal behavior probabilities and exact
  `next_obs`. No in-flight action or surplus row crosses the update boundary.
  Native `step_into_buffers(actions, active=None)` preserves paused tensor rows
  and clears their transient step outputs.
- `transition_gae(rewards, values, ends, next_value, gamma, lam)` handles
  transition-end flags. `update_iteration(trainer, batch, learning, progress,
  rng)` uses the existing trainer/Adam and returns diagnostics/exposure counts.
  The executor currently owns the EMA parameter interpolation once per
  collect/update iteration; ETU-90 should propose a tested helper if moving it.
- `train_search_supervised(..., optimizer_state=None, validation_games=None,
  continuation=None)` preserves its four-item result for existing callers;
  optional `continuation` receives Adam state. Explicit whole-game partitions
  cannot be empty. IDs divisible by ten are validation in regime execution.
- `generate_selfplay_shard(..., deadline_monotonic=None)` now reports
  `terminated` and `truncated` separately. Incomplete teacher games are retained
  and rejected by the executor, not counted as authoritative draws.

## Separate evidence and limits

- **ETU-89:** both main recipes completed multi-stage execution with ordinary
  checkpoint reload in `.runs/regime-smoke-1`, including two cumulative
  supervised rounds and two self-play checkpoints. Schema/store/deadline tests
  passed; a later source-hash path bug was fixed and its deadline test passed.
- **ETU-90:** six Python collector/credit tests passed initially; expanded
  collector/supervised/infrastructure suite subsequently passed 22 tests with
  only the source-hash path failure above. Six native vector tests pass in
  debug, including pause preservation with an invalid inactive action.
  Named treatments executed finite optimizer fixtures. EMA lacks a focused
  clock/identity proof; arbitrary device execution is intentionally not certified.
- **ETU-91:** `.runs/regime-smoke-1` completed in 72.29 seconds with 8 games
  (two four-leg paired comparisons), both checkpoint measurements, exact replay
  and an executed notebook. `.runs/ablation-smoke-1` completed in 222.37 seconds
  with all five arms, two checkpoints, 72 arena games (paired control plus fixed
  random anchor), exact replay and an executed notebook. These directories are
  local generated evidence, not committed. Preserve/copy relevant results into
  the new checkout as needed; no synthetic reconstruction. The first learning
  smoke predates fixed-anchor additions. Both smokes predate the final protocol
  file, setup-cost, termination-metadata and source-hash refinements; rerun final
  acceptance on the integrated world. Regeneration was not yet checked for
  unchanged metrics. No scientific strength or human-play result is claimed.

## Integration still required

ETU-75 changes are not in this checkpoint. Its directed contract is
`checkpoint_world(player_configs, observation_space)` and
`validate_checkpoint_world(checkpoint, observation_space, player_configs=None)`
in `manabot/model/world.py`. Ordinary `save_bc_checkpoint` will require the
actual deck/sideboard `player_configs`; selected-match recipes must set
`AgentHypers(semantic_pack="ur-lessons-vs-gw-allies")`. It adds `semantic_cards`
and `known_hand` tensor keys and remains native w4. ETU-89 owns consuming this
shared contract after sync; ETU-90 must preserve complete tensor propagation,
and ETU-91 must rerun studies against the final schema. Do not create a second
checkpoint binding or call the provisional current smoke final-world evidence.

Before handoff, all edited Python files compiled. No expensive run, paid compute,
external task mutation or additional worker was launched here. The remaining
validation is Task-specific, then integration/queue checks once on the final
stack. Preserve failed attempts and describe unavailable measurements honestly.


## ETU-89 infrastructure follow-up

ETU-89 retained startup/export failures, input artifact digest checks, rejected
checkpoint identities, explicit resolved trainer/policy/precision settings,
whole-run elapsed-budget schedules across continuation, sampled memory/CPU
receipts, and a selected raw artifact. Run payloads now derive their stage list
from the stage table, avoiding duplicate writable stage state. Supervised Adam
continuation uses the newly declared LR and a separately named minibatch seed.
Generated `.lf/tmp/context` accidentally published by the coordinator is removed
from the index and `.lf/tmp/` is ignored; the local file remains available.

ETU-90 requested a tested `update_ema(averaged, learner, rate)` helper; its
commit is pending. ETU-89 will replace only the executor interpolation when
that helper is available. ETU-75 has not published its ordinary checkpoint
contract on current main; final integration/acceptance and landing remain
pending that shared owner. No child-owned files were edited after handoff.

Check result: 2026-10-04 infrastructure-only tests passed 11 tests; the preceding
combined infrastructure/supervised run passed 21 tests. Final-world real execution
and final gate await ETU-75; ETU-90/91 retain their separate acceptance ownership.
