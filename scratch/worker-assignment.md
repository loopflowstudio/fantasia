# ETU-90 independent worker assignment

Jack Heart requested THREE workers on 2026-10-04. This supersedes all earlier sole-writer instructions in scratch or historical comments. ETU-89, ETU-90 and ETU-91 now have separate checkouts. Current Task: ETU-90, direct-RL correctness and Ataraxos training techniques. Do not redo kickoff or the already-written implementation from scratch.

Read worker-handoff.md for the preserved checkpoint, real evidence and exact API/file ownership. Own objectives.py, net_opponent.py, native paused-vector collection and focused RL tests. Independently inspect the inherited implementation, fix actual correctness gaps, and complete the Task's specific proofs (including terminal/boundary credit, behavior-policy identity, reference support/normalization, filtering, estimator distinctions and EMA clocks). Add RL tests in a separate file, not infrastructure test_regimes.py. Coordinate necessary config/EMA wiring changes with ETU-89 using lf task comment --steer; ETU-89 owns models.py and execution.py. Do not silently edit ETU-91 study files.

The checkout is stacked on ETU-89 / PR #200. Preserve that dependency; use lf for sync and delivery. ETU-91 is a sibling worker consuming this contract and must integrate the final RL changes before final study acceptance. Send concrete API/schema changes to ETU-89 and ETU-91, never routine progress comments. ETU-75 owns ordinary checkpoint semantic/world admission; preserve all new tensor keys.

Run pursue-auto headlessly through focused verification, sync/realign, gate, publication and landing. Jack authorized these external effects; no interactive reviews or additional workers are required. Do not claim strength from tiny runs. No paid compute or week-long training. Complete only acceptance actually met, and preserve failed/incomplete evidence. Exclude generated .lf/tmp context and orchestration artifacts from your authored diff; parent cleanup is separately directed. If checks reveal the inherited implementation already satisfies an item, record that evidence rather than manufacture a patch. Finish the real remaining code and validation for this Task.

## Implementation evidence (2026-10-04)

Checkpoint `8076e877` adds independent estimator/reference/filter/KL/EMA proofs,
real collection-policy and exact bootstrap identity checks after a weight
change, a bounded two-stage TrainingRun reload test, and resolved treatment
and selection diagnostics. The inherited terminal/pause implementation passed
inspection and focused tests; no duplicate collector was introduced.

`update_ema(averaged, learner, rate)` averages parameters and copies buffers.
ETU-89 received the concrete helper and wiring request; execution.py still has
its inherited parameter interpolation in this checkout. Parent integration
must connect the helper and verify the continuation schedule clock. The executor
currently uses elapsed whole-run time divided by the regime budget; it does not
reset progress per stage. ETU-91
received the diagnostic keys and final integration requirement. The selected
match must survive the ordinary trainer shim for ETU-75 save admission.

Check result: 24 focused Python tests, 6 native debug vector tests, and the
bounded runtime reload test passed; Ruff passed on all four authored files.
The retained `.runs/rl-proof-2` execution completed 14 games and 1,024 learner
transitions across two stages in 2.31 s, with distinct raw/EMA artifacts,
positive phase costs and the exact second-stage EMA recurrence. This is
inherited-ABI workflow evidence, not learning strength or final-world admission.

Two initial test attempts exposed fixture mistakes (a tensor view needing
explicit detach and checkpoint metadata stored under `bc`); both were fixed.
The retained-output attempt `.runs/rl-proof-1` failed before training because
its parent output directory did not exist; `.runs/rl-proof-2` is the successful
retained attempt. No expensive run or paid compute occurred.

Compression and local plan/memory reconciliation are complete. Remaining delivery
work is parent integration including ETU-75 admission, affected-suite gate and
publication/landing.
Do not claim final Task acceptance before rerunning the runtime proof on the
integrated checkpoint contract. Full study acceptance belongs to ETU-91.

Compression completed: structured-reference counts now use a per-type histogram
instead of an offers-by-offers matrix; the collector has one transition
finalization point per next learner observation. Corrected its stale stock-GAE
description. No public API or diagnostic keys changed. The plan's obsolete
end-flag GAE use and surplus-transition banking are already removed.

Check result: `uv run pytest tests/training/test_rl_objectives.py tests/sim/test_net_opponent.py -q`
passed 24 tests; Ruff and diff whitespace checks passed. Parent sync, EMA helper
wiring, continuation schedule clock and final-world reload remain for ETU-89
integration and the later gate; no native code changed in compression.

Reconciliation check: `lf task sync --plan` reported `noop` on 2026-10-04; source inspection confirms the EMA wiring and final-world admission gaps remain. Prior focused checks are reused; no tests were rerun for documentation-only reconciliation.

Gate result (2026-10-04): `uv run pytest tests/training tests/sim/test_net_opponent.py tests/model/test_train.py -q` passed 44 tests (4.37 s); `cargo test --manifest-path managym/Cargo.toml vector_env --lib` passed six debug tests; Ruff on the five RL implementation/test files and `git diff --check` passed. The runtime test includes real two-stage self-play, phase costs and ordinary raw/EMA reload. No Rust edits required a rebuild in this gate.

Parent integration resumed on 2026-10-04. ETU-90 ready head is 73033266:
d49966f8 preserves collector.match through Trainer.env.match and all tensor
shapes; 73033266 adds real empty-filter continuation proof (learner unchanged,
zero optimizer exposure, EMA advances). Complete-state update_ema is inherited
from 8076e877. ETU-89 integrated these contracts with ETU-75 aba61859 and semantic
recipes at local 9a1b90df; it reports 66 passing checks/one study skip and a
retained semantic 14-game/1,024-transition run with four raw/EMA reloads.

Final integration (2026-10-04): `lf task sync` consumed published parent
9a1b90df and resolved the Wave-memory conflict at af9a7ad1. Rebuilt native
extension; 65 affected Python tests passed, one notebook test skipped because
nbclient is unavailable; six debug vector tests and Ruff passed. Explicit
semantic artifact assertions then passed both retained runtime cases (7.14 s).
Each case completed 14 games/1,024 transitions with four ordinary raw/EMA
reloads. `.runs/etu90-semantic-final` retains the run records and artifacts.
The empty-filter continuation had zero optimizer exposures and fixed learner
weights, with EMA advancing. No scientific training ran. Parent PR200 remains
owned by root; publish the child and request landing after its dependency.
