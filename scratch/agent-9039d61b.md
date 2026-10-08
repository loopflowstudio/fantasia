# Training regimes and the first laptop experiment

2026-10-04. Implementation-plan draft from Jack Heart's direction; the domain
names and experimental intent are accepted, the numerical protocol below is
proposed. No training launch or strength result is implied. Selected ownership
is Intelligence, matching its current reproducible-training and full-game
comparison outcomes. This checkout is not bound to a Task.

## Execution decision

Jack Heart requested autonomous execution across Game, Intelligence and Rules
on 2026-10-04, with kickoff -> implement -> compress and no interactive
Sessions or human-review steps. The authored `auto-code` Flow runs kickoff
then `code` (implement -> compress). It does not add publication, landing,
paid compute or expensive training authorization.

ETU-89 owns this training-regime implementation. Its prepared checkout is
`/Users/jack/src/etude.compare-training-regimes-through-reproducible`.
The copied design there becomes the working design; this checkout retains
source provenance only. Keep the core single-threaded: corrected collection,
TrainingRegime/TrainingRun execution, both recipes, selectable Ataraxos
treatments, arena checkpoints and executed notebooks/reports for both studies.
Continue the supplied design without treating proposed budgets as approved.

Defer separate implementation Tasks for compound combat, post-RL search,
distilling search updates, amortized belief sampling and scaled exploiters.
Their concrete protocols belong in this delivery; implementation depends on
the core's measured policies and stable contracts. Existing historical
training and deck-balance Tasks are not repurposed.

Bounded headless checks can proceed. Expensive experiment budget choices
remain in questions.md. Actual human-play evidence remains unmet wherever
required; automated work cannot manufacture it.

## Outcome and demo

Make it easy to execute a sequence of training stages, retain the resulting
models and costs, and compare two recipes through an existing arena and a
reproducible notebook/report. Jack requested an experimental approach to long
time horizons and direct policy RL followed by belief learning and search.

Accepted concepts:

- `TrainingRegime`: executable recipe of ordered stages.
- `TrainingRun`: one execution with seed, resolved configuration, artifacts,
  measured costs and status.
- An experiment: question/hypothesis, planned runs, evaluation protocol,
  analysis notebooks and report. Initially a document and runner, not another
  general-purpose database entity or orchestration framework.

Proposed demo commands, to be implemented:

```bash
uv run manabot train --regime experiments/regimes/direct-self-play.json --seed 197 --out .runs/regime-demo
uv run experiments/runners/run_training_regimes.py --profile smoke --out .runs/regime-comparison
uv run experiments/runners/run_training_regimes.py --report-only .runs/regime-comparison
```

The comparison command trains both recipes on real managym games, reloads
their checkpoints through the normal player loader, evaluates all four deck/seat
assignments, and produces an executed notebook and report from saved artifacts.
The smoke proves the complete workflow, not learning or relative strength.

## Current system and resolved risks

`model/train.py` owns PPO and checkpoint saving. `sim/net_opponent.py` provides
current-policy self-play. `sim/search_supervised.py` provides visit/chosen-action
distillation and value targets. `scripts/train_challenger.py` binds the current
authored match to PUCT visit distillation and captures source/world identities.
`arena/match.py::play_cell` already implements the selected Allies/Lessons suite
with four-leg paired blocks, bounded subprocesses and retained Commands. Older
planning documents describing that arena binding as absent are stale.

Concrete correctness findings:

1. The self-play collector stores transition-end flags. The shared PPO GAE
   function expects episode-start flags (`dones[t+1]`). A direct probe of the
   existing function with rewards `[0,1,-1]`, zero values, gamma=lambda=1 and
   end flags `[false,true,true]` returns `[0,1,-1]`; correct returns are
   `[1,1,-1]`. Fix the boundary contract before comparison.
2. The collector banks excess transitions but bootstraps from the latest
   pending observation, which can be later than the first unconsumed row.
   Fast streams can also accumulate stale samples across updates. Pause each
   completed stream at its exact rollout boundary. Inspection of
   `agent/vector_env.rs` and `python/vector_env_bindings.rs` confirms all rows
   currently advance: add an optional active mask to the existing buffered
   step API, with all-active behavior preserved for existing callers. Inactive
   rows preserve state/observation and clear transient done/reward outputs.
   Never silently bootstrap across banked rows. Recompute
   boundary actions after updates; do not carry sampled actions into a new batch.
3. Self-play sampling constructs a CPU generator regardless of inference
   device. Use device-compatible sampling and test it; CPU is the initial
   certified execution profile. MPS acceleration requires its own parity and
   complete-loop throughput evidence before the experiment freeze.
4. Checkpoints lack full collector/environment/RNG continuation. A checkpoint
   is a model artifact, not an exact process-resume promise. Failed training
   attempts remain failed; completed stages can be reused only by a new run
   with explicit input references and inherited cost accounting.
5. Belief learning exists over exact possible-world supports with frozen
   behavior-population provenance. It is not an implemented Ataraxos-style
   generative posterior/search pipeline. That integration is a subsequent
   experimental build, not a renamed existing demo.

Machine inspection: Apple M4 Max, 128 GiB, 16 CPU cores. There is no measured
complete-loop throughput for these proposed recipes in this checkout. Hardware
capacity is not a prediction of games, convergence, or week-long reliability.

## Data model and authority

### Evidence incorporated from the additional review

Jack supplied a second agent's review on 2026-10-04. Its strategic conclusion
is adopted as motivation: existing evidence warrants a serious direct-RL
comparison, not treating the historical PPO results as a verdict on RL.
`exp-03` explicitly acknowledges its harmful shaped-reward baseline;
`exp-11` used 262,144-step runs. `exp-09` found control-scenario failures;
`exp-07`, `exp-10`, INT-7 and INT-8 document failed improvement mechanisms at
their tested budgets. These show limitations of particular teachers and
training recipes, not a proven universal ceiling for search or students.
The historical Exit 2 language is research motivation, not current Wave state.

Corrections that affect the experiment:

- `1/(1-gamma*lambda)=16.8` describes a GAE trace scale, not a hard limit on
  learned credit. Bootstrapping can propagate farther. The historical combat
  fraction (~58%) and game lengths came from old-world random play; measure
  the current population. Advantage filtering can select noisy critic errors
  and does not by itself resolve combat or pass decisions.
- KL to a flat uniform policy equals negative entropy plus a state-dependent
  constant for a fixed legal set. The meaningful new factors are the
  reference structure, schedules and collection-policy penalty, not the name
  KL. Infinite `target_kl` means an early-stop threshold is disabled; it is
  not a missing penalty coefficient. Scheduled PPO does not recreate DeepNash.
- `exp-07` measured 24,474 net-in-loop observations/second with 1,024 MPS
  streams on an older world. It excludes learner updates and is not comparable
  to distributed H100 training steps/second. No H100 price or games/week
  extrapolation is adopted. Profile complete collect/update/export loops.
- The structured decoder demonstrated 64 represented attacker declarations
  and deterministic adapter parity. It is explicitly isolated from the
  production policy; it is not a trained autoregressive joint-action policy.
- INT-17 stopped on repeated support materialization with quadratic work, not
  a demonstration that exact beliefs inherently fail on that pool. Preserve
  that repair path. Larger-pool growth motivates sampling independently;
  support depends on multiplicities, hand size and public constraints, not
  just the number of card names.
- The retained 1513 flat-MC-64 rating is attributed to INT-18 in INT-17's
  report. Reuse current arena machinery and rebind S1-S5 competencies to the
  pinned world; do not import historical Elo or scenario scores as baselines.

The Nature supplementary link was inaccessible through its authorization
redirect. The authors' website links the accessible
[preprint appendix D.4, Table 22](https://arxiv.org/pdf/2511.07312): advantage
lambda=.5, outcome lambda=.8; keep the top advantage-magnitude quartile also
exceeding .01; EMA=.999 per training iteration for evaluation; one epoch.
It specifies LR `clip(.5 / iteration^1.1, 5e-6, 1e-4)` and magnet strength
`.05 / iteration^.3`. These are preprint settings, not verified final-Nature
supplement settings or automatically suitable MTG constants. Preserve that
version distinction in the method inventory.

### Models and persisted records

Add strict, versioned Pydantic models under `manabot/training/`. Reuse existing
architecture, observation and match models; do not copy their fields into a
second hyperparameter hierarchy.

`TrainingRegime` contains an ID, world/match/observation binding, named model
specifications, ordered stages, total resource budget and checkpoint-output
selection rule. A stage has an ID, typed operation, inputs referring only to
earlier outputs or immutable external artifacts, target model and trainable
parameters, learning/data configuration, execution profile, stop conditions
and named outputs. Validate references and ABI compatibility before work starts.

Initially implement three operations: `collect_search`, `train_supervised`,
and `train_self_play`. Self-play includes online collection and optimization;
it must not be decomposed into an offline corpus that silently changes the
algorithm. Unsupported operations fail validation. Belief stages can be added
when their real producer and consumer are implemented.

Learning configuration distinguishes objective, advantage estimator, value
target estimator, regularization reference and coefficient schedule, update
constraints, optimizer, and sample selection. Data configuration specifies
behavior/opponents, chance seeds, replay/whole-game splits and information
boundary. Stage-specific validation rejects irrelevant settings instead of
ignoring them. Execution specifies device, worker/thread counts, precision,
memory limit and wall-time budget separately from algorithm hyperparameters.
Also distinguish `learner_weights`, `behavior_weights` and
`evaluation_weights`. Averaged checkpoints are named outputs with averaging
clock/rate and source checkpoint identities. Dataset artifacts name their
generating behavior policy and target kind; search scores, visit targets and
regularized policy-improvement targets are not interchangeable.

`TrainingRun` contains run ID, regime digest and resolved recipe, seed streams,
source/runtime/hardware identities, stage records, artifact references,
actual resource use, and status (`pending`, `running`, `completed`, `failed`,
`interrupted`). A stage records collection, learning and export time, games,
environment decisions, learner transitions, optimizer exposures, and failures.
Name those units; do not collapse them into an ambiguous step counter.

Extend the existing `VerifyStore` SQLite owner with training-run/stage tables
in one migration. Do not stuff multi-stage records into its old PPO-specific
columns. Existing historical rows remain historical; new regime executions
have one canonical writer. Run-directory JSON manifests are derived exports
for portability, not a second writable status authority. Publish artifact
files atomically before committing their digests and references. Arena traces
and receipts retain their existing authority; the run only references them.
`infra.Experiment` remains the existing logging/runtime helper, not this
scientific experiment model.

Core interfaces: `validate_regime(regime)`,
`execute_regime(regime, seed, out, store) -> TrainingRun`, and
`export_training_run(run_id)`. A small explicit dispatcher calls the existing
trainers. No arbitrary Python plugin loader or generic workflow engine.

## First experiment: proposed executable recipes

Question: at equal end-to-end laptop training cost, which recipe is learning
faster now, and which produces the stronger final policy? This is a recipe
comparison; a win cannot identify which individual treatment caused it. The
ablation study below is also a required executable use of the delivered system.

Common settings: current pinned world, authored UR Lessons/GW Allies with
sideboards, equal deck/seat training exposure, viewer-safe inputs, width-64
attention Agent with four heads, identical observation capacity, fresh weights,
terminal +1/-1 and 0 for authoritative draws, and no reward shaping. Training
aborts on omitted legal offers or observation truncation. Distinguish draws
from engine truncation throughout training and evaluation.

**A: search distillation.** Generate complete teacher games with existing
uniform-prior determinized PUCT: 64 total simulations/root, four worlds,
random terminal continuations, 2,000-step continuation limit. Train the policy
on normalized root visits using existing supervised training, Adam 1e-3,
batch 128, at most ten epochs, 10% whole-game validation, value weight zero.
Preserve the unused value head to keep the common network structure. Execute
four collect/train rounds: at most 4.5 hours collecting fresh games and one
hour fitting/exporting each round. Fit the cumulative corpus with permanent
whole-game split assignments, continuing model and optimizer from the previous
round. Each round allows at most ten epochs; unused time is recorded, not
fabricated as compute. The teacher remains fixed, so this is repeated
distillation, not an expert-iteration claim. Final completed epoch per round
is selected. Incomplete teacher games remain charged and
excluded with explicit counts. No free pre-existing corpus or warm start.

**B: direct self-play.** Current policy plays both sides; train a joint
policy/value model for at most 22 hours/run including export. Pilot defaults:
16 streams, 256 learner transitions/stream, gamma=1, policy GAE lambda=.95,
value lambda=1 with rollout-boundary bootstrapping, four epochs, four
minibatches, ratio clip .1, value weight .5, gradient norm .5. Separate the
two estimators and make filtering and schedules independently configurable.
Start with highest-|advantage| 50% of rows selected before normalization for
both objectives as a labelled MTG pilot choice. Also support quantile plus
absolute-threshold filtering for the paper-derived treatment. Log selection
by action type and retained fraction; an empty selection skips and records
the update rather than silently training on all rows.

Proposed damped objective: clipped policy loss + value loss +
`tau * KL(current || uniform_legal)` + `beta * KL(current || collection)`.
Store full legal behavior distributions for the collection-policy penalty.
Use Adam LR `2.5e-4 * (1 + 9p)^-1` and tau `.01 * (1 + 9p)^-1`, beta=.1,
where p is elapsed training-budget fraction. Exact coefficients are pilot
choices, not paper-reproduction claims. Freeze after finite-loss/throughput
calibration without searching for a favorable final result. No search or
belief model supplies B's training data.

Add a structured-uniform reference option: choose uniformly among legal
action types, then uniformly among canonical offers of that type. This has
full legal support, is invariant to offer order, and avoids giving an action
type more mass merely because it has more offers. The grouping is an MTG
design choice, not Stratego's piece-first prior. Make it a measured treatment
before replacing B's flat-uniform pilot. Test masks, normalization and
semantic grouping on target/combat/priority decisions.

Maintain optional EMA outputs initialized from the learner and updated once
per collect/update iteration. Default collection uses current learner weights;
evaluate raw and EMA variants on identical development deals, charging both
evaluations. Do not silently collect with EMA: that is a different behavior
policy and needs explicitly recorded likelihoods. The final raw/EMA selection
rule is frozen before final scoring. Default remains raw for both main arms;
EMA is a paired diagnostic, not post-hoc selection of whichever wins.

The initial comparison is proposed as policy-only for both arms. The later
pipeline freezes B's policy, generates ground-truth-labelled self-play,
trains a belief model, and evaluates search with learned versus uniform
beliefs at matched decision time. Whether that pipeline belongs in this first
week remains an explicit scope question.

## Budget and evaluation protocol

Draft allocation assumes **168 active laptop hours total**, not one week per
arm: 6 hours calibration, 132 training (three seeds per arm x 22 hours), 24
evaluation/analysis and 6 reserve. Laptop unavailability extends calendar time;
it does not create compute credit. If seven elapsed days is the hard limit,
availability must reduce these allocations before freezing. Engineering work
precedes the experiment; setup and failed scientific attempts are accounted.
No paid hardware. Proposed baseline profile: CPU, four collection workers maximum,
one Torch thread/worker, 32 GiB process-tree limit, one active training run.
Calibration additionally measures MPS with in-process batched inference on
the real collect/update path; exp-07 found separate MPS processes problematic.
Use the faster validated complete-loop profile for each recipe, with the same
laptop/time/memory allowance, and freeze device/batching before scoring.
Report algorithm settings and hardware profile separately. A CPU-only reference
remains runnable; MPS microbenchmark wins do not qualify a training profile.
Alternate arm order across seed pairs. Record sleep, contention and throttling.

Final selection is the last completely saved checkpoint within each run's
allowance; never select the best seed. Planned seed IDs: 197, 198, 199, with
separate named RNG streams for initialization, collection, minibatches and
evaluation. Reuse initial weights across paired arms where shapes match;
different visited trajectories are expected.

Use the existing four-leg arena blocks: both deck assignments and both first
players. Primary evaluation is all nine A-seed/B-seed matchups, 128 untouched
deal blocks each: 4,608 games. Secondary evaluation uses every candidate
against fixed random, scripted-greedy and PUCT-64 anchors, 32 blocks each:
2,304 games. Keep anchor results separate from direct head-to-head strength.
Save checkpoints at cumulative 5.5, 11, 16.5 and 22 hour ceilings, with actual
elapsed cost attached. Capture the latest complete checkpoint at each cutoff;
never use a future checkpoint or interpolate weights. Compare all six runs at
the first three cutoffs against the same three anchors on 16 development blocks
each (3,456 additional games), plus paired-seed A/B matches on 32 blocks each
(1,152 games). Total proposed schedule is 11,520 games. Evaluation stops the
training clock and is charged to the evaluation allocation for both arms.
Include source loading, data generation, failed work and exports in the
training cost axis. No endpoint-only answer to the learning-speed question.
Before final scoring, calibration must show the complete schedule including
recording/replay fits 24 hours with a 25% timing margin. Otherwise amend the
document before scoring; never trim games after seeing outcomes.

Both candidates use one stochastic policy pass, CPU, one thread, batch one,
no search. Freeze identical 120-second game / 10,000-Command limits and
report p50/p95 latency and memory. A forfeit, crash or truncation is a failed
execution, not an authoritative draw. Retain every scheduled attempt and
report unresolved-game bounds; an incomplete cohort cannot establish a win.

Report mean B score (win=1, draw=.5) across nine cells with equal cell weight,
all cell/deck/seat scores, and uncertainty resampling A seeds, B seeds and
deal blocks as crossed clusters. Thousands of games do not turn three seeds
into thousands of training replicates. Label intervals descriptive at this
seed count. Proposed decision: B is promising if mean score >=.55 and its
95% interval lies above .50; symmetric criterion for A. Otherwise unresolved.
Anchor reversals or catastrophic deck-specific weaknesses qualify the claim,
not disappear into an aggregate. This is matchup-specific playing strength,
not exploitability or general Magic superiority.

Learning-speed analysis plots every seed's fixed-anchor mean score against
actual cumulative laptop hours, environment decisions and unique complete
games. Cost is primary; decision/game axes diagnose sample efficiency. Report
paired-seed A/B scores at each cutoff, score gains/hour over observed intervals,
and first observed crossing of a preregistered .60 equal-weight anchor score
(unreached is censored). For area-under-learning-curve comparisons use a shared
cost horizon and the last actually available checkpoint between evaluations;
never backfill strength over data-collection time. Do not compare RL returns
to distillation cross-entropy as a shared progress measure. A crossing of the
curves is a useful result: one recipe can learn faster early and lose late.

## Second executable use: Ataraxos-inspired ablations for Magic

Deliver `experiments/ataraxos-mtg-ablations.md`, explicit regime variants,
and the same runner/notebook path, not a paragraph suggesting future tests.
This study asks which learning treatments transfer; it does not claim to
reproduce Ataraxos or prove its game-theoretic guarantees.

Use the five core independent fresh-training arms, all on the same corrected collector,
architecture, match, gamma=1, beta=.1 and common KL-reference choices:

| Arm | Value/policy lambda | Retained rows | LR and tau |
| --- | --- | --- | --- |
| RL control | .95 / .95 | All | Constant initial values |
| Separate estimators | 1 / .95 | All | Constant |
| Advantage filtering | .95 / .95 | Largest absolute 50% | Constant |
| Coordinated decay | .95 / .95 | All | Power schedules above |
| Combined | 1 / .95 | Largest absolute 50% | Power schedules above |

Add named recipe contrasts to make the additional review testable:

- **Horizon:** control at gamma=.99 versus gamma=1; separately increase policy
  lambda to .99 at gamma=1. Do not bundle discount and trace changes.
- **Paper estimators:** outcome lambda=.8 / policy lambda=.5 versus the .95/.95
  control. A scalar-value adaptation is labelled as such; the paper's
  categorical win/loss/draw value objective is a separate representation test.
- **Reference:** structured-uniform versus flat-uniform with all other
  settings fixed. **Step constraint:** beta=0 versus .1 collection-policy KL.
- **Paper filter:** upper quartile AND magnitude >=.01 versus the 50% filter,
  with identical estimates and sample accounting.
- **Averaging:** raw versus EMA checkpoint of each run; no extra training seed
  is manufactured by evaluating two outputs of the same run.

These contrasts are delivered as runnable recipes, but are not all charged to
the five-arm screen. Each add-on has an explicit run list and budget in the
experiment document. The short screen cannot silently select B's week-long
recipe on the same final evaluation deals.

Three paired initialization seeds per arm; one-factor additions identify
effects against the control. The combined arm tests whether the package helps;
it does not identify all interactions. A subsequent leave-one-out design is
warranted if combined performance contradicts the isolated effects. An optional
learning-rate-only versus tau-only study resolves an observed decay benefit;
it is not silently added to the initial budget.

Proposed separate screening profile: one hour/run (15 training hours total),
checkpoints at 15/30/60 minutes, 16 common four-leg development blocks per
anchor at each checkpoint, and 32 untouched blocks per arm/control seed pair
at the endpoint. Freeze a measured evaluation allowance before launch. These
hours are NOT extra work hidden inside the two-regime week. If both studies
must share that week, reduce the week allocation explicitly before execution.
Short screens identify candidates, not whether a treatment will win after a
week. The three full-budget RL seeds are not automatically independent of
screening if their initialization or deals were reused for selection.

Retain diagnostics that explain the result: raw and retained advantage
distributions by action type, policy entropy/KL, value residuals by distance
to termination, bootstrapped tail fraction, episode length, fraction of forced
steps skipped, optimizer examples/second, and collection/optimization time.
Analyze whether filtering selects critic mistakes or terminal proximity rather
than useful choices. For a short-horizon versus long-horizon claim, define
bins from a frozen development population before scoring; episode length
under a trained policy is an outcome, not an independent treatment variable.

The notebook produces an ablation effect plot with every seed visible,
cost-based learning curves, retained-example diagnostics and linked gameplay
traces. The report answers: retain a treatment, reject it at this budget, or
collect more evidence. Proposed screening threshold is a >=.05 mean anchor
score gain at equal cost; uncertainty and all three seed effects accompany
the decision. Confirmatory follow-up uses fresh seeds/deals. Negative and
inconclusive results remain first-class outputs.

Representational changes (autoregressive compound actions), frozen-policy
belief learning and learned-belief search are separate mechanism experiments,
not toggles with claimed implementations. Add a method inventory to the report
mapping each paper technique to implemented treatment, existing behavior,
separate build or omitted mechanism and its reason. This keeps the entire
Ataraxos learning agenda visible without conflating it with the first screen.

## Following the learned policy into search and belief experiments

Search remains a product capability, including belief-conditioned advice.
Policy-only evaluation isolates the source of learned strength; it is not a
decision to remove search from Etude. Deliver the following concrete follow-up
experiment specifications with prerequisites, artifact contracts and proposed
analysis, while keeping their unimplemented stages out of runnable recipes:

1. **Compound combat decisions:** integrate a trainable autoregressive decoder
   over complete legal declarations. Sum conditional log probabilities for
   the joint action; define reward/discount/value boundaries explicitly and
   forbid grouping across intervening information or opponent decisions.
   Compare sequential and grouped policies on the same game outcomes and
   wall budget; report equivalent underlying choices so collapsed prompts
   cannot manufacture throughput gains. Adapter parity alone is insufficient.
2. **Search after RL:** freeze each selected raw/EMA policy identity. On a
   tractable pool, obtain exact posterior weights from that same frozen
   behavior policy, sample compatible worlds, roll out with viewer-safe
   policy observations, evaluate leaves and take one local regularized update.
   Compare policy-only, uniform-belief search and exact-belief search at matched
   elapsed decision budgets. Never feed full sampled worlds into the policy.
   Exact ranges fitted to another population do not establish update equivalence.
3. **Distill the local update:** retain base policy, action-value estimates,
   belief/rollout policy identities, reference, step size and computed target
   distribution. Compare hard argmax targets and regularized soft targets from
   the same roots/cost. Old per-action scores without those identities cannot
   reconstruct this target. Measure student strength, policy mixing and
   adversarial response; soft targets alone do not guarantee sound bluffing.
4. **Amortized beliefs:** collect frozen-policy self-play with hidden truth as
   labels only. Train a constrained autoregressive sampler; keep whole games
   separate across train/validation/test. Compare calibration, legal support,
   sampling cost and resulting search strength against exact beliefs on a
   tractable pool before widening the pool. All widening is a new world-bound
   comparison, not an unverified ten-million-hand extrapolation.

Add a frozen-opponent exploiter protocol for both main arms: independent
attacker seeds, terminal rewards, equal attacker budgets increasing at declared
checkpoints, and fresh final deals. Plot attack success versus attacker compute.
An unsuccessful bounded attacker is not an exploitability certificate.
Charge attacks and their evaluations explicitly; they are outside the proposed
168-hour comparison unless its allocation is amended. Reuse the repaired
`NetOpponentTrainer` frozen-opponent mode, not a second training implementation.
Run S1-S5 at policy checkpoints after verifying current-world legality and
intended strategic premises; report unsupported scenarios rather than silently
substituting old scores. Behavioral failures qualify arena gains.

The document freezes seeds, budgets, numeric prediction (proposed B=.55),
kill criteria and strongest confound before costly runs via `lf commit`.
Training, validation, development and final deal families are disjoint.
The strongest confound is recipe maturity: a negative result may reflect
untuned self-play treatments, not a limit of direct RL.

## Implementation sequence and exclusions

One coherent delivery makes both regime definitions executable and comparable.

1. **This slice:** repair/test self-play boundary semantics and rollout
   freshness, then add regime/run models, persistence and bounded execution.
   Focused fixtures include terminal credit, adjacent episodes, uneven stream
   rates and exact next-state bootstrap. Preserve ordinary PPO behavior.
2. Bind existing supervised and self-play trainers to stage execution;
   implement separate estimators, filtering, KL penalties and schedules as
   selectable treatments. Count all generation/training/export cost. Add
   `--regime`, `--seed`, `--out` to `manabot train`; preset use stays supported
   but combining a regime with preset/override flags is an error.
3. Add the two main recipes, five core ablation variants, named additional
   contrasts and experiment-specific runner; reuse arena
   registrations, replay and world identities. Calibration and final scoring
   are distinct explicit modes; smoke cannot accidentally launch a week.
   `--study learning-speed` and `--study ataraxos-ablations` select the
   two documented uses. Notebook/report generation supports both studies.
4. Add `experiments/study/training-regimes.ipynb` and a report template.
   Analysis functions consume saved run/arena records; the notebook displays
   cost, selected-example diagnostics, scores, uncertainty and trace examples.
   Headless report generation executes it without training or network access.
   Include raw/EMA pairing, reference/horizon contrasts, S1-S5 outcomes and
   explicit not-run panels for unfunded studies. Deliver the compound-action,
   post-RL search, improved-target distillation, belief-sampler and exploiter
   protocols with the experiment documents, not placeholders claiming support.

Delete — do not maintain: the incorrect direct use of stock GAE with
collector-end flags and unbounded excess-transition banking in
`NetOpponentTrainer`/`SeatRoutedCollector`. Update their existing tests.
No wholesale trainer replacement or deletion of historical experiment runners.
Do not add another CLI-local recipe dictionary for these two regimes.

Excluded: launching the expensive experiment during implementation, a generic
Experiment service/model, distributed training, arbitrary architecture search,
automatic best-seed selection, public-belief solving, compound-action redesign,
and an unimplemented belief operation masquerading as a runnable stage.

Success means a new treatment is a validated recipe edit whose cost and
outcome appear in the same analysis. Failure would be a generic orchestration
layer over inconsistent trainers, or two week-long runs whose data/reward
semantics differ unnoticed. The boundary tests and complete smoke target that
failure directly.

## Done when

Proposed gate commands:

```bash
uv run pytest tests/training tests/sim/test_net_opponent.py tests/model/test_train.py tests/arena -q
uv run experiments/runners/run_training_regimes.py --study learning-speed --profile smoke --out .runs/regime-gate
uv run experiments/runners/run_training_regimes.py --study ataraxos-ablations --profile smoke --out .runs/ablation-gate
uv run experiments/runners/run_training_regimes.py --report-only .runs/regime-gate
uv run experiments/runners/run_training_regimes.py --report-only .runs/ablation-gate
```

Each smoke caps its process at 15 minutes. The learning-speed smoke trains
both arms through two checkpoints including a collect/train handoff; the
ablation smoke executes all five variants through at least two updates.
Each reloads immutable outputs, completes a four-leg block for every required
comparison, replays it and executes the notebook. Reports show cost curves
with at least two real measurements and explain the deliberately inadequate
statistical power. Failure to fit is a failed smoke, never
synthetic result substitution. Tests cover invalid/forward artifact references,
world mismatch, budget interruption, stage failure retention, private-label
exclusion from model inputs, reference distribution normalization/permutation
invariance, EMA clock/identity, empty-filter behavior, and report regeneration
with unchanged metrics. Named additional contrasts must validate and execute
bounded optimizer fixtures; the five-arm smoke is not expanded into an
unbudgeted training sweep.
Empty or incomplete evidence renders explicitly as such. No runtime change
is required for planning. The masked-step implementation requires debug
`cargo test --manifest-path managym/Cargo.toml` and the root uv/maturin rebuild
specified by AGENTS.md before Python integration checks.

Check result: 2026-10-04 isolated execution of the existing GAE function
confirmed the collector-mask mismatch; source inspection confirmed current
selected-suite arena support. No training or final evaluation was run.

Launch result (2026-10-04): ETU-89 design/context transfer verified; auto-code
expands to kickoff -> implement -> compress. ETU-89 and ETU-76 startup attempts
failed with `process did not report running within 10 seconds`. ETU-75 is
blocked by a planning/managed-execution Project mismatch. No worker startup
or implementation completion is claimed. ETU-89's destination design is the
working owner; source notes retain launch evidence only.
