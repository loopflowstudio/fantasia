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
the runner does not implement it yet. No automatic retry or reuse of failed paths.
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

## What exists and remaining implementation

Experiment supplies recipe resolution; TrainingRun/VerifyStore and the shared arena
own execution and evidence. Initialization and greedy monitoring, endpoint random
scoring, editable notebook → HTML and complete-state recovery exist. Recovery
preserves learner/Adam/EMA/RNG, counters and current native games; format 3 binds
diagnostic prefixes to canonical VerifyStore rows instead of copying growing
histories. Missing/changed rows reject recovery. Committed work is immutable;
post-snapshot work can repeat with its costs retained. Historical snapshots and
exports remain unchanged. Physical lid closure is untested. Known sleep/pause is
separate; uncertain restart/reboot gaps remain conservatively charged.

The S3 implementation is present at `manabot/training/artifacts.py`; the existing
[storage contract](../docs/training-monitoring.md#s3-model-and-artifact-storage)
owns private model publication and verified readback. W&B owns metric projections,
not model bytes. Credentials on mini and publication remain unverified; a located
contract is not a completed archive. Three ordinary demo-loaded executions and
complete games with both deck assignments remain acceptance work beyond arena.

Remaining launch work is substantive:

1. Bind the exact ETU-105 recipe and linked-stage semantics, fixed 10000 endpoint,
   extra monitoring exports and final 1240 reference in declaration/admission and
   analysis. The current code uses depth1, chooses a minimum 12800 horizon and
   expects 18 final cells instead of the new 24. Implement the bounded calibration
   amendment and mini identity together in calibration/freeze admission; code still
   derives caps from 3600 seconds and clamps learners to 240. Extend Experiment
   for the declared live random diagnostic. CheckpointQueue already has a
   `protocols_for` hook, but Experiment does not yet supply it; reporting must keep
   the two opponent curves separate and reserve their deal families.
2. Pin and stage the reviewed source/environment under an isolated mini evidence
   directory without modifying ETU-105 source or training. The bundle helper
   currently builds only a local artifact under this Task's `.runs`; remote staging,
   manifest/native verification and disconnect-surviving supervision need a bounded
   proof. Existing same-host recovery remains the recovery owner.
3. Measure mini runtime/storage and complete all three calibration seeds under the
   amended cap. Freeze the admitted horizon, full protocol and original-week cost
   ledger. No complete selected-recipe calibration, execution bundle or sustained
   plan exists yet. A failed bound retains evidence; it does not authorize silently
   shortening or extending the 10000-update cohort.
4. Launch the one admitted mini cohort; verify committed learner progress and a live
   completed initialization cohort after disconnect. Keep the editable notebook and
   read-only dashboard current during training, with W&B projection and later S3
   archival through existing contracts. Preserve restart receipts and all failures.
5. Complete final scoring, repeated demo admission/play and publication; promote
   only on the unchanged improvement criteria. Daily-test derivation and independent
   validation follow sustained evidence and remain unimplemented.

Manual pause commits a learner boundary and drains the current bounded evaluation.
A flat curve prompts review; operational failure cannot silently restart a seed.
No further product decision is missing for the authorized mini preparation/launch.

Check: `uv run python` retained-recipe audit — 3 actor-critic recipes and 3720 rate/iteration rows match current formulas, linked 620+620 stages and 256 rows/update verified; `git diff --check` passed. Prior sync feedback retains 25 focused checks at `db2182d8`, including CUDA recovery rejection; no training ran in this reconciliation.
