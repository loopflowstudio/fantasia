# Ataraxos lessons and experiment ownership

2026-10-04. Jack Heart requested an explicit owner for every lesson identified
in the Ataraxos discussion, the supplied ledger review, and the technical review.
This is a coverage map, not a claim that proposed techniques work. Linear owns
Task execution state. Existing running protocols remain frozen; future studies
need their own resolved recipes, budgets and fresh evaluation deals.

## Current foundation

[ETU-89](https://linear.app/loopflow/issue/ETU-89) owns executable TrainingRegime
stages and TrainingRun records. [ETU-90](https://linear.app/loopflow/issue/ETU-90)
owns collector correctness and the implemented PPO-based controls.
[ETU-91](https://linear.app/loopflow/issue/ETU-91) owns planned runs plus an
EvaluationProtocol, notebooks, reports and the active scientific comparisons.
The active campaign retains its original PPO-control recipes. Later implementations
do not retroactively change that cohort or turn its results into a test of the
complete paper method.

The current screen compares control, separate value estimators, filtering,
coordinated decay and their combination. It is not the complete method inventory.
The current teacher is fixed uniform-prior determinized PUCT; it does not improve
from the student. The main RL arm is frozen independently of screen results.

## Landed mechanisms and evidence

- [PR #206](https://github.com/loopflowstudio/etude/pull/206) adds the source-verified
  Ataraxos move recipe: categorical outcomes, inclusive filtering, iteration
  schedules and evaluation EMA. The paper itself uses clipped per-action ratios
  and two reverse-KL terms; clipping is not evidence of a different algorithm.
  MTG adaptations and unresolved source details are explicit in `docs/ataraxos.md`.
  Gradient/runtime checks and raw/EMA-to-belief integration passed; matched-cost
  scientific strength remains unmeasured.
- [PR #205](https://github.com/loopflowstudio/etude/pull/205) adds frozen-policy
  collection and constrained belief fitting. A bounded three-game pilot proves
  execution, not calibration under foreign policies or wider card pools.
- [PR #208](https://github.com/loopflowstudio/etude/pull/208) adds compound attacker
  declarations and supported targeted casts, four credit-assignment treatments,
  and a 56-game replayed workflow. Blockers, payments and intervening information
  remain separate; this does not establish faster learning.
- [PR #207](https://github.com/loopflowstudio/etude/pull/207) adds bounded single-stage
  CPU recovery, including abrupt process death and Ataraxos state equivalence.
  Full-loop hardware calibration and multi-stage recovery remain open.
- [PR #209](https://github.com/loopflowstudio/etude/pull/209) landed with all CI
  checks passing. Its attack runner passed a 24-game replayed
  workflow and a real-PPO toy positive control. It has not attacked the main
  scientific policies. Historical S1–S5 contrasts resolve, but their custom decks
  are explicitly unsupported for selected-match checkpoint scoring.
- [PR #210](https://github.com/loopflowstudio/etude/pull/210) adds independent
  executable contrasts for omitted controls, actor-only filtering, inclusive
  quantiles, EMA collection with matching probabilities and bootstrap values,
  and raw/EMA evaluation without double-counting training seeds. Its 48-game
  replayed workflow and focused checks prove execution, not treatment benefit.
  Independent full-episode terminal-return residual analysis is added by PR #215.
- [PR #211](https://github.com/loopflowstudio/etude/pull/211) adds frozen-policy
  local rollout updates, retained regularized targets and repeated distillation
  stages. The bounded proof used a tractable two-name pool; selected-matchup
  strength and full-game exact histories are not established. Its advice
  projection is not a registered live advice provider.
- [PR #212](https://github.com/loopflowstudio/etude/pull/212) admits compound raw
  policy exports to belief collection and fitting, with per-game policy reset
  and explicit observation-capacity limits. This does not admit compound policies
  to local-search rollouts.
- [PR #213](https://github.com/loopflowstudio/etude/pull/213) adds a bounded CPU
  full-loop calibration command using existing study/TrainingRun records,
  separate replay accounting and measured device/thread evidence. Eight complete
  games replayed in its workflow proof. Concurrent timing does not establish
  uncontended throughput; MPS/CUDA calibration remains unsupported.
- [PR #214](https://github.com/loopflowstudio/etude/pull/214) connects learned
  hand-count samples directly to native rollout worlds without enumerating
  support. The bounded policy→belief→search→student pipeline completed; its
  trained artifacts played two arena games with 183 exactly replayed commands.
  Learned beliefs remain approximate, queries unconditional, and broader
  calibration and playing strength unmeasured.
- [PR #215](https://github.com/loopflowstudio/etude/pull/215) adds frozen complete-game
  filtering diagnostics with separate terminal-outcome and lambda-target
  residuals, whole-game uncertainty and offline regeneration. Its four-game
  example replayed 1,073 decisions exactly. Terminal outcomes are noisy samples,
  not ground-truth expected values; association does not establish causal benefit.

These are delivery receipts, not Task completion claims. ETU-95 owns the
remaining post-training search integration.
Linear remains authoritative for their live execution state.

## Coverage

| Lesson or open question | Explicit owner | Current boundary |
| --- | --- | --- |
| Paper's damped move gradient, per-action ratios and on-policy assumptions | [ETU-92](https://linear.app/loopflow/issue/ETU-92) | Landed move recipe and equation/gradient checks; scientific comparison remains open |
| Exact paper schedules, estimators and categorical win/loss/draw critic | ETU-92 | Final supplement audited; categorical and scalar recipes landed with explicit MTG adaptations |
| Gamma, policy trace and value trace address different horizons | [ETU-93](https://linear.app/loopflow/issue/ETU-93) | Gamma=1 and separate critic traces exist; higher policy trace is outside active screen |
| Structured-uniform reference rather than mass proportional to offer count | ETU-93 | Implemented option; current scientific arms use offer-uniform |
| Coordinated LR/reference decay, collection-policy KL, separate schedule effects | ETU-93 | Controls exist; screen does not isolate every coefficient or interaction |
| Advantage filtering by magnitude/quantile and action type | ETU-93 | Top-count and inclusive-quantile contrasts plus action-type diagnostics landed; comparative benefit unmeasured |
| Actor-only filtering versus filtering the critic too; critic-error and terminal-proximity selection bias | ETU-93 | Both loss scopes and held-out complete-game residual diagnostics landed; benefits and true expected-value error remain unestablished |
| Raw versus averaged weights; averaging for evaluation versus actual behavior | ETU-93 | Separate evaluation and behavior contrasts landed; frozen active studies still use raw weights and learner-driven collection |
| Auxiliary predictions and value representation as learning accelerators | ETU-92 / ETU-93 | Explicit architecture hypotheses; do not silently bundle with gradient changes |
| Compound attacks/blocks/targets/payments and joint log probability | [ETU-94](https://linear.app/loopflow/issue/ETU-94) | Attacker declarations and supported targeted casts landed; blockers/payments remain separate |
| Forced/optionless steps and honest underlying-decision accounting | ETU-94 | Audit existing auto-resolution; collapsing prompts is not a strength result |
| Setup-style outcome-only versus bootstrapped compound-decision credit | ETU-94 | Transfer hypothesis, not assumed equivalent to Stratego setup |
| Freeze a strong policy before belief-conditioned search; consistent beliefs, rollouts and value | [ETU-95](https://linear.app/loopflow/issue/ETU-95) | Compare policy-only, uniform and same-policy exact beliefs at equal decision time |
| One regularized local search update and its distillation target | ETU-95 | Retain full generating identities; old per-action scores alone are insufficient |
| Hard targets, visits and regularized soft targets; mixed strategy and bluffing | ETU-95 | Measure behavior and strength; soft targets do not guarantee sound mixing |
| Improving search teacher versus the current fixed teacher | ETU-95 | Test compounding only after a useful policy/value model exists |
| Selective search effort, replay/cumulative reuse and relabeling economics | ETU-95 | KataGo-inspired hypotheses; charge all searches and retain target versions |
| Frozen-policy self-play with hidden truth as labels; belief model trained afterward | [ETU-96](https://linear.app/loopflow/issue/ETU-96) | Policy→dataset→belief stages landed; broad calibration and search comparisons remain open |
| Constrained autoregressive joint beliefs versus exact enumeration | ETU-96 | Measure legality, calibration, joint likelihood, latency and search strength |
| Learned hand samples actually drive policy rollouts without enumerating support | ETU-95 / ETU-96 | Direct native materialization and artifact-bound search landed; conditional queries, broader calibration and strength remain open |
| Foreign-policy histories, opponent adaptation and belief-training dropout | ETU-96 | Self-play calibration is not immunity to baiting or distribution shift |
| Stronger exploiters, historical opponents and weak control play | [ETU-97](https://linear.app/loopflow/issue/ETU-97) | Independent attack seeds and increasing budgets; failed attack is not a certificate |
| INT-6 arena and S1–S5 as judges; deck/seat and world identity | ETU-91 / ETU-97 | Revalidate scenario premises and historical ratings before reuse |
| Equal-cost learning speed, independent seeds, untouched endpoints and notebooks | ETU-91 | Active experiment; no winner established by smoke/calibration |
| Full-loop throughput, CPU/MPS batching, cloning, hardware projections and recovery | [ETU-98](https://linear.app/loopflow/issue/ETU-98) | Inference observations/s are not training steps/s; no paid-compute projection accepted |

## Evidence limits carried into the Tasks

The supplied ledger review names exp-03/07/09/10/11 and INT-7/8/17. Their
historical results motivate new comparisons; they do not establish universal
teacher ceilings or rule out model-free learning at useful scale. The exact
historical numbers must be checked in their original world and budget before
reuse. The quoted H100 price and games/week estimate is not a measured budget.

Search remains part of Etude's advice experience. Policy-only evaluation isolates
the source of trained strength. Hidden information does not categorically forbid
search teachers; it makes their policy/belief assumptions and improvement operator
important. Neither policy-gradient training nor soft labels alone establish
better bluffing, equilibrium, or immunity to exploitation.

The future Tasks require standalone acceptance and full-game evidence. Their
capture does not expand the current 168-hour campaign or change its active plans.

## Search integration contracts and remaining acceptance

Jack Heart set sampling as the default direction for belief-conditioned search
on 2026-10-04. Production search should consume constrained joint hidden-state
samples without enumerating possible hands. Keep exact enumeration as a
small-pool correctness and calibration reference, not a prerequisite for the
sampling path. Compare a constrained prior sampler with learned sampling;
learning must earn its complexity through better predictions or decisions.
Evaluate public-constraint validity, joint dependencies, sensitivity to sample
count, and playing strength at matched realized cost. This direction does not
change the frozen campaign or authorize additional compute.

ETU-95 now connects the frozen-policy belief sampler to rollouts directly.
The learned path validates public pool counts, known minima, hand size and
source observation identity, preserves the root viewer's information, and
retains reproducible world/rollout seeds. Native tests cover direct/indexed
parity, hidden-hand swaps and stale/impossible inputs. The old indexed path
remains available for enumerated references; learned samples do not pass
through that enumeration. Belief artifact, generating policy and feature
schema identities remain bound in receipts.

Scientific acceptance still requires comparing learned sampling with the
compatible physical-deal prior under the same realized compute accounting,
on a separately frozen evaluation population. The bounded pipeline does not
establish calibration under foreign policies, conditional query mass or a
strength gain. These remaining requirements allocate no additional long run.

The separate exact-history reference has a different gap: opponent combat and
targeting commitments are not represented by the current public likelihood
schema, and ordinary discard prompts cannot be refreshed by the materializer.
Only publicly committed information may condition that reference. Private
subchoices cannot be exposed to make posterior updates convenient. Full-game
exact acceptance remains open until those contracts and history transport are
proved; a learned approximate posterior must never be labeled exact.
