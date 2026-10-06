# Current baseline: sustained trajectory, then a daily regression test

Jack Heart revised ETU-118 on 2026-10-06: WEEKLY → DAILY. This supersedes the
original positive-control-first completion framing. Jack Heart subsequently authorized a week on the current laptop, then required
sleep/restart recovery and checkpoint-safe pause/resume before launch. No recipe
is validated yet. The allocation is at most seven active days, with known downtime and conservative
unknown restart charges separate. Fresh storage admission now passes; complete current-source calibration still gates launch.

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
The updated Task consolidates ETU-116 fixed-capacity duration measurements and
ETU-82 repeated training/export/play acceptance into ETU-118. Preserve the
ETU-103 mini sequence and any separately authorized ETU-116 mini allocation;
consolidation does not relocate it or authorize duplicate cohorts. Reuse one
admitted trajectory for overlapping baseline/duration questions. At least three
complete independent executions, ordinary demo loading and both deck assignments
remain required. Experiment, VerifyStore, arena and notebook/W&B retain authority;
model publication must use the S3 contract. This checkout has no located S3
implementation/contract yet; resolve before publishing model bytes, not by inventing
an unapproved bucket. ETU-85 retains demo-opponent/human comparison ownership.

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

Remaining: finish exact-recipe format-3 calibration, then freeze horizon/source/plan and launch within the remaining original week allocation.
The 64-update timing attempt timed out; the amended 32-update attempt completed
one seed in 200.78 seconds before disk crossed the 4 GiB reserve. Both stopped;
2788.716979166954 seconds of total experimental preparation remain charged.
The earlier provisional 12,800-update three-seed projection was 29.879 GiB plus reserve,
mostly repeated historical diagnostics in snapshots. That historical projection
remains evidence, not the current estimate. Format 3 now stores diagnostic counts
and digests bound to the original writer's canonical VerifyStore rows. Resume
hydrates and validates the exact prefixes before deriving update offsets; stage
metadata and exports remain snapshot-bound. Setup-failed retries resolve the
original writer. Missing/changed evidence rejects recovery. Historical snapshots
and all scientific attempts remain unchanged.

Offline re-encoding of the retained 32-update state measured 2,084,252 bytes for
the compact snapshot. A reference-count-only 12,800-update stress adds two bytes;
it is not training. The revised conservative minimum projects 6.361 GiB plus the
4 GiB reserve, against 6.220 GiB free at measurement. Growing canonical run copies
and evaluation evidence still need storage. That historical admission failed; no sustained launch followed. The 0.3963909999874886-second offline measurement
brings total preparation including storage measurement to 2789.1133701669414 seconds;
the original 2788.716979166954-second experimental ledger remains unchanged.
`experiments/data/current-baseline-storage.json` and its reproduction archive own
the exact observation and limits. Complete current-source three-seed calibration
must use format 3; freeze rejects historical format-2 calibration.

Jack Heart requested resumption after consolidation. Fresh recorded storage
admission observes 209735249920 free bytes and passes the retained projection plus
reserve. This enables bounded calibration, not an uncalibrated sustained launch.
The next calibration deducts 2789.1133701669414 seconds from the original
3600-second exploration ceiling, leaving 810.8866298330586 seconds. No new week.

Delete — do not maintain: growing diagnostic payload copies inside new recovery
snapshots. Preserve canonical rows, exact prefix counts/digests, stage metadata,
immutable exports and historical snapshot readability; do not compact by dropping
evidence or deleting prior attempts. No other artifact deletion is authorized.

Software/evidence delivery must retain this blocker explicitly. No sustained
learner, calibrated plan or immutable execution bundle exists. Sustained improvement
and independently validated daily testing remain open; no baseline promotion or
Task completion. `experiments/current-baseline.md` and its hash-bound calibration
archive own exact costs, failures and evidence limits.

Check: `uv run pytest -q tests/training/test_active_recovery.py tests/training/test_recovery.py tests/training/test_sustained_baseline.py -x` — 28 passed; separate amended calibration admission checks — 3 passed; focused Ruff passed.

Calibration readmission reserves 150 seconds for bounded evaluation and divides
the remaining allowance across three learners (220.2955432776862 seconds each).
The exact 32-update recipe and seed cohort stay fixed; monitoring is timing-only.
Jack Heart selected ETU-105 filter scope after the completed ETU-103 mini screen;
the separate mini duration proposal is superseded and will not run concurrently.

## CPU evaluator coordination (2026-10-06)

ETU-103 reports an independently allocated CUDA comparison requiring the shared
CPU evaluator. ETU-118 reserves no evaluator now. With the existing campaign-wide
lease, the safe serial schedule is ETU-103's four-game timing calibration and
initialization/milestone scoring first, then ETU-118's bounded calibration after
ETU-103 closes its evaluation owner. ETU-118's calibration needs at most
810.8866298330586 active seconds including 150 evaluator seconds (three attempts
capped at 50 seconds); its learner inherits the lease for that entire window.
No experiment was launched for this coordination request and no allocation changed.

Overlapping campaigns require a separate tested lease change before sustained
launch: acquire per complete cohort, retain the inherited lease until its worker
exits, release while idle, and stop passing the evaluator descriptor to learners.
Preserve per-campaign ownership/crash accounting and yield fairly to waiting
cohorts; simple release/reacquisition alone does not guarantee fair sharing.
Until then, handoff requires a closed queue and exited inheriting processes, not
an idle dashboard. Never unlink the lock or interrupt another campaign's cohort.

Initialization and random-opponent monitoring support are committed in
`975ee9ddc2e597b3126121e834e6922df0417704`; `9c088932872e07a3d73611a47d81b70d7fea8706`
factors the shared worker deadline. Narrow reuse should extract the relevant
queue/protocol hunks and tests, not import recovery/native changes wholesale.
Initial checkpoint export already predates these commits. The shared protocol
supports random monitoring, but ETU-118 currently schedules random scoring only
in finalization; a live random diagnostic remains to be scheduled before freeze.

Coordination check: `lsof` found no open owner for either shared lease at inspection;
source review confirms campaign-wide ownership and learner descriptor inheritance.
