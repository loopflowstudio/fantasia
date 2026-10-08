# Training deliverables after Jack Heart's approved split

2026-10-04: Jack Heart approved three separate Tasks. Preserve all current implementation. Jack subsequently requested three workers; ETU-89 owns infrastructure and ETU-90/ETU-91 now have separate stacked checkouts and headless pursue-auto runs.

- [ETU-89](https://linear.app/loopflow/issue/ETU-89): executable TrainingRegime/TrainingRun infrastructure, stage contracts, runnable existing-trainer adapters, artifact/cost/budget/failure records.
- [ETU-90](https://linear.app/loopflow/issue/ETU-90/make-direct-self-play-rl-correct-and-test-ataraxos-training-techniques): direct-RL rollout correctness, terminal/boundary advantage and return calculations, independent horizon/estimator/filtering/KL/regularization/schedule/EMA treatments and their focused proofs. Uses ETU-89 contracts and ETU-75 checkpoint admission.
- [ETU-91](https://linear.app/loopflow/issue/ETU-91/compare-learning-speed-and-ataraxos-ablations-with-reproducible): learning-speed comparison and Ataraxos ablation studies, EvaluationProtocol, existing arena/replay, executed notebooks/reports, and concrete follow-up protocols. Depends on ETU-89 and ETU-90.

The original integrated design remains the technical source; these Tasks divide acceptance ownership, not authorization to discard already-written code. Keep separate evidence per Task and map the resulting PR(s) to each Task actually covered. One shared PR is acceptable if its scope and acceptance evidence explicitly cover all three; never claim a Task complete from another Task's smoke alone. Three workers have disjoint file ownership recorded in the preserved worker-handoff.md; shared API changes require coordination. ETU-91 must integrate ETU-90 before final study acceptance. Existing autonomous implementation/publication/landing authorization continues. No paid compute or week-long training run is authorized.

2026-10-04 07:30 PDT resumed goal: prior child Flows had explicitly stopped on
missing parent integration, not on a review request. Original unified process
handles are gone and the live lf process snapshot had no task workers for
ETU-75/89/90/91. Started fresh ordinary headless contributions (not managed
Task workers): ETU-89 handle 39612, ETU-90 95502, ETU-91 32238, ETU-75 94984.
Each emitted a live implementation update. ETU-89 integrated provider head
aba61859 and RL head d49966f8 locally (head observed a9ceed67); 51 integration
tests passed. ETU-75 reported 92 focused passes; ETU-90 reported 25 passes.
These are worker-reported checks, not final merge or scientific evidence.
ETU-91 is adding executable calibration/scientific profiles; its old CLI was
smoke-only. Root owns one scientific launch after verified landing. Keep the
168-hour total ceiling and both study questions; pilot/smoke is not completion.
Shared PR #200 may carry verified ETU-75 dependencies when its old PR lifecycle
blocks a separate delivery. Do not repeatedly repair unrelated LF plumbing.

Next delivery state: ETU-89 ordinary contribution exited with verified head
9a1b90df. Its integrated gate reported 66 passing tests and one nbclient skip;
root installed the declared notebook extra and independently ran
`uv run --extra notebook pytest tests/training/test_study.py::test_report_regeneration_preserves_metrics_without_training -q`: 1 passed (7.79 s).
Root tried supported `lf task sync main --manual`; it rejects the recorded base
aba61859 as contaminated. `lf task sync --continue` reports no operation in
progress. No raw Git mutation or database repair was done. An asynchronous
permission question is pending for a normal non-force Git push and GitHub PR
commands on existing #200, then lf reconciliation, as a narrow exception to
Jack's explicit lf-only Git/delivery rule. Do not assume approval from silence.
The current remote head is 40b3871c; ancestry check proved it is an ancestor of
local 9a1b90df, so a normal push needs no forced history rewrite.
ETU-90 exited ready at f00fdfc6 (code 73033266), waiting on publication for its
final semantic proof. ETU-75 exited at fb59b847, with 92 focused tests and a
16-game/3,843-Command final replay cohort reporting zero mismatches. Final
receipts are not yet in #200. ETU-91 handle 32238 is live and extending the
scientific protocol with held-out endpoint deals, crossed seed matchups and
three separate fixed baselines; do not duplicate that writer.

2026-10-04 delivery fallback accepted: Jack Heart explicitly authorized direct
Git/GitHub delivery and necessary Loopflow database mutations, preferring landed
code to perfect metadata. The active goal authorizes the actual experiments;
the earlier sentence withholding week-long training authorization is superseded.
Root pushed 9a1b90df normally to PR #200 and requested exact-head squash auto-merge.
Python CI passed; remaining jobs are pending. PR is not yet verified merged.
`lf pr reconcile` failed parsing legacy `supervisor_placement=home`; no database
mutation has been made. ETU-91 finished its previous contribution at 4406bda1.
Root restarted ETU-90 (handle 92475) and ETU-91 (65850) after proving no live
workers in those checkouts. Both emitted active implementation updates, now with
the published parent available. Root owns PR #200 and scientific launch; children
own their final proofs and remaining deliveries. Do not duplicate those writers.

Root repaired metadata after the explicit authorization: SQLite backup is
~/.lf/backups/etude-before-authorized-base-repair-20261004.db. Scoped ETU-89
base_commit from aba61859 to actual merge-base1116937986ee87231d73a559e81815df23283cb6.
`lf land -c` then succeeded, requesting task settlement for PR200 at1707d63d
(scratch cleanup). It had auto-committed tracked runtime metrics, so root removed
ONLY .lf/tmp/metrics/ops.jsonl from tracking (local file retained/ignored) and
started lf commit plus lf land -c again; process24021 owns that mutation.
Legacy Etude landing placement `home` cannot parse in this lf version. Root
verified lf home id matches all12 Etude rows, migrated placement to local and
cleared obsolete supervisor_home_id; original rows retained in backup. First
attempt failed a CHECK constraint and rolled back; second transaction changed12.
No Task outcomes or merge proofs fabricated. Reconciliation must now be retried.
Children92475/65850 remain live. ETU90 reports65 integrated tests+one optional
notebook skip, preparing fresh semantic raw/EMA proof. ETU91 synced parent and
is running smokes plus adding calibrated scientific plan generation. New scale
requirement was delivered via ETU91 --steer; /tmp/etu91-scientific-scale-direction.json.

Latest landing head4a4ac367 removes tracked runtime metrics while retaining the
local ignored file. lf land -c pushed it and enabled auto-merge; a legacy-home
landing row was newly written and then narrowly migrated to local. A subsequent
lf pr reconcile succeeded (delivery check complete), not proof of merge.
Preflight confirms AC sleep0,128GiB RAM,16CPUs,only14GiB disk free. Scientific
storage feasibility sent to ETU91 as new direction. ETU90 fresh proof completed
14games/1024transitions each for normal+empty-filter; all8raw/EMA semantic reloads
passed, empty filter preserves learner weights and advances EMA. Parent CI
restarted on final cleanup head. Root is starting a bounded ETU75 followup to
land final fb59b847 receipts after parent, without API changes or Task completion.

Verified wait/progress: final-head PR200 initial checks all pass; macOS
integration and semantic coverage also pass; Linux integration and semantic
conformance remain running. ETU90 worker92475 exited successfully with clean
PR201 published, no auto-merge because parent unmerged; resume lf land -c after
parent settles. ETU75 worker60914 exited after7tests and exact v4 binding proof;
minimal followup patch /tmp/etu75-v4-receipts.patch, do not confuse it with landed.
ETU91 worker65850 remains live. Both integrated smokes passed:83s/24games learning,
209s/72games ablation, exact replays and overlapping cost windows. These are
one-seed workflow evidence only. New calibration-based plan generation and disk
projection still being completed. No scientific calibration/training launched.

PR200 MERGED verified via GitHub at2026-10-04T14:57:32Z, squash
 e30b7b82459fd5b21b55519870375aaf43d0fd42. All10CI checks passed on4a4ac367.
After repeated legacy-home row parse error, root normalized same-home Etude
landing rows again and lf pr reconcile succeeded. Root started lf land -c on
ETU90/PR201 (handle22925); ETU91 receives parent-merged steer. ETU75 bounded
contribution restarted now parent merged to land minimal v4 receipts. No actual
scientific run yet; ETU91 still writing calibrated plan generation.

PR201 recovery: parent completion deleted its remote base branch, automatically
closing201. Root merged origin/main into ETU90 without rewriting, preserving
only2file authored delta (runtime regression + Intelligence memory). Resolved
2conflicts by retaining child versions after proving parent4a vs main identical
for both. Headff8eeb36 pushed normally;2runtime tests passed. GitHub cannot edit
or reopen a closedPR whose base disappeared, so root recreated parent remote
branch at exactly4a4ac367, reopened201, retargetedmain. Keep that temporary parent
ref until ETU91 reparenting settles. Narrowly updated ETU90 task PR base to
actual mergedmain e30b7b8. Restarting lf land -c for201. Scientific code remains
owned by live ETU91 worker65850 (now adding evaluation-only resume proof).

ETU90 lf land initially failed on removed parent checkout. After retargetmain
and actual ancestry integration, root cleared only its merged parent_pr_id;
lf land -c succeeded (handle18727exit0), preserving completion intent for201.
CI is live, no verified merge yet. ETU75 worker48353 exited with PR202 published
and auto-merge requested; receipt/docs only, ETU75 remains open. ETU91 worker
65850 still live, final learning smoke91s with byte-identical6report files on
offline regeneration; finalablation running within15min cap. Gate95passes,
4inherited historical fixture failures documented; no scientific run yet.

PR201 verified MERGED at4d6bf94d705d41955815a82051db6072826e185a;
PR202 verified MERGED at72e197b8f31cc1b5a2f2a3abde3b36fc0ec55727 after all10checks.
Reconcile succeeded after same-home legacy placement normalization. ETU91 live
worker65850 final settled-source ablation passed204s/72exact-replayedgames;
statuscompleted and18comparisons inspected directly. It preserved one failed
attempt caused by merging source while smoke subprocesses were still launching.
Final scientific runner publication remains pending; no calibration/scientific
training yet. Keep ETU91 checkout open and retain .runs evidence through landing.

ETU91 worker65850 exited0. PR203 published/auto-merge requested at9acb8a4740a0ee250f80d02cb590055ce2be4031,
CI live.14studytests+6debugvectorpasses;4historicalfixtures documented. Keep checkout
open. Root generated and committed initial calibration plans ONLY via git add
selectedpaths + lf commit --no-add; experiments/plans/20261004/{learning,ablation}-calibration.json.
Both width64,seed397,all3anchors,onehourallocation; teacher64sims/4gamesperround,
RL8updates/256transitionsperstage. Before secondlaunch update prior_campaign_seconds
with actual firstattemptcost and checkpoint that amendment. Use existing ETU91
venv/source only after its code merged; output all new campaign evidence outside
its checkout under /Users/jack/src/etude.agent-9039d61b/.runs/ataraxos-20261004/.
No actual calibration or scientific run started yet. Root owns unique launch.

PR203 MERGED at8c1869208a6abe3340ce5670eea80e01699413a6; all10CI checks pass.
Root verified git diff of landed source vs retained9acb8a47 is empty for manabot,
managym,experiment runners and recipes. Started actual learning-speed calibration
from ETU91 checkout via uv --extra notebook, handle64093 (confirmedlive), root
output .runs/ataraxos-20261004/learning-calibration-1 and sibling.log. Committed
plan at experiments/plans/20261004/learning-calibration.json (root775030d7).
Study manifest running, firstsearch-distillationseed397 begun. /usr/bin/time -p
captures wholeprocess wallcost in log; add actualcost to nextplan before ablation
calibration. Do not restart handle64093 absent terminal evidence. No scientific
multiseed run yet; calibration is a required input, not goal completion.

Learning calibration64093 exited0: completed56games (all14cells), report generated;
study978.319s, wholeprocess981.24s (time log). Teacher stages142.59+2.34+290.95+3.81s,
RL54.33+51.34s; differing workloads, no learning-strength inference. Created
root .runs/ataraxos-20261004/campaign.json with981.24charged seconds. Updated
ablation plan prior_campaign_seconds=981.24 and committed via lf --no-add.
Started sequential ablation calibration handle63594 in retained ETU91 checkout,
output root .runs/ataraxos-20261004/ablation-calibration-1 plus.log. Do not duplicate.
After it finishes charge full processcost, generate BOTHscientific plans using
completedcalibration, inspect diskprojection/cutoffs, commit before unique launch.

During live ablation63594, root generated NONFROZEN main-study preview from
completed learningcalibration at /tmp/etude-learning-scientific-preview-20261004.json.
No scientific launch. Preview passes currentdiskgate excluding companionreserve:
1,103,052,935projectedbytes +4GiBreserve;3seeds,4rounds,161teacher games/round,
1789RLupdates/stage,12developmentdeals,96endpointpairdeals,24endpointanchordeals.
Main allocation132h includes108htrain+24heval. Must regenerate final with completed
ablation companionplan and updated campaigncost before commit/launch. Ablation
control completed138.69s, secondarmstarted; fullcalibrationstillrunning.

ETU91 direct-delivery metadata repaired: original task_prs row had no GitHub
number despite verifiedmerged203. Backed database to ~/.lf/backups/etude-before-study-merge-record-20261004.db,
then set publication/merge facts from /tmp/etu203-verified-merge.json (head9acb8a47,
merge8c186920,actualtimestamps,continue_task), cleared mergedparent pointer and
used actualbase72e197b8. No Task completion, no source mutation. Ablation63594
still live,4armscomplete and fifthstarted at517.51s. Wait for fullcohort.

Both calibrations COMPLETED: learning56games/981.24wholeprocessseconds; ablation
152games/1420.35seconds. Total2401.59s charged, nofailedattempts in thiscampaign.
Final scientificplans committed root1e6b9f79. Timing-only amendment before scoring:
ablation dev2blocks/endpoint4blocks (double generator cohorts), eval8h instead6;
shared ceiling4hcalib+15hsktrain+8hskeval+108hmaintrain+24hmaineval+9hrecovery=168h.
Conservative projectedstorage0.376GBscreen+1.103GBmain+4GiBreserve fits12GiBfree.
Main priorreservation27h reflects4+23, allocation132h. No score-based tuning.
ACTUAL SCIENTIFIC CAMPAIGN STARTED2026-10-04T16:01:21Z. Supervisorhandle2656,
childpid98538 confirmedlive; firststudy manifestscientific seeds601/1601/2601,
firstcontrolrunstarted. One-off launcher root .runs/ataraxos-20261004/launch.py
under caffeinate -i, using retainedETU91source. It runs ablation-scientific-1 then
learning-scientific-1 sequentially, records total processcost in campaign.json,
stops on failure, refuses overwrite or insufficient remainingbudget. No duplicate
launch. Inspect handle2656 plus manifests/logs. Do NOT mark goalcomplete from
launch: bothstudies must finish and reports/evidence reviewed. No workers remain.

Monitor interrupted; exec cell365 and unifiedhandle2656 are now missing, but
ACTUAL SCIENTIFIC PROCESS REMAINS LIVE. Confirmed supervisorPID98469 (launch.py),
uvPID98538 and trainingPID98596, ~94%CPU. Do not restart. Poll PIDs and ledger/
manifest directly. Controlseed601 completed2580.88active seconds,3checkpoints,
636818environmentdecisions/3534traininggames. Separate-estimators601 ongoing,
firststage977.83s complete,secondstagecollecting. Study/ledgerstatusrunning;
originalsupervisor will automatically launch main after successfulscreen. Wall
processage may include downtime; scientific activeclock receipts are authoritative.
