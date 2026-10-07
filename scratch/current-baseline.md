# Current baseline: sustained trajectory, then a daily regression test

## Accepted direction, reconciled 2026-10-07

Jack Heart's WEEKLY → DAILY outcome remains: establish sustained improvement,
then independently validate the shortest useful daily regression test. Jack Heart
subsequently moved the single duration cohort from laptop to mini and requested
actual supervised execution after ETU-105 CPU release. This supersedes laptop
placement and the old separate mini duration proposal. ETU-116 duration and ETU-82
repeated training/export/play outcomes belong here; no duplicate cohort or fresh
week is authorized. PR251 software delivery does not complete ETU-118.

Jack Heart's latest 2026-10-07 direction selects ETU-105's actor-and-critic-filtered
masked-mean scalar width64/depth2/heads4, no-history current-self recipe for three
10,000-update runs. This supersedes the depth1 first-screen candidate and automatic
12800–102400 horizon selection. The selection uses ETU-105's early gains and lack
of demonstrated actor-only cost payoff; it is an explicitly evidence-informed
experimental choice, not promotion or optimality. ETU-103/106/105 retain capacity,
representation and learning-rule contrasts. Optional all/none Ataraxos screens
remain future ETU-105 work, not prerequisites. ETU-85 retains human comparison.

## Evidence and resource boundary

The [protocol](../experiments/current-baseline.md) and hash-bound archives own exact
results and costs. Three lethal-target seeds rose 50→100% with unchanged controls
after a retained root failure; the 128-update fixed-random complete-game cohort
gained +6.25/+8.33/+6.25 points and missed the +10-point mean criterion. Neither
establishes sustained self-play strength or supplies current-self calibration.

Calibration 1 timed out at 64 updates; calibration 2 completed one 32-update seed
before disk exhaustion; format-3 calibration 3 timed out at 220.296 seconds with
only initialization evaluated and two seeds pending. All originals remain in
this checkout's `.runs`; pre-kill running exports are not live-process evidence.
Preparation is 3030.011508249935 seconds, leaving 601769.9884917501 seconds of the
original 604800-active-second allocation before new charges. The old exploration
balance is 569.9884917500649 seconds and cannot support the unchanged retry.

Mini route: `jack@100.96.227.95`, repository `/Users/jack/src/etude`.
Jack Heart explicitly released ETU-105 CPU after its twelve final/random cells.
Read-only inspection on 2026-10-07 confirmed completed/exit-zero rows in
`.runs/etu105-mini-filter-scope-final-20261007-1/supervisor.json`; SHA-256 is
`52970cabb661dc96d2d434d2ef5ec0d24b0095d5544b6496274fa883908b9548`.
At 16:44:39 UTC none of its twelve child PIDs appeared and neither shared lease
had an open owner. This is point-in-time evidence; launch still acquires leases.
Mini free space was 60,449,624 KiB (about 57.65 GiB), not the laptop's 195.33 GiB.
This is a capacity observation, not calibrated mini storage admission.

One learner CPU thread plus one bounded evaluator runs on mini under a detached
supervisor. ETU-103 GPU work remains untouched. Existing leases are host/account
local: serial mini use after handoff does not require a cross-campaign fairness
redesign. Same-host overlap remains unsupported; no lock deletion or interruption
of another campaign is authorized.

## Calibration amendment and frozen measurement contract

Under Jack Heart's explicit direction to amend calibration within the remaining
week, the 2026-10-07 execution design reserves at most 7200 additional active
seconds for one fresh mini calibration: three unchanged seeds 11841–11843 × 32
updates, 1800 seconds per learner, 1200 total evaluator seconds (200 per initial/
endpoint four-game cohort), and 600 seconds for bounded prefix/source checks and
coordination/report overhead. Calibration uses the newly selected depth2 recipe.
The longer watchdog addresses the retained 220-second timeout; it is not a
learning-duration result. This numeric amendment is fixed before measurement;
the runner implements it. No automatic retry or reuse of failed paths.
Actual maximum elapsed/additive-process cost is charged once, including setup
and failed preparation. Consuming this full allowance would leave
594569.9884917501 seconds before other new charges. No scientific scores choose
the recipe or horizon.

The sustained contract retains new seeds 11851–11853 and fixes 10,000 updates each,
four streams × 64 transitions = 256 collected rows/update, 2.56M rows per run.
Initialization and updates 400/620/800/1240/2500/5000/7500/10000 are scored; 400/800
remain additional monitoring exports, preserving the first two stage boundaries
at 620 and 1240. Later stages continue to 2500/5000/7500/10000 without resetting
learner, Adam, EMA, collector or iteration. Calibration admits this fixed horizon
against conservative timing/storage plus 4 GiB reserve; it no longer selects a
larger candidate. Jack Heart's roughly 31-hour training estimate excludes measured
evaluation/checkpoint overhead and is not calibration.

ETU-105's frozen serialized recipe says `schedule_clock=run_elapsed_budget`, but
the actual Ataraxos move rule uses one-based collection/update iteration for LR
and tau. Retained diagnostics run 1–620 then 621–1240, including skipped updates;
`learning.rates(iteration)` ignores the budget fraction. Preserve that actual
behavior and the two linked stages, not an invented stretched schedule. The exact
recipe/diagnostics live in `experiments/data/etu105/filter-scope-mini.json.gz`;
source provenance is owned by `experiments/ataraxos-technique-screen.md`.
Current recovery and initialization differ from that historical source, so a
bounded matched-prefix check must establish unchanged learner/RNG/continuation
behavior before scientific execution. Equal rate formulas alone are insufficient.
Source/runtime/world, initial weights, configuration, inference and deals freeze
before scoring. Mini calibration and training share one source/native/environment;
laptop snapshots do not become portable training continuation.

Greedy monitoring uses 25 paired deals × four deck/seat legs (100 games) at
initialization, stage milestones and roughly hourly exports, during training.
The separate live random diagnostic is fixed at initialization and stage milestones
on deals 1911185000–1911185024, also 100 games; it is not endpoint evidence.
Both must flow through the shared queue/reporting path and monitoring reserve.
The existing untouched final deals stay unchanged. Final scoring includes init,
800, 1240 and 10000 for both anchors. The historical +10-point initialization and
+5-point update800 criteria remain; the same +5-point/positive paired-seed-bound
condition also applies versus 1240, the selected recipe's early endpoint. This
prospective addition preserves acceptance while testing improvement beyond that
screen. Every seed/checkpoint, failure, paired change, seed/deal uncertainty,
plateau/regression, transitions, exposures, losses, entropy and phase cost remains
visible. No favorable-checkpoint selection or automatic statistical plateau stop.

## Running execution and remaining acceptance

Implementation is committed at `ba0ae3e9`, published in PR251 and frozen on mini.
The same source/native and locked environment passed a four-update historical/current
comparison: batches, learner, Adam, Torch/minibatch RNG and diagnostics agreed across
a linked boundary. This is bounded prefix evidence, not full 1240-update reproduction.
The three 32-update calibration seeds completed, with six exact-replayed four-game
cohorts. Calibration charged 521.313901 additive seconds. The source-symlink packaging
failure and pre-learner PATH failure are retained; no training seed was retried.
Precalibration overhead exceeded its 600-second subreserve, but actual preparation
remained inside the unchanged 7200-second amendment and original week.

Total preparation is 4355.1377444409545 seconds, leaving 600444.8622555591 active
seconds at launch. Frozen plan `46aabdb0ca584d62cc2264fde9766914750d3befd696970d0428678bae034bb7`
admits 10000 updates per seed at 8.455201 conservative seconds/update and projects
6,198,501,227 retained bytes against 59,870,167,040 free. The 70.46-hour conservative
training projection supersedes the rough 31-hour estimate. Full monitoring/final
reserves remain within the original week; 3600 seconds of the final/report reserve
belongs to periodic notebook refreshes.

Remote root: `/Users/jack/src/etude/.runs/etu118-mini-20261007-1` on
`jack@100.96.227.95`. `source/` owns immutable execution bytes and `.venv`;
`plan.json` owns the frozen cohort; `science/experiment.sqlite` owns execution.
Use this source/environment for all later reads, pause or explicit recovery.
Do not rebuild or edit it, start another cohort, delete leases or reset charges.
The local retained copy is `.runs/etu118-mini-20261007-1/retained` in this Task.
The [protocol](../experiments/current-baseline.md) owns full receipts and limits.

Supervisor 86655 and coordinator 86658 run independently of SSH. After disconnect,
seed11851 committed 128 updates / 32768 transitions / 7634 optimizer exposures;
`load_update` verified snapshot iteration128 against VerifyStore. Both initial
100-game greedy/random cohorts completed with exact replay. Seed11852/11853 remain
scheduled. `science/comparison.ipynb` is editable; supervision refreshes read-only
`science/comparison.html` every five minutes within a retained reporting cap.
`science.supervisor.json` records refresh costs/failures. Flat curves prompt review,
not automatic failure. Safe pause/recovery preserves the existing complete state.

W&B accepted 128 diagnostic rows at
https://wandb.ai/loopflow-studio/etude/runs/training-ed8e425c3663727830077360 .
This verified backfill is not automatic publication for later seeds. S3 remains
credential-blocked: default chain unavailable; configured softmax token retrieval
fails. No auth repair or artifact publication occurred. Private model/recovery
bytes remain on mini and must be retained through archival.

Remaining work:

1. Keep the admitted single trajectory and live evaluator supervised; inspect
   failures before explicit recovery. Preserve the pinned source, all attempts,
   phase costs, monitoring and untouched final cohorts. Refresh/backfill W&B from
   retained evidence; notebook refresh already runs independently.
2. Finish all three 10000-update seeds and the 24 final comparison cells. Report
   every seed, paired changes and separate seed/deal uncertainty; no favorable
   checkpoint selection, baseline promotion or strength claim before the criteria.
3. Admit each completed checkpoint through the ordinary demo and complete games
   with both deck assignments. Archive exact models/evidence through the S3 contract
   once credentials are available; software delivery cannot complete ETU-118.
4. Derive and independently validate a daily test only after sustained evidence.
   This remains unimplemented; no positive long-run result is presumed.

Delete — do not maintain: obsolete depth1 construction and automatic horizon
selection were removed. All historical laptop evidence remains unchanged.

Check: focused allocation, Experiment/queue/report, live dual-opponent export and
real recovery checks passed; mini historical/current prefix passed, all 96 calibration
updates/24 games completed, and detached science committed 128 updates/200 initial
games with exact replay. Lint/diff checks passed; full CI remains its own matrix.
