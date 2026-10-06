# Current baseline: sustained trajectory, then a daily regression test

Jack Heart revised ETU-118 on 2026-10-06: WEEKLY → DAILY. This supersedes the
original positive-control-first completion framing. Jack Heart subsequently authorized a week on the current laptop, then required
sleep/restart recovery and checkpoint-safe pause/resume before launch. No recipe
is validated yet. The allocation is at most seven active days, with known downtime and conservative
unknown restart charges separate. Storage admission currently blocks launch.

## Accepted outcome and order

1. Retain cheap engine-backed positive controls as debugging prerequisites only.
   Use real viewer observations, ordinary policy/learner, reload and evaluator,
   initialization and no-update controls. Never label their pass the baseline.
2. Establish a serious sustained, instrumented learning trajectory: fixed recipe,
   multiple independent seeds, fixed greedy plus random evaluation anchors,
   intermediate checkpoints, exact world/source/configuration/checkpoint bindings,
   complete failures and costs. Select hardware, horizon and explicit budget from
   calibration before launch; do not choose the recipe for fast early gains.
3. Demonstrate sustained improvement with uncertainty and honest plateaus or
   regressions before promoting a versioned current baseline.
4. Derive the shortest reproducible daily test from that established trajectory.
   Validate its relationship to longer outcomes and test relevant regressions;
   early learning speed or a toy task cannot establish predictive validity.
5. Publish runnable Experiment definitions, shared execution, editable notebook
   and concise read-only HTML. Software/debugging delivery cannot complete ETU-118.

## Candidate and coordination

The candidate is the unchanged masked-mean scalar recipe from the first value-model
screen (400→800 updates improved fixed-greedy score in three seeds). The later
pooling/filter follow-up was flat. These are candidate evidence, not validation.
Keep architecture/learning fixed; distinguish any opponent or source migration.
ETU-116 owns overlapping total-step dynamics on the mini after ETU-103. Its
planning item had no registered execution when inspected; an ordinary contribution
request failed without starting work. An earlier proposal to consume only its
trajectory is superseded by Jack Heart's explicit laptop authorization for ETU-118.
Share compatible definitions and evidence; do not duplicate its long run merely
for the same question or alter the reserved mini sequence. The laptop study owns
baseline and daily-test acceptance; mini results can inform it with host/cost
and protocol differences kept explicit.

## Sustained allocation and recovery prerequisite

Jack Heart authorized the current laptop, no paid provisioning, one learner CPU
thread and one bounded evaluator. Select three independent seed horizons from
exact-recipe measured throughput, reserve evaluation/reporting and recovery within
the single allocation, and retain every failed/interrupted attempt. No automatic
fresh-week restart. Calibration remains bounded; the short full-game timing is
not calibration of current-self learning.

Reconciled 2026-10-06 against `b4b9913e`: the opt-in recovery path now bounds
native replay to each stream's current game and preserves learner/Adam/EMA,
RNGs, counters, schedules and committed exports. The candidate checkpoints every
128 updates, at stage completion and on a requested pause. Work after the last
committed snapshot can repeat; committed updates and exports cannot. The canonical
store and original source/recipe retain recovery authority.

Active-clock accounting separates known downtime and conservatively charges
unobserved restart intervals, including reboot gaps. These estimates are not
measured compute. Bounded interruption, continuation and complete-state equality
checks passed; physical lid closure remains untested. Existing wall-clock recipes
retain their original semantics.

The shared dashboard exposes update/evaluation freshness, checkpoint lag,
throughput, costs, failures and strength uncertainty. Manual pause commits a
learner boundary and waits for the current bounded evaluation cohort. No automatic
statistical plateau rule exists. Main's progress-export throttling is integrated;
it does not replace recovery checkpoints or eliminate snapshot duplication.

The remaining launch prerequisite is retained-storage admission followed by a
complete exact-recipe calibration, not another implementation of recovery.

## Existing work preserved

`experiments/current-baseline.md` and frozen JSONs own the original debugging
protocols. The lethal-target root keeps the authored Allies/Lessons catalog,
varies UR seat and visible life/mana, and uses real terminal rewards. Custom
subsets had incompatible native semantic IDs and were rejected before scoring.
A root-preparation failure at native Discard was retained (52.37 s); explicit
fresh full-cohort recovery charged it once. Three recovered learning seeds each
went from 50% to 100%, with frozen controls unchanged and 1,152 exact-replayed
root evaluations (137.39 s). This is a narrow debugging pass only.

The 128-update fixed-random full-game cohort completed within its 2,700-second
cap: 432 exact-replayed games, 2028.40 seconds, paired gains +6.25/+8.33/+6.25
points. Mean +6.94 failed the predeclared +10-point debugging criterion. Frozen
controls matched. No threshold was weakened; neither this result nor its timing
can establish or calibrate sustained current-self strength. All 27 JSON receipts
are hash-bound in the published debugging bundle; full private evidence remains
in the original `.runs` directories.

## Implementation and remaining work

One ordinary SeatRoutedCollector/Ataraxos learner owns updates. A native-root
buffer implementation supplies diagnostic terminal transitions; full games use
the original vector environment. Experiment resolves recipes; TrainingRun and
VerifyStore retain execution authority. The explicit diagnostic driver adds
initialization/no-update controls and root replay. The sustained run must use
the shared Experiment scheduling/notebook path and its phase accounting.

Short full-game thresholds and outcomes remain debugging criteria. The executor and
report share typed Result/Attempt/Score evidence. Learner/evaluator deadlines use
one clock helper, and notebook sections are authored directly instead of patched
by cell index and string matching. Retained evidence bytes remain unchanged.

The source-bundle builder exists, but no execution bundle has been created.
The sustained declaration and endpoint analysis exist through the shared runner;
their presence does not imply an admitted horizon or an executed cohort.

Remaining: resolve storage admission, finish exact-recipe calibration, then freeze
horizon/source/plan and launch within the remaining original week allocation.
The 64-update timing attempt timed out; the amended 32-update attempt completed
one seed in 200.78 seconds before disk crossed the 4 GiB reserve. Both stopped;
2788.716979166954 seconds of total experimental preparation remain charged.
A provisional 12,800-update three-seed storage projection is 29.879 GiB plus reserve,
mostly repeated historical diagnostics in snapshots. Current-game replay does not
bound that duplication. Free space fell to about 1.5 GiB. No unrelated data was
removed. The archive separately records 6.77 GiB free at projection time; neither
historical observation is a current capacity check. Compacting snapshot diagnostics
is unimplemented follow-up requiring recovery validation; a shorter toy endpoint
is not a substitute. `save_update` copies current and completed StageRecords,
and resume derives the update offset from diagnostic length. Any compaction must
preserve those coordinates, immutable exports and canonical diagnostic evidence;
dropping diagnostic rows would change recovery semantics. Storage projection must
then be measured again against the changed format before another launch.

Software/evidence delivery must retain this blocker explicitly. No sustained
learner, calibrated plan or immutable execution bundle exists. Sustained improvement
and independently validated daily testing remain open; no baseline promotion or
Task completion. `experiments/current-baseline.md` and its hash-bound calibration
archive own exact costs, failures and evidence limits.

Check (retained at `b4b9913e`): `uv run pytest -q tests/training/test_active_recovery.py::test_safe_pause_restores_current_games_and_exact_learning` — 1 passed after progress-export integration; broader gate/native results remain in `experiments/current-baseline.md`.
