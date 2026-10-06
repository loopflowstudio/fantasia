# Recovering bounded manabot training

Recovery is opt-in for bounded CPU self-play stages, including multistage chains
that retain the latest collector or start a fresh learner. Set `schedule_clock`
to `iteration_fraction` and `recovery_max_microsteps` to an explicit journal
ceiling. Every stage must be `train_self_play`; supervised, compound, collection
and belief-training stages cannot opt into recovery. MPS/CUDA are unsupported.
Ordinary elapsed-time recipes remain unchanged.

```bash
uv run manabot train --regime recipe.json --seed 197 --out .runs/first
uv run manabot train --regime recipe.json --seed 197 --out .runs/continued --resume-from RUN_ID
```

Both output directories must share the same parent so the CLI selects the same
canonical `training.sqlite`. Use a new output directory and the stopped attempt's
stored ID. Only its latest committed boundary can resume, with one recovery
child per attempt. Continue the child after another failure. Completed attempts
cannot resume; an interrupted attempt with every stage completed can finalize
without replaying or exporting those stages again.

## Same-host contract

Private snapshots retain model parameters and buffers, Adam, evaluation EMA,
Python/NumPy/Torch and minibatch/sampling RNGs, native collector state, diagnostics,
collector count baselines, stage-local update progress and run-wide iteration.
Frozen-opponent identity is recipe-bound and its checkpoint digest is rechecked.
The iteration clock continues across linked stages; a fresh stage resets it.
Scientific schedules use the same update coordinates as uninterrupted execution.

Native state is reconstructed from its original seed and bounded action journal,
then every observation buffer is checked. The ceiling counts active environment
microsteps across vector streams, not learner transitions, and applies to the
collector's lifetime across linked stages. This is a bounded correctness path,
not a scalable native snapshot format.

Snapshots are published at stage entry, after each update, and after completed
export/admission. VerifyStore commits the snapshot reference and stage records
together. Completed prefixes retain their original artifact paths, digests,
counts and cost receipts; they are not re-exported into the child directory.
Uncommitted work may repeat, but its failed-attempt cost remains charged. Orphan
files never become authoritative merely because they exist on disk.

Recovery requires the same recipe, seed, source, runtime and host. Changed or
missing snapshot/completed-artifact bytes fail admission. Old source-bound
snapshots are historical evidence, not portable migrations. A local POSIX lease
rejects simultaneous writers; do not remove lease files because replacing the
inode defeats mutual exclusion. Foreign-host recovery and network-filesystem
leases are unsupported. Private snapshots contain hidden state and pickle
objects: never load untrusted files or serve them as model exports.

## Cost and failure semantics

`seconds` measures this attempt; `prior_seconds` charges ancestors once, and
`recovery_seconds` is a subset of this attempt's time. Sum run attempt costs, not
inherited completed-stage receipts a second time. Active-stage phase timings
measure only the current attempt, while counts describe committed scientific
work across retries. Completed stages retain their original receipts unchanged.

The watchdog uses macOS continuous time or Linux boottime, including sleep.
Whole-run allowances charge all prior attempts and reconstruction. Each stage's
watchdog retains its own consumed allowance across retries; a later stage does
not inherit an earlier stage's charge. Restoring an already completed collector
for the next stage charges the run's reconstruction cost without rewriting the
completed stage. Setup and finalization also belong to the run clock.

Caught failures retain measured time. Abrupt process death leaves a running
record; acquiring its saved lease on the same host permits settlement. The
canonical record becomes interrupted while the old `run.json` stays unchanged.
The unobserved calendar interval, including downtime, is conservatively charged
to the run and an active stage. A backwards calendar rejects settlement. These
estimated costs are not measured throughput; recovery assumes a reliable host
calendar and cannot reset an exhausted allowance.

The failure-injection suite compares uninterrupted and resumed learning state,
collector state, schedules, diagnostics and counters across stage entry, update,
completion and terminal boundaries. It also exercises abrupt subprocess exit,
exclusive ownership, incompatible artifacts and budget exhaustion. These are
software-correctness checks, not scientific training or strength evidence.

[ETU-99](https://linear.app/loopflow/issue/ETU-99) owns empirical hardware
calibration, seed/policy timing variation and cohort projections. The active
ETU-91 campaign is unchanged and does not gain recovery retroactively. The
[complete-loop calibration command](training-calibration.md) remains a separate
CPU accounting instrument; no new scientific run is required for this contract.


## Sustained CPU runs: bounded current-game recovery

ETU-118 adds an explicit `recovery` policy on TrainingRegime, separate from the
historical `recovery_max_microsteps` contract. Select only one. The new policy
uses `max_game_microsteps` (default 40,000 across current vector streams) and
`checkpoint_updates` (default 128). It requires current-self collection and
iteration-based schedules. Diagnostic injected roots are unsupported.

Native reset seeds and each unfinished game's legal prefix reconstruct collection;
auto-reset discards the completed game's prefix. Native code owns both the root
seed and subsequent deal stride. Every observation buffer must match before
restored model/Adam/EMA/RNG state resumes learning. Terminal flags describing the
preceding transition are restored separately from the already-reset observation.
Snapshots remain private, source-bound compressed artifacts. Every created
snapshot and failed attempt stays retained; the interval avoids serializing an
unbounded lifetime journal at every update. Committed updates/exports are not
repeated. Work after the latest recovery commit may repeat and its failed-attempt
cost remains charged.

For this opt-in contract, occupied elapsed time while the OS is awake is the
allocation clock. It is not CPU time. macOS/Linux monotonic clocks exclude system
suspend; the historical continuous watchdog stays unchanged for existing recipes.
Saved calendar time and known downtime are separate. A safe pause has a measured
end, so the intervening calendar gap is excluded. After an abrupt owner death on
the same OS boot, the monotonic gap is conservatively charged as **uncertain awake
time** (it can include time after process death); known suspend time is excluded.
After reboot no common monotonic epoch exists: the unobserved calendar gap is
conservatively charged as uncertain, rather than fabricated as measured compute.
This can exhaust the remaining allowance; it never grants a fresh allocation.
Exact active-time attribution across an unobserved reboot is not promised.

ExperimentSchedule selects `active_runtime=True`, requires this recovery policy
for every learner and an active-runtime MonitoringBudget. Isolated workers have
sleep-excluding watchdogs that remain bounded if their supervisor exits. No
sleep-prevention program is used. Retained evaluator crash allowances remain
conservative process charges, not measured throughput.

The Experiment's `pause.request` file requests a pause at the next complete
learning boundary. The learner forces a recovery commit before returning
`TrainingPaused`; the supervisor drains its currently running bounded evaluation
without launching another, then records `paused=true`. Wait for that state before
shutdown if an exact known pause is desired. Explicit `resume=True, recover=(N,)`
continues attempt N before pending later seeds, subtracts consumed allowance and
preserves the original schedule. A failed seed is never silently retried. The
[ETU-118 runner](../experiments/current-baseline.md) exposes CLI controls.

The 2026-10-06 focused checks compare uninterrupted and paused/resumed real native
learning state, optimizer/EMA/RNGs, observations, diagnostics and counts; native
debug tests compare restored reset sequences with independent scalar environments.
Clock fault injection tests accounting, not physical lid closure or a host reboot.
