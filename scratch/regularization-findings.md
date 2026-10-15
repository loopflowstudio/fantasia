# Strategic regularization and update control in manabot

2026-10-14 · Task lf-85fb3bd · findings for review

Requested by Jack Heart in the supplied [brief](research-brief.md) and
[handoff](research-handoff.md). This is one bounded research pass, not an
implementation, allocation, recipe promotion, or continuation of inherited
auto-code. Source inspected: `9576dc40ef486966246e20d9fdf58e5d741f1c40`.
MTG task names below refer to the requested work; retained `ETU-*` identities
and paths are preserved verbatim.

**Decision:** keep the existing recipe as a control. The implementation already
separates sampled-ratio clipping, collection-policy KL and fixed-reference KL.
The retained MTG-105 screen does not compare these mechanisms. Before attributing
entropy changes to regularization, measure distributions at identical decisions,
including action-encoding collisions. The smallest next measurement is a bounded
replay of frozen roots; the smallest subsequent learning comparison is the
existing collection-KL pair with prior and other controls held fixed.

The most consequential qualification is that high entropy can be forced by the
ordinary policy representation: attack and decline-attack have identical action
features. Changing regularization cannot make this policy distinguish them.
This is a source-derived boundary for the separate MTG-107 architecture review,
not authorization to change that architecture here.

## Evidence registry and proof limits

| Evidence | What it supports | Exact remaining gap |
| --- | --- | --- |
| [Collection](../manabot/sim/net_opponent.py), `SeatRoutedCollector.collect`, `_build_batch`, `transition_gae`; [executor](../manabot/training/execution.py), self-play stage | Saved behavior distributions, same-viewer transitions, bootstrap and optimizer sequencing | No new real-game execution in this checkout |
| [Move loss](../manabot/training/ataraxos.py), [PPO regime loss](../manabot/training/objectives.py), [references](../manabot/training/references.py), [numerical distribution rules](../manabot/model/policy_distribution.py), [health](../manabot/training/health.py) | Exact mathematical objectives, gradient ownership, support and diagnostic semantics | No causal strength comparison of KL or priors |
| [Native action types](../managym/src/agent/action.rs), [offer generation](../managym/src/flow/action.rs), [observation projection](../managym/src/agent/observation.rs), [encoding](../managym/src/agent/observation_encoder.rs), [Agent](../manabot/model/agent.py) | Legal-offer families and feature collisions in ordinary flat policy | Incidence and outcome cost on retained checkpoints are unmeasured |
| [MTG-92 adaptation](../docs/ataraxos.md), [MTG-93 controls](../experiments/ataraxos-omitted-controls.md), their objective/runtime tests | Implemented controls and historical bounded integration proof | Those proofs are not scientific replications or strength evidence |
| [MTG-105 report](../experiments/ataraxos-technique-screen.md), [compressed evidence](../experiments/data/etu105/filter-scope-mini.json.gz), [analysis](../experiments/data/etu105/analysis.json), [closeout](../experiments/data/etu105/closeout.json) | Completed scalar filter-scope screen, uncertainty, cost and failed attempts | No collection-KL/prior ablation; no full fixed-state checkpoint distributions in the compact bundle |
| [This pass's diagnostics](regularization-diagnostics.json), [script](regularization-probe.py) | Retained identity extraction and exact arithmetic on eight constructed distributions | Not native-root, trained-policy, gradient, or performance measurements |

The supplied guide is scientific direction, not evidence of a manabot effect.
Existing tests were inspected, not rerun: no `.venv` or native extension is
present. All 48 paths in MTG-105's local-backup receipt are absent **in this
checkout**. That does not contradict the producer's historical verified-copy
receipt or establish loss of its artifacts. No other checkout or host was used.

## What the optimizer actually compares

### Entry points and data flow

`uv run manabot train --regime ... --out ...` validates a `TrainingRegime` and
dispatches through `execute_regime`. The MTG-92/93/105 controls use its ordinary
`TrainSelfPlay` stage, `SeatRoutedCollector`, and the optimizer owned by
`NetOpponentTrainer`/`Trainer`. `Learning` selects the PPO regime update;
`AtaraxosMoveLearning` selects the damped move update. The ordinary
`uv run manabot train --preset ...` path instead reaches the stock trainer.
Calling all three paths simply “PPO” obscures meaningful differences.

Each collector stream saves the acting learner's observation, sampled action,
selected log probability, **full** masked behavior probabilities and normalized
log probabilities, and scalar or categorical outcome prediction. A transition
ends at that same learner's next decision or game termination; intervening
opponent actions get no learner policy-gradient row. Terminal rewards are from
the learner's perspective, and truncation fails rather than becoming a draw.
The next observation is paused before sampling its action.

Parameters are fixed during collection. Raw-self uses current learner weights
for self-play; EMA-self uses averaged weights and bootstraps from that same
pre-update averaged model. Games can span updates. The saved behavior is the
policy that actually sampled the action, not a reconstructed “previous model.”
These are fresh, close-to-on-policy batches, not full episodes under immutable
weights and not trajectory-level importance correction.

Let `p` be the current legal-action distribution, `b` the saved collection
distribution, `rho` the prior at the same observation, and `a` the sampled action.
For a retained actor row the move loss is

\[
 L_\pi=-\min(r\hat A,\operatorname{clip}(r,1-\epsilon,1+\epsilon)\hat A)
       +\beta\sum_{j\in L}p_j\log(p_j/b_j)
       +\tau\sum_{j\in L}p_j\log(p_j/\rho_j),\qquad r=p_a/b_a.
\]

Both sums are `KL(current || target)`; “reverse KL” in repository names means
this explicit orientation. Clipping sees one sampled ratio. The KL terms see
every legal offer at that row. Neither is a hard bound on the final update.
There is no exact optimization over a free policy simplex: Adam updates shared
network parameters, with gradient clipping, minibatches and a critic loss.
This is not a tabular mirror-descent step.

For the move recipe, detached policy advantages use gamma=1 and lambda=.5;
value targets use lambda=.8. The categorical critic learns soft loss/draw/win
lambda targets by cross-entropy; its scalar ablation uses mean squared error.
The policy and critic losses have equal weight. Inclusive absolute-advantage
quantile .75 plus floor .01 select rows before training. One epoch processes
increasing learner-timestep minibatches, without advantage normalization.
Actual ratios matter even in one epoch because earlier timestep minibatches
change the learner before later ones.

Behavior, references, advantages and targets are constants for differentiation.
Current policy/value logits and shared encoder receive gradients. The default
filter applies to actor and critic. With `filter_scope="actor"`, the surrogate
**and both KLs** use selected actor rows but the critic uses all rows. An empty
actor set therefore does not prevent policy movement through the shared encoder.
An empty actor+critic set skips Adam; the EMA iteration clock still advances.

Adam uses inherited betas .9/.999 and epsilon 1e-5. The move defaults are ratio
radius .2, collection KL coefficient .1, max gradient norm .267,
`LR(i)=clip(.5/i^1.1, 5e-6, 1e-4)` and `tau(i)=.05/i^.3`, on a one-based
collection/update clock. EMA .999 advances after the update, including skips.
Gradient norm clipping acts on the joint loss before Adam; it is not a bound on
parameter displacement or policy KL. Numerical health measures parameter movement
on the first optimizer step at iteration 1 and every 25th iteration.

The PPO **regime** uses the same two KL types but independently configurable
traces, selected-row advantage normalization, shuffled multi-epoch minibatches,
and `.5*MSE` times `value_weight`. Its configured progress clock can be elapsed
budget or iteration fraction. The stock **preset trainer** instead has an
explicit `-ent_coef*H(p)` bonus, optional clipped value loss, and sampled
`mean((r-1)-log(r))` for target-KL early stopping. Under exact expectation over
`b`, that estimator corresponds to `KL(b || p)`, not the regime's full
`KL(p || b)`. Finite-sample stopping and ratio clipping still do not enforce a
hard trust region. See [stock `_optimize_step`](../manabot/model/train.py).

### Why reference choice changes the scientific question

Encoded-uniform means `rho(a)=1/N` for N legal offers. At a fixed observation,

\[
 KL(p\|\mathrm{Uniform}_N)=\log N-H(p).
\]

Thus fixed-reference KL to uniform and an entropy bonus of the same coefficient
have identical policy gradients on the **same rows**, although their logged
losses differ. This is a myopic state loss, not entropy-to-go. Changing the
collector, selected rows, normalization, optimizer, or schedules invalidates an
“entropy versus KL” equivalence claim for the whole experiment.

The implemented structured prior is only **action-type uniform**. If G types
are present and type g has n_g offers, `rho(a)=1/(G*n_g)`. It gives equal total
mass to each type, then equal mass within that type. Its KL decomposes into
family-mass KL to uniform plus policy-weighted conditional within-family KL.
Equivalently it is `-H(p)+log G+E_p[log n_g]`. This compensates offer counts at
the type level; it does not balance source cards, targets, modal semantics or
complete payment outcomes within a type. A “fixed” prior is a fixed rule
conditioned on the state's legal offers, not one action vector for every state.

The prior can resist loss of a rare type, but can also overweight pass, decline
or poor types. It cannot certify useful exploration or equilibrium mixing.
Collection KL instead resists departure from whatever behavior already does,
including bad or collapsed behavior. At `p=b` its gradient is zero; after
earlier minibatches, or initially under EMA behavior, it can be nonzero.
The uniform prior can still exert a gradient at that same point.

## Legal support, encodings and entropy

The engine owns legality. The ordinary encoder emits a one-hot action type,
validity, and object-focus indices. Its capacity validation rejects too many
offers/focus objects before the internal bounded encoding loop; the `.take`
inside that loop alone is not evidence of silent legal-action truncation.
The MTG-105 receipt uses a 64-action capacity. Runtime schemas must be pinned;
neither a smaller tensor nor a subset of offers is an interchangeable world.

| Decision | Encoded-uniform versus action-type uniform | Consequence / limit |
| --- | --- | --- |
| Priority: 4 casts, 1 land, 1 pass | Uniform assigns mass 2/3, 1/6, 1/6; type uniform assigns 1/3 each | Different strategic prior even with identical legal support |
| Required target choice | Usually all `ChooseTarget`, so the priors coincide | No balancing of target categories or source spells |
| Optional target: 3 targets plus decline | Target mass 3/4 versus 1/2 | Structured prior changes continuation/stopping propensity |
| Waterbend: 3 eligible taps plus pay remainder | Tap mass 3/4 versus 1/2 | Can change mana-versus-permanent use; still uniform among taps |
| Learn: 2 Lessons, 3 discard candidates, decline | Mass 1/3, 1/2, 1/6 versus 1/3 each | Distinct choice priors; duplicate card copies still count separately |
| Attacker yes/no | Both offers are `DeclareAttacker`; both priors are 1/2, 1/2 | Representation forces the same distribution in the ordinary flat Agent |
| Blocker target / no block | One type with differing focus lengths | Priors coincide, though the model can distinguish these offers |
| Forced action | Probability 1, entropy/KLs zero | Declining aggregate entropy can simply reflect more forced states |

**Important counterexample to the guide's general encoding concern:**
[`compute_player_actions`](../managym/src/flow/action.rs) emits a cast per
castable card, followed later by target/payment prompts. It does not enumerate
every target/payment combination as a priority action. More targets therefore
do not directly increase that spell's priority mass. They can increase
conditional choice entropy and the number of subsequent training rows.
Ordinary mana-source payment is not represented as a Cartesian menu here.

Waterbend can have multiple sequential tap paths to the same selected set.
Whether two paths are strategically equivalent requires checking final state,
triggers and information, not comparing labels. The structured-offer path
already canonicalizes selected tap IDs and rejects duplicates
([`InternalOffer::Waterbend`](../managym/src/agent/structured_offer.rs)); do not
assume those permutation aliases survive there. Different tapped permanents
can matter strategically. Repeated copies are not automatically redundant.

**Observed representation, derived policy consequence:**
[`flow/tick.rs`](../managym/src/flow/tick.rs) offers true/false for the same
attacker. `Observation::action_focus` gives both the same permanent;
`ActionOption.declared` retains the distinction for presentation, but
`encode_actions` does not encode that field. The ordinary Agent scores identical
type/focus features with shared row-wise layers. Consequently their logits
coincide for all weights, giving exactly 50/50 stochastic play when those are
the two offers. This is not learned equilibrium mixing. Modal choices similarly
omit mode index, and multiple activated abilities on one permanent omit ability
index from the ordinary action features. Their occurrence in the screened
matchup is not measured here. These are feature collisions between potentially
different outcomes, distinct from redundant encodings of the same outcome.

The separate compound trainer is not a silent fix or drop-in control:
[`optimize_games`](../manabot/training/compound.py) regularizes conditional
distributions at retained behavior prefixes. Summing those conditionals does
not give exact joint `KL(new || behavior)`, which needs new-policy prefix
occupancy. Conditional uniform is not uniform over completed subsets.
Keep compound factorization and search-specific trust regularization outside
this comparison.

**Support:** both implemented priors are positive on every legal offer and zero
on padding. `policy_logs` uses a legal mask, finite normalized legal logs and
`-inf` on padding. Invalid masks, empty support and inconsistent stored behavior
are rejected. Move loss rejects zero prior probability on legal actions.
In the mathematical forward-from-current KL, a true target zero with positive
current mass makes KL infinite; a zero-support scripted prior would prohibit
those actions. It would need an explicit full-support mixture, not an epsilon
introduced unnoticed into this experiment.

Finite float32 sampling can nevertheless underflow legal `exp(log p)` to zero.
The saved legal log remains finite, KL uses logs, and health counts underflow;
there is no probability floor. Thus nominal log-space support and realized
exploration differ. A sampled action must have positive saved sampling mass.
These invariants are covered by existing numerical-health and gradient tests,
not newly demonstrated at a trained checkpoint here.

## Fixed-state diagnostics obtained in this pass

These are **constructed offer sets**, not native states, learned outputs or a
reproduction of MTG-105. All values are nats. Full vectors and both KL
orientations are in [regularization-diagnostics.json](regularization-diagnostics.json).
The first five examples use encoded-uniform as behavior b except attacker,
which is already 50/50.

| Constructed decision | p | H(p) | KL(p‖b) | KL(p‖type-uniform) |
| --- | --- | ---: | ---: | ---: |
| Priority: casts, land, pass | .1,.1,.1,.1,.1,.5 | 1.497866 | .293893 | .155264 |
| Three targets, decline | .2,.2,.2,.4 | 1.332179 | .054115 | .020136 |
| Three taps, pay | .2,.2,.2,.4 | 1.332179 | .054115 | .020136 |
| Attacker yes/no | .5,.5 | .693147 | 0 | 0 |
| Learn: Lessons, discards, decline | .1,.1,.1,.1,.1,.5 | 1.497866 | .293893 | .068959 |
| Forced pass | 1 | 0 | 0 | 0 |

Two discriminating counterexamples were also calculated:

- If four encodings truly denote one equivalent outcome, uniform encoding
  entropy is 1.386294 while outcome entropy is zero. This is a hypothetical
  equivalence class, not a finding that four actual casts are equivalent.
- With `b=(.2,.4,.4)`, `p=(.2,.79,.01)` and sampled action 0, the sampled ratio
  is exactly 1 and its clip indicator zero, yet `KL(p||b)=.500760` and
  `KL(b||p)=1.203324`. A small clip fraction is not a whole-policy guarantee.

Real fixed-root diagnostics must retain full masks, ordered native action
identities, p, b when collection evidence exists, both priors, family mass,
entropy and both KL directions. At arbitrary replay roots a preceding
checkpoint distribution is **checkpoint drift**, not the actual collection KL.
Do not relabel it. Use `H(p)/log N` only when N>1, with forced rows separate;
also report family entropy and conditional entropy. Semantic-equivalence
entropy requires validated equivalence classes.

## What MTG-105 actually measured

The retained mini experiment completed on 2026-10-07. It compares only
actor+critic filtering with actor-only filtering on a two-layer width-64,
four-head semantic model with **scalar masked-mean critic**, authored
Allies/Lessons w4, raw-self behavior, four streams × 64 transitions, one CPU
thread, float32, action-type prior and collection KL .1. Three paired training
seeds 10501–10503 each ran 1,240 updates / 317,440 learner transitions.
The categorical move preset and separate proposed contrasts are not this run.

Final held-out greedy scores were 42.00% [35.67,47.67] for actor+critic and
45.33% [40.00,49.67] for actor-only. Paired seed effects were +7,+7,−4 percentage
points; mean +3.33 [−4.33,+11.33]. Actor-only cost 1.45× mean training wall time
(6,714.61 versus 4,626.75 seconds). The common observed cost-window contrast
was −2.33 [−7.33,+2.67] points; the strict one-hour cutoff gave +2.33
[−4.33,+9.00], using sparse earlier exports. Random-opponent difference was
+2.33 [−4.00,+9.67]. These are descriptive paired-seed/common-deal bootstrap
intervals, with only three training seeds; they neither prove benefit nor
equivalence. The older +5-point program threshold was not separately
preregistered for this mini. Keep actor+critic as its unpromoted control.

The retained final-100-update means illustrate the limitation of aggregate
optimization diagnostics:

| Seed | Filter | Entropy | Reference KL | Collection KL |
| --- | --- | ---: | ---: | ---: |
| 10501 | actor+critic | .728750 | .312098 | .004183 |
| 10501 | actor-only | .704259 | .279290 | .001768 |
| 10502 | actor+critic | .896198 | .197177 | .001218 |
| 10502 | actor-only | .680558 | .298331 | .003197 |
| 10503 | actor+critic | .790793 | .261415 | .002091 |
| 10503 | actor-only | .650372 | .301080 | .004548 |

These are averages of per-update **last executed minibatch** diagnostics, not
all-row epoch averages or fixed-state comparisons. The logits were computed
before that minibatch's optimizer step; logging occurs afterward without a
fresh forward. Under actor-only filtering the move diagnostics average all
rows of the executed timestep, while the actor objective averages selected
rows. Under actor+critic they see the selected population. Occupancy and sample
populations change too. Neither lower value loss nor lower entropy establishes
better held-out learning. The compact bundle omits per-update selection groups.

Batch-tail bootstrap fractions were about 98–100%. No complete-return claim
follows. LR remains at its upper clamp for iterations 1–2305, so this 1,240-step
screen cannot measure LR decay. All 3,600 scientific monitoring/final games
terminated with exact replay and no recorded legality, private-exposure or
truncation failures. That supports evaluation integrity, not broad robustness
or replay of every training update.

Earlier failed preflight, two process-inspection `PermissionError` calibrations,
a terminated supervisor with a completed child, and its successful continuation
remain recorded. Original reserve arithmetic undercounted monitoring cohorts
and final evaluation multipliers. No failed attempt or accounting error is
removed from interpretation. Closeout reports 34,024.10 training seconds,
34,273.64 scientific wall seconds, 40,056.35 additive worker-process seconds,
and 2,834.21 final arena seconds; overlapping clocks must not be summed again.
Conservative elapsed time from first preflight through closeout was 61,353.34 s.
Owned-host dollar pricing is unavailable; no paid resource was launched.
S3 publication remained credential-blocked; W&B receipts are not model backups.

The separate [ETU-118 dated baseline note](../experiments/current-baseline.md)
records later 10,000-update training and development improvements, with final
acceptance still unjudged at that note's observation time. It is counterevidence
to a blanket claim that the recipe cannot learn, but not an isolated KL/prior
comparison. No live status or final outcome was inferred or fetched here.

### Identity ledger

Full six-run recipes, endpoints and hashes are extracted in the diagnostics
artifact. Representative control endpoint: seed 10501, TrainingRun
`4e71b2de1dd54e689faa42f10c5f8e09`, raw SHA-256
`f8d903cbfb53255475ca5aa811447a4030d7a54eb8319d09669f052a1a303b74`.
Its paired actor-only endpoint is
`15d58f892e9dec659efd2156ec129bd7bdd0f9999f74028bd005b0917954b1b5`.

| Identity | Retained value |
| --- | --- |
| Actual training source | `a108ed3428a7f8c363a28c7df5dc71a4cd8d2719` plus the three archived repairs |
| Python source bundle | `1e822ce38c8fe55c7672f0c98c6e9df3414ffaa15064e5f9c84ac692b7fb8694` |
| Native extension | `f12d239e1034b0f4f7f2e820da5e1fce10c4bc426dd56d511214e641d4e1fa8b` |
| World / content | w4 / `dca9ab421ff18dc33546a35a0555c9817c302267f8fe21ff75d247e1600ce124` |
| Observation ABI | `b28c5dd6144d2b847fce54de773ffb08f514f8142498905b67f3833ff0e40d47` |
| Action ABI | `388cad683f617fae7c39bd515be1f28c2966c7414b47877559093ab2e7eacddf` |
| Matchup | `5b46db09a613880980ac8fbd5d0942fe24d5465ff0789984cc75709adf7be343` |

The incidental `source_commit=eac2535f...` in TrainingRuns came from the parent
checkout and is **not** the exported Python source identity. Historical
producer paths are preserved, not rebound to this checkout. Current source
inspection is not proof of byte-identical historical implementation.

## Source-check of the paper claims that affect this decision

The final Nature Methods explicitly separates prior regularization from four
update controls: collection-policy KL, ratio clipping, gradient clipping and
Adam learning rate. The move prior samples a movable piece then a legal move;
the setup process uses entropy. Ablations remove components from the final
configuration without retuning other hyperparameters. They support usefulness
within that configuration, not superiority of coordinated schedules over
independently retuned schedules or transfer to MTG.
[Sokota et al., Nature, Methods and Extended Data Fig. 5](https://www.nature.com/articles/s41586-026-11036-y).

The supplement S3.4, equation (6), directly contains the clipped surrogate and
both oriented KL terms. Equation (5) is categorical outcome cross-entropy.
Table S7 specifies .2 ratio clipping, .1 collection KL, .267 gradient cap,
.5/.8 traces, the two iteration power laws, one epoch and .999 evaluation EMA.
This confirms the implemented recipe's stated source, with MTG changes to
action grouping, decision clock and model. It does not supply an equilibrium
guarantee for this neural implementation.
[Supplement, S3.4 and Table S7](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-11036-y/MediaObjects/41586_2026_11036_MOESM1_ESM.pdf).

The distinction from mirror descent is substantive: the MMD paper's equilibrium
and tabular results concern its specified algorithm, not arbitrary Adam losses
containing KL. PPO likewise introduces a surrogate optimization method, not a
universal final-policy KL constraint.
[MMD paper](https://arxiv.org/abs/2206.05825),
[PPO paper](https://arxiv.org/abs/1707.06347).
Search-specific objectives and ablation interpretation remain with the MMD task;
no training recommendation here depends on the guide's search-result claim.

## Prospective bounded protocol — not executed or allocated

### First: establish real fixed-root evidence

Propose a five-minute, one-thread CPU measurement, no optimizer updates, at
most 256 frozen viewer-safe roots × three existing raw checkpoints. Reuse
arena `replay_prefix`, normal checkpoint admission and `Agent` forward/log
normalization, with scenario/root identities in the existing evidence store.
Do not use the old initial-policy script's custom default deck, deterministic
argmax and fallback stepping as a scientific replacement for that path.

Before execution, bind root replay hashes/command offsets, acting viewer,
full native offers, encoded observations, source/native/content/schema/setup
identities, checkpoint digests and the root partition. Allocate up to 32 roots
each to priority, attack, block, target, payment, Learn/selection, modal/scry,
and forced decisions. Report unavailable strata; never manufacture them under
a checkpoint's different setup. Rare custom scenarios require compatible
checkpoint admission. Partition by whole game before selecting roots.

Measure the quantities specified above, offer permutation/padding invariance,
zero illegal mass, nonempty legal support, legal underflow, type/focus collision
groups, and equality of allegedly aliased logits. Check true native actions
rather than labels when testing equivalence. A failure in the predicted attack
equality would falsify the source model and require tracing the actual runtime
path before changing regularization. Evaluate reference-KL gradients at the
same frozen logits if desired, without applying an optimizer step. Actual
collection KL requires retained b; otherwise mark it unavailable.

Prerequisites missing here are native runtime and compatible model/root bytes.
Their absence is a completed research finding, not a reason to launch training
or fetch another active experiment. If the proposed cap cannot cover the pinned
panel, retain partial measurements as incomplete rather than selecting favorable
states. This measurement alone makes no strength claim.

### Smallest learning comparison, then isolated prior contrasts

Use the existing MTG-92/93 controls and MTG-105 `collection-kl` contrast through
`Experiment`/`ResolvedStudy`, the existing training-regime runner, arena, replay
and study report. No second runner is needed. Freeze the scalar MTG-105 model
and other recipe settings for continuity; the technique generator's default is
categorical with a value token, so both `value_kind="scalar"` and
`value_aggregation="masked_mean"` must be explicit in both resolved arms.
Do not silently use a PPO-package or architecture change as the comparison.

The first scientific screen would compare beta=.1 against beta=0 with the
same action-type prior and tau schedule. Hypothesis: beta=.1 reduces fixed-root
policy movement/tail KL and improves held-out robustness; alternative: it only
slows useful adaptation or has negligible effect under the other controls.
Collecting lower training KL alone would support control of movement, not
strategic benefit.

After that, the clean design to distinguish update control and strategic prior
is a 2×3 factorial, not a bundled algorithm swap:

| Fixed-prior treatment | beta=0 | beta=.1 |
| --- | --- | --- |
| tau=0 | sampled clipping / norm / LR controls only | add collection KL |
| tau=.05/i^.3, offer uniform | add entropy-equivalent regularization | both controls |
| tau=.05/i^.3, type uniform | change strategic prior at same coefficient | both controls with type prior |

Keep clip=.2, gradient cap=.267, Adam, traces, filtering, behavior, model,
streams, initialization, raw endpoint selection and all other schedules fixed.
Do not create two redundant tau=0 arms distinguished only by unused reference.
The prior contrast is type-uniform versus offer-uniform; the tau contrast is
uniform versus zero; the beta contrast and interaction are separately
estimable. A later ratio-radius .2/.1 comparison is already implemented and
would isolate sampled-ratio control. Do not add it to this first screen.

**Proposed limits:** three new paired training seeds, 1,000 updates per cell,
four × 64 learner transitions/update, maximum 5,400 active training seconds per
run, one learner thread on an available owned host. First pair: at most 9 hours
training plus 2 hours evaluation and 1 hour preparation/diagnostics/failures,
12 hours total. Full 18-run factorial instead: 27 hours training, 8 evaluation,
2 calibration, 2 diagnostics/reporting and 9 reserve, 48 hours total. These are
ceilings, not throughput predictions or permission. Calibrate full-game
evaluation before freezing either cohort; if it cannot fit with 25% margin,
revise the proposal before scientific runs, not the scored sample afterward.
One thousand updates deliberately tests early regularization only, while LR
is clamped; it cannot answer long-run schedule or equilibrium questions.

Equal updates fix collected learner transitions but do not fix selected rows,
optimizer exposures, native decisions or wall cost. Report both an update-matched
endpoint and cost-matched curves. Predeclare exports at 0/250/500/750/1000
updates and prospective 900/1800/2700/3600-second cutoffs; use the last actually
available artifact at each cutoff, compare only common observed support, and
report checkpoint age/update lag. No interpolation, best-checkpoint selection
or substitution for a missing endpoint. Pin the current cadence facility needed
to export these cutoffs; if only step cadence is used, keep cost comparisons
explicitly sparse and secondary.

**Evaluation and uncertainty:** prefreeze disjoint development and final whole-game
deal families, 32 final four-leg paired-deal blocks per checkpoint/opponent,
both seat/deck assignments, stochastic raw one-pass CPU inference, and a fixed
three-opponent panel: scripted greedy, random diagnostic, and a compatible
frozen historical trained anchor. All anchor hashes and fresh seed/deal ranges
must be admitted before launch; none is selected by later scores. This is
2,304 final games for the first pair, 6,912 for all six cells. If the trained
anchor is unavailable, report a blocked robustness protocol rather than claim
that greedy/random exhaust strategic diversity. New deck generalization needs
its own compatible-world cohort; it cannot be inferred from two seat assignments.

Report per-seed effects and paired-seed/shared-deal bootstrap intervals,
resampling complete four-leg blocks and preserving cross-arm pairing. Three
seeds provide descriptive screening uncertainty, not a confirmatory claim.
Primary screen criterion proposed in advance: at least +5 percentage points
on the equal-weight greedy/trained-anchor held-out score, paired 95% interval
above zero, and no more than a 5-point regression on either primary anchor.
Random is diagnostic. Also report worst-anchor score and all family diagnostics.
No promotion follows from entropy, training KL, or a favorable single seed.
A larger independent-seed confirmation would need a new accepted budget;
failure to clear this threshold is not proof of equivalence.

Track all available decision families, legal-action counts, forced rows,
selection fractions, actor/critic exposures, clipping indicators, gradient norm
before/after cap, parameter changes, actual post-update fixed-root KL, and
reference/family entropy. Separate occupancy-weighted summaries from fixed-root
strata. Positive mass on illegal actions, hidden-information leakage, wrong
world/schema/setup, nonfinite loss/gradients, unreplayable games or capacity
overflow stop a cell and retain its evidence. Budget exhaustion leaves the
cohort incomplete; do not replace seeds or stop because scores look favorable.
Charge initialization, training, exports, monitoring, replay, failures and
reporting, keeping overlapping wall/process clocks separate.

## This pass's execution receipt and unresolved conclusions

Limits were recorded in [questions.md](questions.md) before probes. Three
offline Python 3.12.12 standard-library invocations completed: two evidence
inspections (0.05955 and 0.06025 s) and one retained diagnostic calculation
(0.06220 s), each inside a 60-second alarm. Each read 15,099,233 decompressed
bytes of the same retained bundle, below the 64 MiB cap. The arithmetic script
checks normalization and the entropy/uniform-KL identity. These approximately
0.182 seconds measure probe bodies only, excluding process setup and research
reading. No probe failed. No training, optimizer step, native game, paid
resource, external message, experiment modification, Task launch or PR occurred.
Current-run model/world identity is absent because no model was executed;
historical identities are recorded above, not claimed as a current runtime.

Still unmeasured: real fixed-state checkpoint distributions and final-update
KL; frequency/strategic cost of feature collisions and redundant paths;
family-conditioned entropy changes under equal state occupancy; causal benefit
of either KL coefficient or reference choice; held-out historical-opponent
robustness for those contrasts; long-run schedule interaction; equilibrium or
exploitability. Existing scalar diagnostics do not answer these questions.

Findings and protocol are ready for review. Implementation, empirical allocation,
architecture disposition, search regularization, publication and delivery remain
outside this completed pass.
