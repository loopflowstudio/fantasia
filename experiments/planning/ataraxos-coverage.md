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
These are distinct from a paper-faithful damped-gradient implementation.

The current screen compares control, separate value estimators, filtering,
coordinated decay and their combination. It is not the complete method inventory.
The current teacher is fixed uniform-prior determinized PUCT; it does not improve
from the student. The main RL arm is frozen independently of screen results.

## Coverage

| Lesson or open question | Explicit owner | Current boundary |
| --- | --- | --- |
| Paper's actual damped policy gradient; on-policy assumptions versus PPO ratios and clipping | [ETU-92](https://linear.app/loopflow/issue/ETU-92) | New selectable algorithm, equation-level paper/supplement audit and analytic gradient checks required |
| Exact paper schedules, estimators and categorical win/loss/draw critic | ETU-92 | Verify final supplement; distinguish scalar MTG adaptations |
| Gamma, policy trace and value trace address different horizons | [ETU-93](https://linear.app/loopflow/issue/ETU-93) | Gamma=1 and separate critic traces exist; higher policy trace is outside active screen |
| Structured-uniform reference rather than mass proportional to offer count | ETU-93 | Implemented option; current scientific arms use offer-uniform |
| Coordinated LR/reference decay, collection-policy KL, separate schedule effects | ETU-93 | Controls exist; screen does not isolate every coefficient or interaction |
| Advantage filtering by magnitude/quantile and action type | ETU-93 | Current top-half filter needs comparison with verified paper treatment |
| Actor-only filtering versus filtering the critic too; critic-error and terminal-proximity selection bias | ETU-93 | Current implementation filters all losses; benefit is a hypothesis |
| Raw versus averaged weights; averaging for evaluation versus actual behavior | ETU-93 | EMA export exists; active studies use raw weights and learner-driven collection |
| Auxiliary predictions and value representation as learning accelerators | ETU-92 / ETU-93 | Explicit architecture hypotheses; do not silently bundle with gradient changes |
| Compound attacks/blocks/targets/payments and joint log probability | [ETU-94](https://linear.app/loopflow/issue/ETU-94) | Trainable joint action and credit boundaries still required |
| Forced/optionless steps and honest underlying-decision accounting | ETU-94 | Audit existing auto-resolution; collapsing prompts is not a strength result |
| Setup-style outcome-only versus bootstrapped compound-decision credit | ETU-94 | Transfer hypothesis, not assumed equivalent to Stratego setup |
| Freeze a strong policy before belief-conditioned search; consistent beliefs, rollouts and value | [ETU-95](https://linear.app/loopflow/issue/ETU-95) | Compare policy-only, uniform and same-policy exact beliefs at equal decision time |
| One regularized local search update and its distillation target | ETU-95 | Retain full generating identities; old per-action scores alone are insufficient |
| Hard targets, visits and regularized soft targets; mixed strategy and bluffing | ETU-95 | Measure behavior and strength; soft targets do not guarantee sound mixing |
| Improving search teacher versus the current fixed teacher | ETU-95 | Test compounding only after a useful policy/value model exists |
| Selective search effort, replay/cumulative reuse and relabeling economics | ETU-95 | KataGo-inspired hypotheses; charge all searches and retain target versions |
| Frozen-policy self-play with hidden truth as labels; belief model trained afterward | [ETU-96](https://linear.app/loopflow/issue/ETU-96) | Explicit policy→dataset→belief artifacts and stages required |
| Constrained autoregressive joint beliefs versus exact enumeration | ETU-96 | Measure legality, calibration, joint likelihood, latency and search strength |
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
