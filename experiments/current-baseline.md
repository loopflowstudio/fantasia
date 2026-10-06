# Current learning baseline — ETU-118

Status: fresh storage admission passes; current-source calibration required; debugging evidence only.
The sustained learner has not started; daily-test validation remains open. Jack Heart authorized
bounded local CPU evidence on 2026-10-06. No self-play, architecture superiority,
full-matchup improvement or chapter acceptance follows from this fixture.

## Weekly-first scope revision (2026-10-06)

Jack Heart clarified WEEKLY → DAILY during the bounded full-game run. Establish a
serious sustained improving trajectory first, then validate a short daily test
against it. This supersedes any baseline-promotion wording in the original debug
protocol below. Its frozen thresholds still score that debug cohort; they cannot
promote a baseline, choose a recipe for fast early gains, or complete ETU-118.
The original debugging cohort and its thresholds remain intact. Sustained hardware/horizon/budget require exact
recipe calibration and coordination with ETU-116. Jack Heart subsequently
authorized a week on the laptop, subject to the recovery requirements below. The current executable protocol and retained outcomes are below.

## Frozen positive control

Question: does the historical masked-mean candidate learn to direct lethal damage
at the opponent through the ordinary RL path?

`uv run python -m experiments.runners.current_baseline --plan experiments/regimes/current-baseline-positive.json`
exports the Experiment declarations, seeds, held-out deals and thresholds. Execution:
`uv run python -m experiments.runners.current_baseline --run .runs/etu118-positive-1`.
Use a fresh destination; existing attempts are never overwritten or retried.

The starting recipe is the exact ETU-106 historical scalar baseline with only
masked pooling selected: width64, heads4, depth1, no history, Ataraxos move,
quantile .75, minimum advantage .01, actor-and-critic filtering, LR upper bound
.0001, policy/value traces .5/.8, collection KL .1 and action-type reference.
Architecture and learning settings remain fixed. Workload becomes 100 updates,
four streams, 16 terminal transitions per stream (6,400 per execution).

`lethal-target-v1` keeps the exact authored Allies/Lessons decks and semantic
catalog. The UR player alternates seats. The native scenario surface clears hands,
sets both life totals to 1–3, adds 3–4 existing Mountains to UR's battlefield and
puts its existing Igneous Inspiration in hand. A fixed preparation casts it;
the learner chooses between the two legal player targets. Fixed priority passing
then lets the engine resolve the spell to terminal. No reward is fabricated.
This is a target-choice task with scripted preparation/continuation, not a learned
complete-game policy. Changing seat reverses the winning positional action index;
visible life/mana, physical card identities and library order vary with seed.
The model sees ordinary viewer-safe encoded observations, no answer feature.

Seeds 11801, 11802, 11803 each run learning and no-update collection controls.
Initialization and frozen endpoints must have identical weights and paired
sampled evaluation outputs. Raw trained exports must change weights and reload
through ordinary admission. Each evaluated artifact plays 64 held-out seeds
1911180000–1911180063 in both seats (128 terminal games). Action RNG is matched
across artifacts; every selected action and terminal digest is replayed from its
root. Evaluation games quantify checkpoint noise; three training seeds are the
method-level replicates. No seed replacement or checkpoint selection.

Prediction and pass rule, fixed before scoring: **each seed** reaches at least
85% sampled terminal wins and improves at least 25 percentage points over its
initialization and frozen control. All games must terminate legally with exact
replay. Failures, empty filtering and negative results stay in the record; failure
does not authorize changing this threshold. Constant action-index play achieves
50% on the seat-balanced task. Report each seed plus paired-seed uncertainty;
three seeds do not establish transfer or broad robustness.

One learner CPU thread, 900 seconds per complete attempt including reload/scoring,
3,600 seconds aggregate including all failed attempts. The regime reserves 780
seconds for training with a 760-second stage bound. No paid compute or other
campaign intervention. The native build is a setup operation, not training.
Host load fell from 41.73 to 10.46 during preparation; these runs cannot calibrate
uncontended throughput. A new full-game allocation must be frozen before that
level; positive-control failure requires diagnosis before full-game debugging.

## Execution and evidence ownership

Experiment resolves complete regimes and existing execute_regime / VerifyStore
owns learning, artifacts and costs. SeatRoutedCollector, NetOpponentTrainer and
the existing Ataraxos update are unchanged in their estimator meaning. A serial
native-root buffer implementation supplies genuine terminal transitions and
respects paused streams. The asynchronous Experiment monitor only admits ordinary
Allies/Lessons games, so this root evaluator is explicit rather than relabeling
fixture outcomes as arena games. Retained JSON binds checkpoint hashes, every
root/action/terminal digest, failures and elapsed cost.

## Debugging acceptance and remaining outcome

The original positive-control and short full-game cohorts completed; their results
are retained below. The editable notebook generates the debugging evidence HTML.
These checks cannot promote the candidate. Sustained learning, followed by an
independently validated daily test, remains the main outcome.

## Frozen full-game debugging protocol

After the complete positive control passes, the next bounded level uses the
unchanged authored Allies/Lessons setup and masked-mean learning settings, fresh
seeds 11821–11823, and **128 updates × 4 streams × 64 transitions**. The environment
returns to ordinary native full-game reset/step; the training opponent is fixed
uniform random, not current-self. This isolates learning before self-play.
Initialization and full-length no-update controls remain paired per seed.

Freeze 12 new held-out deals 1911181000–1911181011, all four deck/seat legs, for
48 games per checkpoint against source-pinned scripted greedy. This opponent is
an evaluation reference, not the training opponent. Three seeds × initialization,
trained and frozen endpoints means 432 complete arena games. Each policy uses
one CPU thread, one stochastic forward pass and the same action-seed aliases.
The arena retains canonical Commands, exact replay, truncations and failures.
No search, best-checkpoint selection or training on evaluation deals.

Allocate at most **2,700 seconds** total for this level and **900 seconds per
seed/control attempt**, including evaluation; cap training at 600 seconds per
run / 580 per stage. Positive-control costs plus this allocation must fit the
original 3,600-second exploratory ceiling. Stop without replacements on failure.
These are conservative execution allowances, not measured throughput promises.

Prediction: the mean paired trained-minus-initialized score is at least 10 points.
The original debugging criterion requires that mean gain, positive gain in every seed, identical paired
frozen/initial outputs, all games replaying, and a positive lower 95% paired-seed
bootstrap bound. Report every seed and seat/deck leg regardless of the result.
Three seeds and one scripted reference are only a reproducible small-matchup
learning control, never a chapter-strength or self-play claim. Failure preserves
the narrow target-task result; neither debugging outcome permits baseline promotion.

## Retained failure and protocol amendment (2026-10-06)

The first attempt at commit `14597e3e`
stopped after 52.36744591698516 seconds. Seed11801 reached 100% from 50%; its
frozen control stayed at 50%. Seed11802 failed after six updates because seed22243
surfaces Discard before Priority. No third seed ran. These partial observations
cannot satisfy the cohort rule. Originals remain in `.runs/etu118-positive-1`.

Preparation now legally executes initial non-priority decisions until Priority
before injecting; no deal is dropped or reseeded. The fixed seeds, 100 updates,
held-out cohort and thresholds are unchanged. Explicit recovery is a fresh full
cohort, not continuation or replacement of the failed seed, with all previous
52.36744591698516 seconds deducted from the 3,600-second ceiling:

`uv run python -m experiments.runners.current_baseline --run .runs/etu118-positive-2 --prior-result .runs/etu118-positive-1/result.json`

The amendment follows observed partial results and is not independent confirmation.

## Sustained-run ownership and daily validation

Jack Heart explicitly authorized a week-long run on the **current laptop** after
positive-control prerequisites and exact throughput calibration. ETU-103→ETU-116's
mini sequence remains reserved. The earlier mini-only consumption proposal is
superseded; coordinate compatible total-step evidence with
[ETU-116](https://linear.app/loopflow/issue/ETU-116) without duplicating its study.

The subsequent recovery requirement is a launch prerequisite: complete learner,
optimizer, EMA, RNG and collector state must survive sleep/restart, with safe
checkpoint-boundary pause/resume and no duplicate committed work. Preserve attempt
lineage and spent allocation. Seven active days with separately shown calendar
downtime is the requested accounting direction; exact handling of abrupt-death
uncertainty must be explicit and tested. No sleep-prevention tool substitutes for
this contract. Existing lifetime journals and sleep-inclusive watchdogs are not
sufficient for that claim. The sustained learner has **not started**.

Choose seed horizons from measured candidate throughput and reserve evaluation,
reporting and recovery inside one nonrenewing allocation. Display last update and
evaluation timestamps, checkpoint lag, throughput, failures, costs and repeated
strength estimates with uncertainty. Operational stalls differ from statistical
plateaus. Initially expose evidence and a manual safe pause; no automatic plateau
stop is inferred from loss or a single noisy score.

The shared evidence contract should include three independent seeds, the exact
masked-mean current-self recipe, initialization and 400/800-update checkpoints,
a meaningfully longer calibrated endpoint, fixed greedy and random anchors,
paired deck/seat/deal blocks, all attempts, raw checkpoint identities and separate
collection/learning/export/evaluation costs. Fix the iteration schedules across
milestones; do not stretch schedules to produce favorable endpoint comparisons.
Laptop calibration must measure that exact recipe. The 128-update random-opponent
laptop cohort does not supply its rate, horizon or allocation.

After an improving sustained trajectory exists, daily-test selection can inspect
candidate prefixes and evaluation subsets against later outcomes. Reserve
independent repeats for validation rather than fitting and testing the same three
seeds. Include optimizer-disabled, reward-perspective and terminal/bootstrap
regressions as candidates; test which the short measurement actually detects.
Do not claim a shorter test predicts long-run plateaus, capacity rankings or
architecture improvements merely because its early score increases. The present
root checks detect terminal reward/sign errors and lack of optimizer improvement;
they have **no established predictive relationship** to sustained strength.

Recovery/accounting now passes bounded interruption and resume checks, including
complete-state equality and conservative restart charges. Physical lid closure
was not tested. Exact laptop calibration, frozen seed horizons, sustained improvement
and independently validated daily-test limits remain unresolved. Seven-day
authorization exists; no calibrated sustained plan or daily threshold is selected
yet. This PR does not complete ETU-118.


## Retained debugging results

The corrected target cohort completed in 137.39071470798808 seconds after the
retained 52.36744591698516-second failed attempt. All three seeds rose from 50%
to 100%; frozen controls stayed at 50%. The degenerate three-seed bootstrap gain
interval is [50, 50] points, not evidence of population certainty. All 1,152
root evaluations replayed exactly.

The short full-game cohort at `6a2da188` completed in 2028.4034482080024 seconds.
For seeds 11821/11822/11823, initial scores were 31.25/33.33/33.33% and trained
scores 37.50/41.67/39.58%; frozen controls matched initialization. Gains were
6.25/8.33/6.25 points, mean 6.94 [6.25, 8.33] by paired training-seed bootstrap.
All 432 games replayed exactly. The predeclared 10-point mean-gain criterion
**failed**. This is retained negative debugging evidence, not sustained self-play
acceptance; training used a fixed random opponent and only 128 updates. Individual
checkpoint deal-cluster intervals remain in the original monitor records.
Total experimental debugging cost including the failure was 2218.161608833 seconds.
Software builds/tests and report generation are separate preparation work.

The byte-preserving [JSON bundle](data/current-baseline-debugging.zip) and
[hash manifest](data/current-baseline-debugging.json) retain all 27 result/run/monitor
records. Full private checkpoints, SQLite and replay tapes remain under this
checkout's `.runs/etu118-{positive-1,positive-2,full-game-1}`. Do not relocate or
remove those originals during delivery. The editable
[notebook](study/current-baseline.ipynb) reads the bundle and generates HTML;
refresh never overwrites notebook edits. Regenerate with:

```bash
uv run --extra notebook python -m experiments.runners.current_baseline_report experiments/data/current-baseline-debugging.zip --output .runs/etu118-report/published.html
```

## Sustained protocol, before calibration/scoring

The serious candidate keeps the masked-mean scalar architecture and Ataraxos
move-learning controls above, with current-self collection. Absolute iteration
learning schedules do not stretch with the selected horizon. Three new independent
seeds are 11851, 11852 and 11853. Timing-only calibration uses 11841–11843, 32
updates each, one learner thread, one evaluator and a 1,050-second total cap;
per-learner attempts are capped at 240 seconds. This cap plus retained debugging and the failed timing attempt below fits the
original 3,600-second exploration ceiling. Calibration scores
cannot select a recipe or horizon. Recovery and restart checks precede it.

`experiments.runners.sustained_baseline` constructs an ordinary Experiment and
uses the shared runner. Candidate endpoints are 12,800, 25,600, 51,200 or 102,400
updates. Select the largest fitting a conservative measured rate (1.5 times the
slowest whole-run average or 95th-percentile update interval), measured retained
storage projection and 4 GiB disk reserve. Smaller horizons do not silently
satisfy this sustained protocol. Preserve 400/800 and doubling milestones,
initial raw weights, and hourly monitoring exports. Raw weights alone are scored;
EMA exports remain retained, without favorable checkpoint selection.

One nonrenewing 604,800-active-second ceiling includes recorded debugging,
calibration, training, monitoring, recovery and final evaluation/reporting. Reserve
86,400 seconds for monitoring and 86,400 for final evaluation/reporting; divide
remaining learning allowance equally among seeds. These are maximum allowances,
not a requirement to spend a week. Sleep and safe-pause downtime are separate.
Unknown abrupt-restart gaps are conservatively charged and identified as estimates.
No automatic retry, fresh allocation, paid compute or mini displacement.

Repeated greedy monitoring uses 25 fixed deals 1911183000–1911183024, all four
seat/deck assignments, with deal-cluster uncertainty. These inspected games are
not held-out endpoint evidence. Final evaluation uses 100 separate paired deals
1911184000–1911184099, all four assignments, against source-pinned scripted greedy
and uniform legal random at initialization, update800 and the preselected endpoint.
Every game must terminate legally and replay; incomplete cohorts suppress claims.
No replacements, exclusions, outcome-based stopping or endpoint selection.

Promotion requires the primary greedy endpoint's mean gain over initialization
at least 10 points, positive gain in every seed and a positive lower 95% paired
training-seed bootstrap bound. It must also improve at least 5 points on average
over update800 with positive lower paired-seed bound, demonstrating progress beyond
the existing short screen. The secondary random mean must not regress more than
5 points from initialization. Retain per-seed and deck/seat results and both
checkpoint deal uncertainty and training-seed uncertainty separately. Three seeds
remain exploratory; passing does not establish human-challenger acceptance.
Plateaus, regressions and failures remain results; thresholds will not be weakened.

No automatic statistical plateau rule is selected. The dashboard must expose
strength versus active training cost, update/evaluation times, throughput and lag,
with manual checkpoint-safe pause/resume. An operational stall is missing updates,
checkpoints or failed evaluation, not a claim inferred from RL loss. A daily test
is selected and independently validated only after this trajectory is established.


The public run controls are:

```bash
uv run python -m experiments.runners.sustained_baseline calibrate .runs/etu118-calibration-3 --preparation-seconds 2789.1133701669414
uv run python -m experiments.runners.sustained_baseline freeze .runs/etu118-calibration-1 experiments/regimes/current-baseline-sustained.json --preparation-seconds ACTUAL_RETAINED_COST
uv run python -m experiments.runners.sustained_baseline run experiments/regimes/current-baseline-sustained.json .runs/etu118-weekly-1
uv run python -m experiments.runners.sustained_baseline pause .runs/etu118-weekly-1
uv run python -m experiments.runners.sustained_baseline run experiments/regimes/current-baseline-sustained.json .runs/etu118-weekly-1 --resume --recover STOPPED_ATTEMPT_ORDINAL
uv run python -m experiments.runners.sustained_baseline report .runs/etu118-weekly-1
```

`ACTUAL_RETAINED_COST` includes debugging and every calibration attempt, with
parallel evaluator occupancy retained separately; it is not a new allocation.
Use the frozen source bundle for the serious run and every recovery. Its source
manifest binds the original commit and exact tracked/native bytes. It lives
inside this checkout's `.runs`, has no Git metadata and launches no second Task.
Ordinary review commits cannot change its imports or restart admission. Model
exports, optimizer state and replay tapes remain private evidence, not notebook
inputs or player-facing files.

The shared editable `comparison.ipynb` is created once in the run directory.
`report` executes its existing cells to write read-only HTML, preserving edits.
Individual curves show progress before all seeds reach common milestones;
comparisons still use their shared milestones. Saved JSON carries current progress
between report refreshes. Last saved update, evaluation lag, throughput, uncertainty,
failed attempts and costs distinguish stale execution from a statistical plateau.
No raw-loss stopping rule is active. A requested learner pause also waits for the
current evaluation cohort to finish; it is bounded, not instantaneous.

A completed sustained cohort automatically enters the fixed endpoint comparison
inside the reserved final budget. Its plan hash marks those held-out rows as a
predeclared comparison, never arena promotion authority. Failed/incomplete cells
suppress acceptance. A later `finalize PLAN RUN --resume` retains existing attempts
and budget; it does not silently replace failed games. The derived conclusion
reports criteria met/not met, leaving human-challenger and daily-test acceptance
explicitly separate. No result has yet established either.

### Timing-only calibration amendment (2026-10-06)

The original 64-update probe at `975ee9dd` exceeded its first 240-second learner
cap before a complete update checkpoint was committed. No subsequent seeds ran.
The failed attempt remains in `.runs/etu118-calibration-1`: 240.11953008300043
seconds elapsed and 255.35032220798894 additive learner/evaluator seconds. Charge
the larger amount once; retain incomplete training state and the initial evaluation.
No score was used to choose this amendment.

The fresh timing cohort uses the same three calibration seeds and exact recipe,
32 updates each, unchanged 240-second learner caps and a 1,050-second total cap
with 300 seconds reserved for six bounded four-game evaluator cohorts. Debugging
plus failure plus this maximum totals 3523.511931040989 seconds, within 3,600.
This shortens a throughput probe, not the sustained endpoint or learning criteria.
No fresh allocation or claim follows from the failed timing attempt.

### Storage admission failure and current boundary (2026-10-06)

The amended calibration at `784dcedd` completed seed11841's 32 updates in
200.77795141597744 training seconds, then stopped the second learner when disk
space crossed the shared 4 GiB reserve. The third seed did not run. The retained
attempt used 269.494022333005 elapsed seconds and 315.2050481259648 additive
learner/evaluator seconds. Its incomplete cohort cannot freeze a sustained plan.
The first timeout's partial update work remains uncommitted; neither attempt is
silently resumed, replaced or treated as successful calibration.

All experimental preparation so far is **2788.716979166954 seconds**, charging the
larger elapsed/process total per calibration attempt and retaining prior debugging.
The [calibration archive](data/current-baseline-calibration.zip) and
[hash/cost manifest](data/current-baseline-calibration.json) preserve 23 original
records/logs/notebooks. Full SQLite, model and recovery files remain in
`.runs/etu118-calibration-{1,2}`. Both coordinators and their workers stopped.
The amended attempt's editable notebook regenerated its HTML from retained data.

A timing-only projection from the single completed seed puts the smallest planned
12,800-update × three-seed cohort at **29.879 GiB**, plus the 4 GiB free-space
reserve. This is provisional, not admitted calibration. Repeating the growing
historical diagnostics inside every immutable recovery snapshot dominates the
projection; compressed current-game prefixes alone do not bound total retained
storage. Free space was approximately 1.5 GiB when execution stopped. No unrelated
files, campaign evidence or mini processes were changed.

Before another calibration or sustained launch, storage must satisfy admission.
Recovery format 3 now replaces diagnostic copies with count/digest bindings to
the original writer's canonical VerifyStore prefixes. Loading verifies and restores
those exact rows, preserving stage-local offsets, complete learning state and
exports. Completed-stage diagnostics use the same references. Retained format 2
snapshots remain unchanged; this does not admit old sources for new training.

The [offline storage measurement](data/current-baseline-storage.json) and
[reproduction script/receipt](data/current-baseline-storage.zip) re-encode the
retained 32-update state without training or changing original artifacts. The
snapshot falls from 2,134,089 re-encoded bytes to 2,084,252; changing just the
reference count to 12,800 adds two bytes. The latter isolates format growth and
is not a trained long-horizon state. Under the existing conservative allowances
(130 snapshots per seed, 1 MiB current-game headroom each, four growing run-record
copies, and 2 GiB evaluation reserve), 12,800 updates × three seeds now projects
**6.361 GiB plus 4 GiB free-space reserve**. Measured free space was **6.220 GiB**;
admission still fails. The original 29.879 GiB projection remains historical.
Complete current-source three-seed calibration is still required, and freeze now
rejects calibration using the old snapshot format. The 0.3963909999874886-second
offline measurement is charged separately, bringing preparation including this
measurement to **2789.1133701669414 seconds**; the original 2788.716979166954-second
experimental ledger is unchanged. No calibration or sustained learner started.
Merely freeing enough for another short probe would not admit the full projected
cohort. The seven-day authorization remains valid; no frozen sustained plan,
source bundle or sustained learner has been created. Do not shorten the main
horizon into a toy test, reset spent budget or claim baseline/daily acceptance.

Verification: affected Python gate 39 passed; focused monitoring/report/authoring
and abrupt-restart checks 44 passed; allocation checks 2 passed. Seven native
debug checks and all-target/all-feature Clippy passed. These bounded proofs do not
establish a physical lid-close test, sustained throughput or learning success.


### Consolidated continuation and storage readmission (2026-10-06)

Jack Heart requested resumption after consolidating ETU-116 duration measurements
and ETU-82 repeated training/export/play acceptance into ETU-118. Preserve the
reserved mini sequence and separately authorized mini allocation; use one admitted
trajectory for overlapping questions. Three complete independent executions must
load through the ordinary demo and complete both deck assignments. Publish model
bytes through the S3 contract and retain notebook/W&B reporting; the S3 contract
has not been located in this checkout and remains a publication prerequisite.
ETU-85 retains the demo-opponent and exploratory human comparison.

[Fresh storage admission](data/current-baseline-storage-readmission.json) records
209735249920 free bytes against 6830273768 projected plus 4294967296 reserve.
It supersedes the capacity shortage, not the incomplete timing evidence. The
format-3 calibration retains all three timing seeds and 32 updates, with a total
cap of 810.8866298330586 seconds: the original 3600-second exploration ceiling
minus 2789.1133701669414 already charged. It may fail within that bound; failures
remain evidence and do not grant a new allowance. No sustained horizon is frozen.

Calibration readmission reserves 150 seconds for bounded evaluation and divides
the remaining allowance across three learners (220.2955432776862 seconds each).
The exact 32-update recipe and seed cohort stay fixed; monitoring is timing-only.
Jack Heart selected ETU-105 filter scope after the completed ETU-103 mini screen;
the separate mini duration proposal is superseded and will not run concurrently.

Compact recovery verification: 28 selected recovery/allocation checks passed,
including exact state, abrupt exit, multistage completion, setup-failure lineage
and missing/changed diagnostic rejection. Three amended admission checks passed.
These are software checks, separate from experimental preparation charges.
