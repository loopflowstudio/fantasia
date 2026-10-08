# Mirror curriculum: laptop screen (ETU-125)

Jack Heart authorized this overnight laptop screen on 2026-10-07, with no rental,
ETU-128 training, Mini displacement or GPU-cohort change. One allocation runs
from 2026-10-08 06:00 UTC through 14:00 UTC, including preparation, calibration,
interruptions, evaluation and reporting. A bounded idle-sleep assertion applies
only to this job; closed-lid execution is not promised.

## Frozen question and predictions

Does including mirrors improve Lessons learning and target cross-deck strength?
Prediction, before scoring: mirror-inclusive training improves Lessons versus
greedy Allies by 5 percentage points at the common endpoint, with at most a
5-point loss for Allies versus greedy Lessons. Treat the result as exploratory:
three independent seeds, small evaluation cohorts and two simple opponents cannot
establish general strength. A positive retention decision requires a positive
paired-seed mean Lessons cross-deck gain with a 95% seed-bootstrap lower bound
above zero and no more than a 5-point average Allies cross-deck regression.
Otherwise retain the negative/unresolved result. Game intervals resample whole
deals and do not substitute for independent training seeds.

First diagnose the unchanged ETU-118 seed-11851 update-2500 checkpoint, SHA-256
`55d3cfb0420f900c7bfcbc7341ebd3924c71dd48b951bc0b31021c0c59ce1090`.
Prediction: both policy decks gain at least 20 points when the greedy opponent
switches from Allies to Lessons. The four-cell matrix tests this directly;
matchup effects and imperfect opponent quality prevent unique causal attribution.
No claim about self-targeting is made without inspecting retained Commands.
The supplemental diagnostic uses five paired deals per greedy cell (10 games),
two per random cell (4 games), in namespace 1912500000. These small cells reserve
learning time; their intervals can remain broad. Source changes in the supplemental
instrument are recorded separately; checkpoint bytes, full rules/content/input
binding and historical primary cohorts remain unchanged.

## Training intervention

The saved baseline is the Mini's width64/depth2/heads4 semantic encoder,
masked-mean scalar critic and Ataraxos move settings, with history off and all
current authored decklists/sideboards. Both arms use 12 streams × 32 learner
transitions per update (384), one CPU learner thread, float32, identical
initialization seeds and iteration-based schedules. The stream geometry differs
from Mini's 4×64 but is identical between the randomized arms; this is not a
replication of Mini's training rate or learning curve.

- A: cross-deck only. Half the streams start Lessons, half Allies; learner
  seats alternate within each setup, giving each deck/play-order stratum 1/4.
- B: four streams each Lessons mirror, Allies mirror and cross-deck. Each
  mirror has both learner seats; cross-deck has both deck orders and seats.
  Thus matchup probabilities are 1/3 each and deck marginals are 1/2 each.

The sampling unit is a learner transition: every stream supplies the same count
per update. Fixed strata persist through native terminal auto-reset. Completed
games and opponent decisions can be unequal because game lengths differ; do not
claim game-balanced sampling. Explicit pack selection keeps mirror semantic IDs
and the complete compiled content manifest equal to the cross-deck world.

Initialization pairs seeds 12551/12552/12553 across arms; order is AB, BA, AB.
Calibration seed 12550 never enters scientific results. Twenty updates per arm
measure whole execution cost, including recovery export. Freeze a common even
multiple-of-20 target, at most 400 updates, from the slower calibration with 1.6×
headroom. Reserve evaluation from measured diagnostic seconds/game with 1.6×
headroom, at least 2,400 seconds, and 600 seconds for final reporting. Require
three paired seeds and at least 100 updates; otherwise stop with failed admission.
The exact plan is recorded before training. No outcome chooses counts or seeds.

## Evaluation and reporting

All arms use the same eight-leg deal block: both policy seats in each of the
four policy-deck/opponent-deck cells. Greedy and uniform legal random source
identities, artifact hashes, actual seat decks and exact replay travel with rows.
Each initialization, midpoint and endpoint receives 10 games per greedy cell
and 4 per random cell. Monitoring namespaces 1912510000 and 1912520000 are
held out from training and shared across arms/seeds/checkpoints. They are repeated
screen evaluations, not untouched final-confirmatory deals. Initialization bytes
are the frozen/no-update control: all gains subtract this same policy's paired
outcomes under the identical frozen evaluator and RNG plan; no fake optimizer
run is used for the control. Aggregates, when shown, weight all four cells equally.

The editable `comparison.ipynb` generates the read-only `comparison.html` using
PR262's report owner, with four cells prominently separated. Show per-cell counts,
deal-cluster uncertainty and gains over initialization; compare paired arm effects
across seeds separately. Costs and progress retain transitions, updates, native
decisions and elapsed time. Calibration and diagnostic results are labeled
separately from randomized training. No conclusion is available while seeds are
pending or the primary cells are incomplete.

## Stop and recovery

TrainingRegime/VerifyStore own optimizer, EMA, collector and recovery snapshots.
The local independent service owns an immutable absolute allocation deadline and
process-tree teardown. It cannot extend the allowance on reconnect or sleep.
The existing one-host/one-evaluator leases prevent overlap with ETU-126. Any
legality, nonfinite, semantic, replay or budget failure retains its attempt and
suppresses the affected estimate. No automatic failed-job replacement occurs.
Same-host checkpoint recovery is explicit and must fit the original deadline;
recovery failure stops that attempt. No model selection, paid compute or promotion
follows automatically from this screen.

## Execution evidence

Pending calibration and independent launch. Full retained artifacts live in
`.runs/etu125-overnight`; exact plan and launch receipts will be linked here.
