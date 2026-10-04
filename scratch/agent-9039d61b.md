# Training regimes and the first laptop experiment

2026-10-04. Implementation-plan draft from Jack Heart's direction; the domain
names and experimental intent are accepted, the numerical protocol below is
proposed. Bounded implementation smokes have run; no expensive launch or
strength result is implied. Selected ownership
is Intelligence, matching its current reproducible-training and full-game
comparison outcomes. This checkout is bound to ETU-89.

## Accepted delivery boundary (2026-10-04)

Jack Heart split the implementation into ETU-89 infrastructure, ETU-90 RL
correctness/treatments, and ETU-91 study/arena/report delivery, then assigned
three dedicated workers. The integrated scientific design below remains the
shared intent; acceptance is separate for each Task. File/API ownership and
preserved evidence are in `worker-handoff.md`.

ETU-89 owns the regime/run models, executor, CLI, store, supervised continuation
and ordinary artifact integration. ETU-90 owns collector and objective changes;
ETU-91 owns recipes, protocols, runners, notebooks and study evidence. Existing
child-owned code in the parent checkpoint is preserved. ETU-75 owns ordinary
checkpoint compatibility. Publication and landing are authorized; paid compute
and expensive experiments are not. Numerical scientific budgets remain draft.

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

Implemented entry points (bounded pilot recipes; final-world acceptance pending):

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

Implemented corrections and remaining limits:

1. The original collector supplied transition-end flags to episode-start GAE,
   losing terminal credit. `transition_gae` and paused native vector stepping
   now implement the corrected boundary. No surplus row or sampled action
   crosses an update boundary. ETU-90 owns final correctness acceptance.
2. CPU float32 is the supported execution profile. MPS requires separate
   parity and complete-loop timing evidence; historical throughput does not
   certify these recipes.
3. Same-run self-play continuation keeps the latest live collector and Adam.
   Supervised continuation retains Adam and fixed whole-game membership as the
   corpus grows. Checkpoints remain model artifacts, not process-resume files;
   external resume and inherited-cost admission are unimplemented.
4. The belief-learning demo is not a generative posterior/search pipeline.
   Compound combat, post-RL search, distillation of local updates, belief
   sampling and exploiters remain ETU-91 follow-up protocols.

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

### Implemented models and persisted records

`manabot/training/models.py` supplies strict version-1 models. One regime binds
an Agent, observation space and authored match, ordered typed stages, a total
wall budget and last-complete-raw selection. Stage IDs name earlier outputs;
validation rejects forward/wrong-kind/duplicate dataset references, unsupported
operations and branching from an older self-play collector. Named multiple
models and external artifact inputs from the original broader schema are not
implemented; the two initial recipes use one model and same-run references.

The three operations are `collect_search`, `train_supervised`, and
`train_self_play`. Existing trainers own the work. The CLI rejects regime plus
preset/override combinations and preserves ordinary presets. Execution is CPU,
float32, one worker with declared thread/memory/wall limits. Self-play schedules
use elapsed whole-run budget, including setup, collection, updates and exports;
continuation does not reset the clock. Raw weights collect; EMA is an optional
named evaluation artifact. Final EMA helper integration remains below.

`VerifyStore` owns run and stage records; `run.json` is derived from SQLite.
Artifacts are published atomically and hashed, checked again at use, and normal
checkpoint loading is required before admission. Failed/rejected artifacts,
startup/export errors and deadline interruptions retain records. Source/native/
content/tensor/hardware identities, named seeds, setup and phase wall times,
CPU time, sampled process-tree RSS, games, decisions, learner transitions and
optimizer exposures are recorded. Memory is sampled, not an exact peak or an
OS-enforced hard ceiling.

Source games have run-local immutable indexes; indexes divisible by ten retain
validation membership across collection rounds. Both whole-game partitions
must be nonempty. Supervised stages retain independent Adam snapshots and use
the newly declared LR. No fresh split or optimizer reset is hidden in a round.
The shared interfaces are `validate_regime`, `execute_regime` and
`export_training_run`; `infra.Experiment` remains the existing runtime helper.

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

## Implementation status and remaining acceptance (2026-10-04)

ETU-89 infrastructure and trainer adapters exist. The retained
`.runs/regime-smoke-1` completed both recipes with two checkpoint measurements,
including cumulative supervised rounds and ordinary reload. Those artifacts
predate ETU-75 and later provenance refinements. The focused suite subsequently
passed 23 tests, including real two-stage self-play Adam continuation and
checkpoint exports. This is infrastructure evidence, not strength or final ABI
acceptance. Earlier design details remain at `40b3871c:scratch/agent-9039d61b.md`.

Remaining work is explicit:

1. **ETU-75 integration in ETU-89:** `manabot/model/world.py` is absent here.
   Consume its ordinary `checkpoint_world`/`validate_checkpoint_world` contract,
   pass actual deck/sideboard `player_configs` to `save_bc_checkpoint`, and bind
   selected recipes to `semantic_pack="ur-lessons-vs-gw-allies"`. Preserve
   `semantic_cards` and `known_hand` through collection/training. Native w4 alone
   does not establish tensor or checkpoint compatibility. No parallel format.
2. **ETU-90 integration:** checkpoint `8076e877` supplies the tested
   `update_ema` helper (average parameters, copy buffers, once per iteration,
   including empty-filter skips). This checkout still interpolates parameters
   inline. ETU-90 may replace the call after parent sync. Its trainer env shim
   must retain collector match for ordinary `Trainer.save` admission. The
   reported 14-game/1024-transition raw/EMA proof predates ETU-75.
3. **ETU-89 acceptance:** after integration, repeat a bounded real multi-stage
   execution, reload immutable outputs with the ordinary loader, and validate
   world rejection, CLI ambiguity, fixed splits, optimizer continuation,
   interruption and failed-stage retention. Earlier checks remain evidence;
   final gate owns the integrated check. Actual demo games are separate chapter
   evidence and are not established by arena reload alone.
4. **ETU-91 acceptance:** Jack Heart's latest steer reports checkpoint
   `52d222df`, resolved protocols, common-cost analysis, retained failed attempts
   and offline integrity checks. Its preliminary learning smoke completed 24
   replayed games in 104 seconds with unchanged metrics across two offline
   regenerations. This report is not independently rerun here. The final two
   studies require ETU-75 and ETU-90 integration. Stacked `lf task sync` selects
   its parent automatically and refuses an explicit sibling target; ETU-90 must
   reach ETU-91 through the parent or land before final study acceptance.

ETU-91's final smoke requirements remain two real checkpoint measurements,
complete four-leg paired comparisons plus a fixed random anchor, exact replay,
executed notebooks and unchanged metrics on offline regeneration. Both studies
have 15-minute smoke caps; the ablation smoke covers five arms and at least two
updates. Named extra contrasts retain bounded optimizer fixtures. Unsupported
competencies and unfunded studies remain explicit not-run evidence. The
three-anchor scientific cohort and expensive profiles remain proposals.

The retained smoke training seed family begins at 10197 (teacher 10197–10200;
conservative self-play bound 10268), disjoint from study seeds 910001/920001.
This bound applies to those saved executions only. Longer runs need an explicit
seed-family check before scoring. No scientific improvement, exploitation
resistance or human-challenger result has been measured by these smokes.

Open budget/scope decisions remain in `questions.md`; none blocks bounded
infrastructure work. Frozen expensive studies still require an accepted budget,
protocol and measured timing allowance. No expensive training is authorized.

Check result: prior `uv run pytest tests/training/test_regimes.py tests/sim/test_search_supervised.py -q` — 23 passed (6.62 s); realign inspected code and retained records without rerunning tests; integrated gate deferred until ETU-75/90 integration.

Gate (2026-10-04): `uv run pytest tests/training/test_regimes.py tests/sim/test_search_supervised.py tests/sim/test_net_opponent.py -q` — 30 passed; after cumulative-cost change, `uv run pytest tests/training/test_regimes.py -q` — 12 passed; `uv run pytest tests/sim/test_distill.py tests/sim/test_distill_datagen.py -q` — 5 passed; `cargo test --manifest-path managym/Cargo.toml --lib agent::vector_env::tests` — 6 debug tests passed; scoped Ruff lint/format and `git diff --check` passed. Full CI matrix remains CI-owned. ETU-75's absent `manabot/model/world.py` and ETU-90 EMA integration still block final integrated acceptance; ETU-91 final study smokes remain with their owner.

Jack Heart requested exact checkpoint cost cutoffs during gate. Completed stages
now freeze `StageRecord.cumulative_seconds` at admission from run start,
including prior persistence. A real two-stage continuation test injects delayed
persistence and verifies the later checkpoint includes it without changing the
earlier cost. Older records retain null. ETU-91 should consume this field rather
than reconstructing cost from setup plus stage durations. The public contract
is documented in `docs/training-regimes.md`.
