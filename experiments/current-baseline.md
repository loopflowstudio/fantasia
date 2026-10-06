# Current learning baseline — ETU-118

Status: prospective positive control, not a promoted baseline. Jack Heart authorized
bounded local CPU evidence on 2026-10-06. No self-play, architecture superiority,
full-matchup improvement or chapter acceptance follows from this fixture.

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
level; positive-control failure requires diagnosis before graduation.

## Execution and evidence ownership

Experiment resolves complete regimes and existing execute_regime / VerifyStore
owns learning, artifacts and costs. SeatRoutedCollector, NetOpponentTrainer and
the existing Ataraxos update are unchanged in their estimator meaning. A serial
native-root buffer implementation supplies genuine terminal transitions and
respects paused streams. The asynchronous Experiment monitor only admits ordinary
Allies/Lessons games, so this root evaluator is explicit rather than relabeling
fixture outcomes as arena games. Retained JSON binds checkpoint hashes, every
root/action/terminal digest, failures and elapsed cost.

## Remaining acceptance

Run the frozen positive control, diagnose any failure, then freeze and execute
a small complete-game fixed-opponent comparison with initialization and frozen
controls. Produce the editable read-only evidence notebook/HTML and publish the
reviewable result. Software tests alone cannot promote this candidate.
