# One-step search updates: findings and bounded comparison

2026-10-14. Research contribution for **lf-e0e4bd2**, requested by Jack Heart.
Scope: `research-brief.md` and `research-handoff.md`; findings review only.
Inspected source: `9576dc40ef486966246e20d9fdf58e5d741f1c40`.

## Accepted experiment inputs — 2026-10-14

Jack Heart agreed to use existing trained policies and **no learned beliefs**.
Use the physical-compatible deal prior for every search arm. No learned-sampler
fitting, artifact substitution or physical-versus-learned comparison belongs to
this experiment set. Historical learned-sampler evidence below remains context.

The proposed policy cohort is ETU-118's final raw 10,000-update checkpoints,
seeds 11851, 11852 and 11853; pilot seed 11851 is selected in advance. Exact bytes,
hashes, signed-value semantics and world/setup admission remain to be verified.
These are observation-only sequential policies on w4 UR Lessons versus GW Allies,
not trained compound policies. Preserve their original decks and sideboards.
Define recursive reference probabilities against their actual authoritative
action structure; do not claim a trained-compound comparison from this cohort.

The hidden-world prior and the action reference are distinct: the former samples
physically compatible deals; the latter supplies recursive-uniform action
preferences in MMD. Both remain independent of a learned belief model.

## Decision

**Full MMD is already implemented.** The narrow experiment is to ablate the
existing `regularized_update` call after local rollout aggregation, retaining
the same evidence. Do not add another planner or reimplement the formula.
The code supports KL-only by setting `alpha=0`; the current local selector is
already the full-MMD control. Raw policy and Q-argmax supply distinct controls.
Actual flat-MC and PUCT selection need separately labeled panels because they
produce different evidence, budgets and continuation policies.

The formula is correct for the stated objective. Whether either regularizer
improves current-world play is **unmeasured in the inspected evidence**. Software
delivery, toy complete-loop proofs, and old-world arena results do not establish
that effect. The highest-value next selection is a small, paired root-evidence
study, followed only if separately authorized by a frozen held-out arena cohort.

## Evidence registry and proof limits

Paths below are relative to this repository at the inspected commit. Cached Task
reads used `lf task status MTG-{95,99,100,107} --json`; all reported disconnected
sync and stale planning. Their descriptions are historical context, not live
authority to launch work. The manifest's Wave directory is absent. Neither gap
prevents this bounded contribution; no planning repair was attempted.

| Evidence | Observation | Exact limit or gap |
| --- | --- | --- |
| [MTG-95 / historical ETU-95](https://linear.app/loopflow/issue/ETU-95), [local-search contracts](../docs/local-policy-search.md), `local_update.py`, `local_sampling.py` | Delivered frozen-policy rollout, direct physical/learned sampling, retained targets and replay. Documented initial toy proof: 4 games, 318 labels, 9.94 s; it predates final validation edits. | Ignored proof artifacts were not loaded or re-admitted here. No selected-matchup benefit. Complete-history exact posterior remains unsupported. |
| [MTG-100 / ETU-100](https://linear.app/loopflow/issue/ETU-100), [PR 221](https://github.com/loopflowstudio/etude/pull/221), `local_compound.py`, v3 receipt validation | Exact compound conditional support, including legal payment offers with zero base mass; no smoothing, suffix resampling or flat-head substitution. | Fixed-weight correctness evidence, not trained strength. Cached PR reports merge `db820056de813a874ea89cb51f213639b007e389`. |
| [MTG-99 / ETU-99](https://linear.app/loopflow/issue/ETU-99), [transfer protocol](../experiments/ataraxos-transfer.md), especially B2 | Repository protocol is dated October 5, prospective and unexecuted; specifies policy/prior/learned comparisons and distinguishes realized cost from ceilings. | Cached Task state says completed. That state does not supply a result for its empirical questions; no scored MMD-vs-KL-only cohort was found. Preserve this discrepancy rather than infer success. |
| [MTG-107 / ETU-107](https://linear.app/loopflow/issue/ETU-107), existing compound code | Broader model-interface design requires its own review. | This proposal uses existing semantic offer identities and retained prefixes; it selects no new action representation. |
| [INT-7](../experiments/int-7-value-target-comparison.md), retained manifest `3f7a00e179fe49fe111ff8a361501ca8080e501fa7189abeaacb66194a5de5bf` | `continue_visit_policy_only`; improved value calibration accompanied weaker complete PUCT players. Manifest explicitly says `engineering_smoke_only_no_admission_claim`. | One 507-row teacher corpus; initialization seeds are not independent data seeds. World w2, not w4. |
| [INT-8](../experiments/int-8-student-signal-guidance.md), retained result namespace `64779c48ab1f3c9d54fbd697a373666ada7333840058cab88494e9ccf129b38e` | `kill_retained_smoke_policy_guidance`: chosen/visit priors failed arena and label-agreement gates against uniform priors. | Tiny w2 cohort, with a reported visit-32 latency outlier. Evidence against assuming every learned prior helps, not against current MMD. |
| [INT-17](../experiments/int-17-belief-calibration.md), failure receipt namespace `78bde491e16957b743a59cebe6f87fd519dc982793d5d6f7dbb649a98d57e027` | Inspected failure JSON: 5,876 wall s, 5,078.04 CPU s, 3 completed updates, no curves, `evidence_wait_rules_materialization_provider`. | Systems failure, not a negative calibration score. Historical quadratic materialization cause must not be assumed to persist in current direct sampling. |
| [exp-10](../experiments/exp-10-value-gate.md), `experiments/data/exp-10-value-gate.json` | Corrected deal-diverse value-search gate passed: 60.25% vs V-greedy; matched-wall comparison against random-rollout search failed at 38.5%. | Earlier battery invalidated by repeated deals; training saw three deals and the cap was exceeded. Preserve both correction and failure. This is not a current-world MMD result. |

Current source identifies world **w4** in `manabot/README.md` and `WORLDS.md`.
Historical INT-7 policy seed 197 is explicitly w2 in `search_runtime.py`:
checkpoint SHA `1673a237ef2460d0e699667987c29fe6b42c28711bdb2041989f37692edbd1e6`,
observation ABI `d7da94347d956dd492039d55a10291bcdc1b2605e59f67dfe7af66d3fbbbaaa5`,
action ABI `9f1290e4db495c9a299df0bbf06f19fd02cf1eabc62b435f8b029ddd5f6257b2`.
These are registry identities, not fresh byte-verification or current admission.
No checkpoint was selected or loaded for a new cohort.

## How evidence becomes an action

### Flat and PUCT paths

- `FlatMCPlayer.act` (`manabot/sim/flat_mc.py:100`) calls native
  `flat_mc_scores`, then takes the first argmax. This is a point-mass behavior
  distribution, not a normalized vector of scores. Worlds are shared across
  legal root actions; continuations are uniformly random legal actions. Values
  are root win/draw/loss scores 1/.5/0; step caps also score .5 and are counted.
  `sims` is per action, resolved to worlds × rollouts with integer rounding.
  Current `Game::determinize` preserves known-hand minima and reshuffles residual
  uncertainty, unlike a naive unconditional hand shuffle.
- `determinized_puct` (`mcts.py:380`) uses a **total traversal** budget across
  worlds. Each world owns a separate adaptive tree. Root priors are computed
  once, then copied. `_select_action` uses acting-seat Q plus
  `c_puct * prior * sqrt(total+1)/(visits+1)`; opponent nodes use `1-Q`.
  `DeterminizedPuctPlayer.act` chooses maximum visits, breaks ties by Q, then
  array order. Normalized visits are teacher targets, not its play distribution.
- Default PUCT uses uniform priors and random terminal playouts.
  `AgentLeafEvaluator` uses a frozen policy softmax and **sigmoid** value head,
  with a neutral-.5 mode. That historical win-logit convention differs from
  local search's signed critic. A world-compatible shape alone does not certify
  critic semantics; do not feed a signed categorical/scalar critic through this
  sigmoid and call it the same evaluator.
- PUCT aggregates value sums divided by visits; unvisited entries are filled
  with .5. Different actions can have different world visitation weights.
  Such entries are not complete equal-world action estimates. Independently
  optimized per-world trees also permit strategy fusion even when neural inputs
  are viewer-limited. Replacing only final selection cannot remove that bias.

### Existing local / compound path

The path is `make_player(kind="local_update")` → `LocalUpdatePlayer` history →
`LocalUpdateTeacher.search` → shared sampled worlds → per-action frozen-policy
rollouts → signed means → `regularized_update` → sampled action. Arena registration
pins the implementation source; private receipts retain branch Commands.

| Quantity | Actual owner and meaning |
| --- | --- |
| Raw trained policy `p0` | `predict`, `local_update.py:507`: exact checkpoint forward on the acting player's observation. Compound: `project_compound` on the **original viewer root plus retained token/Command prefix**. It is the raw conditional next-Command distribution, not the flat head or a previous search target. |
| Action magnet `rho` | `local_update.py:664`: uniform over current semantic offers, strictly positive, independent of Q. This is neither the hidden-world prior nor PUCT exploration priors. Uniform offers can overweight semantically redundant encodings; no claim of strategic neutrality. |
| Belief / world sampler | `SearchHandSampler`, `PreparedHands`, `HandBatch`: physical-compatible hand measure (not uniform count vectors), or an artifact-bound learned count sampler. Sampler bytes/schema/dataset/generating-policy/world are checked. Native materialization owns legal worlds. |
| Continuation and value | Same frozen checkpoint. Ordinary actions use actor-view observations each step; compound rollouts drain one conditional declaration using its original context before admitting a new policy root. No gradient or optimizer state. |
| Q | Each positive-base-support action gets one branch per sampled world. Depth counts canonical decisions including the forced root action. Terminal values are −1/0/+1; actor-relative leaf values are sign-flipped to root viewer. Categorical WDL gives signed expectation; admitted scalar signed critics remain unbounded. |
| Output / provenance | `regularized-local-update/v3`: offer IDs, base/Q/reference/target, counts, seeds, policy/native/source identities, world constraints/history, sampled hands, per-branch values, actor hashes and Command witnesses. Unsupported actions have base/target/count zero and Q null. Allocation counts are not PUCT visits. |

Both production samplers reject non-`True` conditional queries. The explicit
`sampling="belief"` reference enumerates and checks its support cap afterward;
it is unsuitable as a large-pool fallback. Compound exact-history likelihood and
belief-input-policy rollout memory are rejected. A learned sampler's policy
binding does not make its posterior correct for a foreign opponent.

Materialization checks root viewer hash and semantic offer equality before
branching (`local_update.py:733`). Branch inference uses its acting viewer;
root aggregation precedes selection. Compound projection rejects actor/revision
interruptions and suffix-dependent prefix values. These are information-safety
mechanisms, not proof of equilibrium consistency across all information sets.

**Narrow boundary:** keep everything through `values = sums/counts` fixed and
compare selectors at `local_update.py:827`. Keep v1/v2/v3 receipts immutable;
put prospective derived contrasts beside the original receipt, naming its hash
and their coefficient settings. Do not overwrite `target` or rewrite schemas.

## Mathematical and primary-source check

For support S where `p0(a)>0`, maximize

`F(p) = sum_a p(a) Q(a) - beta KL(p||p0) - alpha KL(p||rho)`,

with `beta=1/eta>0`, `alpha>=0`. At an interior optimum on S, stationarity gives

`Q(a) - beta(log(p(a)/p0(a))+1) - alpha(log(p(a)/rho(a))+1) = constant`.

Thus

`p*(a) = softmax_S((Q(a)+beta log p0(a)+alpha log rho(a))/(beta+alpha))`.

The Hessian on S has diagonal `-(alpha+beta)/p(a)`, so the objective is strictly
concave there and this is the unique optimum. Substituting `beta=1/eta` yields
the guide's powers `p0^(1/(1+eta alpha)) rho^(eta alpha/(1+eta alpha))`
and exponent `eta Q/(1+eta alpha)`. With `alpha=0`, it is `p0 exp(eta Q)`.
This derivation concerns a fixed Q vector; it proves neither Q accuracy nor
improvement against the actual opponent.

The [ICLR 2024 update-equivalence paper, §3.2](https://arxiv.org/html/2304.13138v3)
states this two-KL objective and closed form. Its game-theoretic improvement
argument has algorithmic assumptions; it is not a guarantee for arbitrary
truncated, biased manabot estimates. The [ICLR 2023 MMD paper](https://arxiv.org/html/2206.05825v4)
is the underlying regularized-update source, not evidence of an MTG outcome.

The [Ataraxos supplement, S3.7 equations (7)–(8), Table S12](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-11036-y/MediaObjects/41586_2026_11036_MOESM1_ESM.pdf)
matches this objective using beta as the trained-network KL coefficient. Its
settings are alpha .002, beta .02, about 1,000 total rollouts and depth 40;
hidden configurations number roughly 1,000 divided by legal moves. These are
not manabot's defaults (.02, 1, one world, depth 2).

The [Nature methods](https://www.nature.com/articles/s41586-026-11036-y)
describe fixed-network continuations and a sampled tabular update. Their magnet
selects a movable piece, then a move, uniformly at each level. The
[Extended Data Table 1 caption](https://www.nature.com/articles/s41586-026-11036-y/tables/1)
specifically identifies removing KL **to the move network** as causing performance
below the raw network. It does not establish the independent benefit of the
magnet in MTG. These sources were checked directly during this pass.

### Units, support and numerical contract

- Use signed root outcomes for the primary local panel. For a genuine
  probability score `q`, `Q=2q-1`; preserving the optimizer requires doubling
  both alpha and beta (equivalently halving eta). Mere rescaling without these
  changes alters the treatment. An arbitrary neural scalar is not a probability.
- Mask illegal actions before normalization, with canonical offer IDs rather
  than positional assumptions across worlds. The current function receives an
  already legal vector. Keep exactly the positive base support; no epsilon
  smoothing or invented Q for inaccessible offers.
- General reverse KL would intersect base and magnet support for alpha>0.
  **Current API intentionally requires positive rho everywhere**, even at
  alpha=0. A zero magnet must be rejected, not silently accommodated.
- Implementation uses float64, log weights, max subtraction and normalization.
  Nonfinite supported Q/parameters, malformed probabilities and underflow that
  destroys supported target mass fail. Off-support Q may be NaN. Large finite
  scalar values can still cause rejection; record the failure, do not clip.
- Constant Q leaves the KL-only policy unchanged; full MMD can still move it
  toward rho. Uniform rho makes the log-rho term constant, but alpha still
  changes the denominator and base exponent. It is an entropy treatment, not
  a no-op. Eta approaching zero recovers p0 when rho is positive.

## Local checks performed and probes specified

Pre-execution limits were recorded in [questions.md](questions.md). One offline,
standard-library Python 3.12 process through uv evaluated five algebraic fixtures
and a 1,001-point two-action grid. No project imports, engine, checkpoint, GPU,
training or dependencies were used. All five assertions passed: objective-grid
maximum, additive-value invariance, signed/probability unit conversion, constant-Q
KL-only identity, and inaccessible-support independence. Fixture
`p0=(.2,.8), Q=(-1,1), rho=(.5,.5), alpha=.3, beta=2` gave
`p*=(.11154671719820757,.8884532828017924)`.

Measured inner probe cost: **0.000730 wall s, 0.000729 CPU s**, excluding uv and
interpreter startup; tool command returned in under one second. Paid resource
spend $0; engine transitions, training steps and checkpoint loads all zero.
Research reading/tool time was not metered as an experiment. This arithmetic
probe validates the derivation, **not the production NumPy implementation**.
No `.venv` exists here, so native/pytest verification was specified, not executed.

Existing probe owners, to run later in an admitted environment without training:

| Probe | Existing evidence and exact acceptance |
| --- | --- |
| Optimum / zero support | `tests/sim/test_local_update.py::test_two_kl_optimum_and_shift_invariance` and `test_zero_support_update_is_the_restricted_simplex_optimum`; equal active-coordinate gradients and immutable zeros. Add alpha-zero, unit-conversion, permutation, extreme-logit rejection fixtures when implementing a contrast consumer. |
| Root information boundary | `test_real_root_replay_and_hidden_swap`: same root information, varied actual hidden world, same sampler seeds → identical target and unchanged source witness. Different sampled worlds may legitimately change Q; never demand invariant outputs across genuinely different actor information states. |
| Compound semantics | `tests/sim/test_local_update_compound.py`: payment joint parity, supported-root-to-payment replay, saved compound teacher, interrupted prefix, wide offers. Require original-root conditional parity, prefix-value independence and no suffix resampling. |
| Sampler identity / cost | `tests/sim/test_local_update_sampling.py`: direct lifecycle, injected sampler validation and post-sampling deadline. Same complete batch across selector arms; invalid preparation, stale history or deadline gives unavailable evidence, not policy fallback. |
| Native execution | Retain ordinary debug Rust checks for any later native change. This research changes no Rust and rebuilds no shared runtime. |

Analytical counterexample, also evaluated by the probe: raw `p0=(.9,.1)`,
true signed Q `(.6,-.6)`, biased search Q `(-.2,.2)`. KL-only at eta 1, 4, 16
assigns the wrong action .1422, .3550, .9853 and yields true expected scores
.4294, .1740, −.5823 (raw: .48). This demonstrates the danger of increasing
step size under systematic bias. It is **not an observed rollout-count curve**.
At fixed eta, more draws can concentrate an estimate around the wrong mean;
the prospective test below separates that effect from increasing eta.

## Prospective bounded protocol — not authorized execution

### 1. Freeze and audit before scoring

Use an existing admitted w4 raw checkpoint with its signed critic, exact world,
rules/content/decks/sideboards/Lesson pool, observation/action/compound schemas,
architecture receipt and source/native hashes. Record original producer cost,
checkpoint hash, raw/EMA choice and selection rule. Do not substitute an old w2
INT checkpoint. No current checkpoint or learned-sampler pair was admitted here;
this is an explicit launch prerequisite, not a placeholder result.

Use existing TrainingRun/VerifyStore collection, local receipts and arena/replay
instruments. The ordinary study `EvaluationProtocol` is policy-only; a selector
contrast consumer and explicit arena-cell registration/analysis are still needed.
They are narrow integration work requiring later selection, not a second runner.

Proposed first-stage cap: one CPU worker/thread, no GPU, **15 wall minutes and
15 core minutes**, 1 GiB retained outputs, 64 nonterminal roots from at least
16 whole saved games. Reserve 8 games for development and 8 for held-out roots
before examining outcomes; at most 4 roots per game, fixed chronological sampling
rule, record every excluded/unsupported root. Incompatible saved trajectories
mean stop with a missing-input result, not generate a new training campaign.
All timeouts, admission failures, replay and analysis cost count toward the cap.

### 2. One realized evidence batch, all root selectors

At each root use direct physical sampling first; `full_probability=1`, depth 2,
world counts 1/2/4/8 as nested prefixes of one 8-world receipt. Derive Q for each
prefix from retained branch rows, preserving actual continuation RNG, canonical
Commands, actor observations and terminal/leaf evaluator. Each selector sees
the **same batch**, not independent reruns with nominally matching seeds.

| Arm | Distribution from that one receipt |
| --- | --- |
| Raw policy | Exactly retained `base`; consumes no Q but is evaluated alongside the same evidence. |
| Current local selection | Exactly retained `target` at alpha .02, beta 1; recomputation must agree. |
| KL-only | Existing function, alpha 0, beta 1; same base/Q/rho. |
| Full MMD | Existing function, alpha .02, beta 1: deliberately identical to current local selection, serving as a wiring check rather than a fourth independent method. |
| Q-argmax diagnostic | First maximum supported Q, point mass; matches the local-argmax target convention. This is not mislabeled as the actual flat-MC or PUCT player. |

Development-only sensitivity: beta `{.25,1,4}` at alpha `{0,.02}`, fixed signed
units and uniform-offer rho. Freeze one KL-only/full pair before held-out scoring;
keep the default pair separately labeled. No value-dependent temperature or
uncertainty-adaptive trust is introduced. Do not fit a structured magnet here.

If historical flat/PUCT behavior is included, use separate same-root panels:
produce that planner's evidence once, then compute raw, its actual selection,
KL-only and full MMD on that evidence. Pin a semantically compatible checkpoint
for raw/base and keep the generator unchanged. Flat's current selector is Q
argmax; PUCT's is visit argmax with Q tie breaking. PUCT update entries lacking
observations on base support must be unavailable, not .5 pseudo-evidence;
report coverage and world weighting. Such a panel measures selection on adaptive
PUCT evidence, not Ataraxos fixed-policy rollout equivalence. It is optional and
outside the first-stage cap unless explicitly traded into that cap before launch.

Shared evidence gives **exactly equal realized search work** for root contrasts.
Report its generation cost once in program totals and attribute it fully to each
standalone search method; report selector overhead separately. Raw policy's
deployment cost remains one policy inference. Do not claim it intrinsically
costs as much as shadow search, or pad its timing with artificial work.

### 3. Belief error and becoming confidently wrong

The main comparisons use the same physical-compatible deal prior throughout.
The optional synthetic sensitivity diagnostic below perturbs explicit legal
world weights without fitting any belief model. Within each fixed treatment,
preserve selector arms on the same sampled batch. Different treatments cannot
literally share their sampled worlds; report that distinction.

For a tiny exact-information fixture, predeclare a finite legal world distribution
with known weights. Tilt those weights toward an incorrect but legal hand class
by mixture fractions `{0,.25,.5}` and freeze them before selection. Truth and
reference action values are scoring-only. This is a synthetic belief-bias panel,
not an allowed impersonation of an admitted production sampler: its identity
must be distinct, and no injected sampler may claim the original distribution.
If the existing fixture boundary cannot express it honestly, leave it specified.

Measure signed expected regret against fixture reference values, chosen wrong
action mass, entropy, `KL(target||base)` in nats, L1 shift, supported action count,
per-action/world Q variability and disagreement with raw. For a predeclared
wrong-action set (true gap at least .1 signed units), define “more confidently
wrong” as increasing probability mass on that set with world count at **fixed**
beta, accompanied by increasing reference regret. Keep eta sensitivity separate.
For real game roots, a single terminal outcome is not ground-truth Q; report
outcome associations, not certified root errors.

### 4. Separate held-out full-game confirmation

Only after review and explicit empirical allocation: propose up to **4 wall/core
hours**, one worker, no training, and 24 paired deal blocks × four deck/seat legs
× four distinct policies (raw, KL-only, full MMD, PUCT) = **384 games maximum** against
two frozen compatible opponents (raw and PUCT), 12 blocks each. The PUCT opponent
is the same frozen configuration as the PUCT candidate, giving a direct MMD–PUCT
comparison as well as comparisons against common opponents. This smaller block
count trades precision for the requested additional method within the same cap.
Use disjoint deal lists from producer data and development where receipts permit
verification. If historical training membership is unavailable, state the limit.
This first cohort is conditional on one checkpoint, not population-level proof.

Freeze calibrated world count from `{1,2,4,8}`, depth 2, coefficients and a proposed
200 ms decision ceiling on development roots. If no count fits, stop; do not
increase the envelope after seeing held-out results. Record p50/p95/max latency,
CPU, transitions, forwards, materialization, decoder factors, cap/failed-game
counts and per-game actual cost. Native operations can overrun cooperative checks;
use the existing arena outer subprocess deadline. No fallback, replacement draws
or counting incomplete games as draws. Hitting the overall cap yields incomplete
evidence and no acceptance claim.

In full games actions diverge, so later information sets and rollouts cannot stay
identical across policies. Pair initial deals/seats/opponents and budgets, and
label this an outcome confirmation, **not exact shared-rollout isolation**.
Require search-arm mean realized per-game costs within 10% for a matched-cost
claim; otherwise retain cost imbalance. Raw policy remains its honest cheaper
baseline. The PUCT comparison is an algorithm comparison, not another root
selector on the same rollout evidence. Use the same admitted checkpoint and
information-safe world distribution where the current interfaces permit it;
keep the existing PUCT tree and selection rule. Its current sigmoid leaf adapter
must not reinterpret a signed critic: an explicit, tested value-semantic adapter
is a launch prerequisite. Match measured inference cost, not traversal counts.
Freeze PUCT exploration and traversal/world settings using development data with
the same tuning allowance as local search. Where sampler or evaluator parity is
unavailable, label that configuration difference; do not claim an isolated search
algorithm effect. More general MCTS variants remain outside this comparison.

Primary contrast: full-MMD minus KL-only effective score (win 1/draw .5/loss 0),
averaging the four legs per deal block. Predeclare a practically useful difference
of .02 and a paired block 95% interval wholly above zero for a positive conditional
signal; a wholly negative interval is negative, otherwise inconclusive. Report
raw comparisons and opponent/deck breakdowns without using them to reselect
coefficients. Bootstrap whole deal blocks, never individual decisions. Method
generalization requires separately selected independent producer checkpoints;
do not manufacture replication from repeated deals on one network.

The direct MMD–PUCT result is a predeclared secondary contrast with its own paired
interval and measured costs. It does not establish that the magnetic term caused
any advantage; the shared-evidence KL-only contrast addresses that question.

## Subsequent direction: recursive reference and PUCT comparison

Jack Heart requested a PUCT/MCTS comparison and agreed on recursive-aware
uniformity on 2026-10-14. These choices refine the proposed design; no empirical
execution or production implementation occurred in this research pass.

**Current reference:** `local_update.py:664` sets `rho(a)=1/n` over the current
canonical semantic offers, including compound projections. “Fixed” means a fixed
rule independent of search Q, not the same vector in every position. This is an
entropy incentive over the current offer vector. It is not a uniform distribution
over complete compound declarations. Compound training already documents
conditional legal uniforms at decoder factors (`training/compound.py:288`), which
need not induce a uniform marginal over the canonical Commands used by search.

**Selected reference direction:** uniform over legal children at each stage of
the authoritative action-construction hierarchy. For a declaration path
`c1,...,ck`, its reference probability is the product of the conditional factors
`1 / number_of_legal_children(prefix)`. Forced factors contribute one. For a
canonical next Command, sum the probability of every construction path lowering
to that Command, conditional on the retained prefix; integrate unselected suffixes.
This is the same probability boundary used for the learned compound projection,
but with fixed conditional uniforms in place of learned scores.

For example, if one legal top-level choice has ten continuations and another has
one, recursive uniformity gives each top-level choice half the mass; individual
leaves get .05 and .5 respectively. Uniformity over the eleven complete leaves
would instead allocate 10/11 to the first choice. This illustrates the definition,
not a claim that today's root offers enumerate all target/payment combinations.

The hierarchy itself expresses a prior. Reuse engine-owned legality and the
existing compound grammar; do not invent action families from string labels.
Do not cross reveals, opponent decisions or native interruption boundaries. A
legal child must have an admitted completion. Avoid enumerating all declarations;
use conditional structure and the existing projection machinery, with exhaustive
normalization only on tiny reference fixtures. Aliased orderings must use the
same path-to-Command aggregation contract as actual execution.

Preserve exact base zeros. A recursive reference may assign zero to canonical
offers inaccessible under the declaration grammar, whereas today's update API
requires rho positive everywhere. Resolve that contract explicitly in later
implementation: the reference must be positive on every positive-base action;
off-support zeros need support-aware validation. Never conceal the difference
with epsilon smoothing or change historical receipt meanings. Test reference
normalization, tiny-tree hand calculations, prefix conditioning, canonical
aggregation, hidden-world invariance and payment support before scoring.

Retain three shared-evidence local controls: KL-only, MMD with today's uniform
offers, and MMD with recursive reference. Hold alpha/beta fixed for the initial
reference contrast. The full-game MMD candidate uses the recursive reference only
after that implementation and its identity are frozen; otherwise that arm is
unavailable, not silently substituted. Keep the offer-uniform arm in the root
panel rather than expanding the proposed game cap. Structured references,
frozen learned anchors and removing the magnet are reasonable alternatives, but
no current-world win-rate evidence selects among them. A reference equal to the
raw policy merely combines the two KL coefficients into stronger trust, where
support validation permits it; it is not an independent magnetic preference.

## Review disposition

### Added subgoal: train and compare compound policies

Jack Heart subsequently selected training compound policies as a subgoal and
comparing them against non-compound policies. No learned beliefs remains a firm
constraint. This adds proposed training work; no training allocation or execution
has occurred. It does not authorize the broader MTG-107 interface redesign.

Use the existing `train_compound` pipeline and authoritative decoder. The current
`compound-sequential-outcome.json` recipe provides a concrete starting point:
w4 curated matchup, observation-only model, 64-dimensional encoder, sequential
factor credit and terminal-outcome targets. Its two one-update stages are a
workflow demonstration, not a strength-training budget or a validated recipe.

Two comparisons answer different questions:

1. **Practical benchmark:** new compound checkpoints versus ETU-118 final raw
   non-compound checkpoints, without search. Preserve the original training costs
   and label any recipe/budget differences. This measures which available player
   is stronger, not a causal effect of compound representation.
2. **Matched training experiment:** three paired initialization/run seeds, each
   training one non-compound and one compound policy: six main training runs.
   Use the same world, full deck/sideboard setup, reward, shared encoder capacity,
   hardware and measured training-compute allowance. A preceding short pair
   calibrates complete-game collection, optimizer, export, evaluation and replay
   costs; its data are development-only. Freeze the main budget and recipe before
   those six runs. Pair evaluation deals, not stochastic training trajectories.

Existing compound training and the ETU-118 Ataraxos recipe differ in learning
rules as well as representation. A clean representation claim requires a common
admitted learning rule with explicit factor/group credit and regularization
semantics. If that is unavailable, report the comparison as two complete recipes;
do not silently attribute a PPO-versus-Ataraxos difference to compound decisions.
Record parameter counts, canonical Commands, decoder factors, games, optimizer
exposures and actual compute; equal update counts are not equal work.

Evaluate final-raw checkpoints selected at the frozen cutoff, with intermediate
learning curves at common observed costs. Primary outcome is compound versus
non-compound direct held-out play with both deck assignments and seats. Add common
frozen opponents to expose nontransitivity and deck-specific regressions. Include
initialization comparisons, failure rates and decoding latency. Three seed pairs
support a first screen, not a precise population-level effect. Keep all attempts;
do not choose the best seed or checkpoint from held-out performance.

Search comparisons then run **within each policy family**: raw, KL-only,
offer-uniform MMD, recursive-uniform MMD and PUCT at declared cost. This separates
whether compound training helps from whether search helps a compound policy.
All search arms use the physical-compatible prior. Compound-aware PUCT needs
verified retained-prefix/critic semantics before admission; the ordinary flat
`AgentLeafEvaluator` is not a compound adapter. Defer that cell explicitly if the
interface is unavailable, rather than evaluating the unrelated flat head.

The earlier 384-game proposal and later conversational search-screen sizes are
provisional designs, not cumulative authorized allocations. Recalculate the full
matrix and cost after the short training pair; do not automatically multiply the
entire search program by the added training axis.

The root-update mechanism is delivered and mathematically consistent; its
current-world benefit remains an empirical question. Select the paired evidence
consumer/probes first if this report is accepted. Do not launch MTG-99's wider
belief/distillation/robustness program, alter MTG-107's interface review, or promote
the local teacher into Academy advice from this result. No production files,
frozen experiments, training processes, PRs or Task/Wave state were changed.
