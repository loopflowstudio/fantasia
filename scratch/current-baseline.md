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

Inspect the unchanged masked-mean scalar recipe from the first value-model
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

The existing recovery journal grows with lifetime microsteps and saves every
update. Its continuous watchdog and orphan settlement charge sleep/calendar gaps.
Those contracts cannot be represented as seven active days with bounded restart
cost. Before launch, extend the existing owners rather than add a second trainer:

- Bound native replay by each stream's current game, preserving exact reset seed,
  next seed, legal action prefix and current observation. Preserve learner,
  optimizer, EMA, all RNGs, counters, run-wide schedules and committed exports.
- Use explicit opt-in active-clock accounting; keep existing wall-clock recipes
  unchanged. Retain calendar elapsed, known sleep/pause time and uncertain abrupt
  interruption charges separately. Never label estimated cost measured compute.
- Checkpoint at bounded intervals and on pause; an interrupted update may repeat
  but committed updates/exports may not. A pause finishes and commits a boundary;
  resume uses the canonical store, original source/recipe and remaining allocation.
- Exercise interruption and recovery against uninterrupted state, including
  episode boundaries, no-update steps, continuation and restart accounting before
  the serious allocation. No sleep-prevention tool substitutes for recovery.
- Expose last update/checkpoint/evaluation time, evaluation lag, throughput, costs,
  failures and strength versus active time with uncertainty. Operational stalls
  are distinct from statistical plateaus. Initially use human-requested pause;
  no automatic statistical plateau rule is authorized by a noisy score or RL loss.

The sustained learner has not started. Recovery semantics and their tests are
launch prerequisites, not reasons to spend the allocation on a known failure.

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

Delete — do not maintain: short full-game promotion/graduation wording is removed;
its frozen thresholds and outcomes remain debugging criteria. The executor and
report share typed Result/Attempt/Score evidence. Learner/evaluator deadlines use
one clock helper, and notebook sections are authored directly instead of patched
by cell index and string matching. Retained evidence bytes remain unchanged.

Current-game recovery, safe pause and active-clock accounting now extend the shared
owners. Real pause/resume matched uninterrupted learner/optimizer/EMA/RNG and native
observations; seven native debug checks passed. The shared Experiment supervisor
preserved interrupted attempts and remaining allowance. Physical lid closure was
not exercised. The affected gate passed. A source bundle inside this checkout
will keep long-run imports immutable through later review commits.

Remaining: resolve storage admission, finish exact-recipe calibration, then freeze
horizon/source/plan and launch within the remaining original week allocation.
The 64-update timing attempt timed out; the amended 32-update attempt completed
one seed in 200.78 seconds before disk crossed the 4 GiB reserve. Both stopped;
2788.716979166954 seconds of total experimental preparation remain charged.
A provisional 12,800-update three-seed storage projection is 29.879 GiB plus reserve,
mostly repeated historical diagnostics in snapshots. Current-game replay does not
bound that duplication. Free space fell to about 1.5 GiB. No unrelated data was
removed. Compacting snapshot diagnostics is unimplemented follow-up requiring
recovery validation; a shorter toy endpoint is not a substitute.

Publish the retained software/evidence with this blocker explicit. No sustained
learner, calibrated plan or immutable execution bundle exists. Sustained improvement
and independently validated daily testing remain open; no baseline promotion or
Task completion. `experiments/current-baseline.md` and its hash-bound calibration
archive own exact costs, failures and evidence limits.

Check: `uv run pytest -q tests/training/test_current_baseline.py tests/training/test_worker_deadline.py tests/training/test_checkpoint_queue.py tests/training/test_experiment_report.py` — 13 passed after compression; broader gate/native results remain in `experiments/current-baseline.md`. Storage compaction and sustained calibration remain follow-up work.
