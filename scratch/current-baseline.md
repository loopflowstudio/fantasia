# Current baseline: demonstrate learning before architecture conclusions

Jack Heart approved this direction and invoked launch-plan on 2026-10-06.
The goal is a reproducible demonstrated-to-learn reference, not a best-recipe claim.

## Core and demo
Ship one end-to-end positive-control learning experiment through the real engine,
viewer-safe observations, ordinary policy, actual learner, saved/reloaded
checkpoint and evaluator. Choose an engine-backed situation with multiple legal
choices and clearly different outcomes. Vary held-out situations so memorizing
one action index cannot satisfy acceptance. No privileged answer feature, mock
gradient, alternate policy or supervised surrogate may stand in for the RL path.

Measure initialization, trained checkpoints and a frozen/no-update control on
matched held-out games across at least three independent seeds. Before scoring,
freeze substantial gain criteria, evaluation sample count, seeds and budgets.
Thresholds and the concrete task must follow inspection of engine capabilities;
do not retroactively weaken them. Include terminal reward perspective, legal
probabilities, advantage sign, gradient flow and checkpoint identity checks.
Failures are evidence for diagnosis, not grounds to drop seeds or retry secretly.

Then demonstrate a small full-game matchup versus a fixed opponent, using the
same path, before declaring a general learning baseline or moving to self-play.
The first positive control proves a narrower contract and must be labeled so.
Both levels belong to this Task; no placeholder-only infrastructure delivery.

## Recipe and evidence
Start by inspecting the exact masked-mean recipe from experiments/value-token-screen.md:
400 to 800 updates improved fixed-greedy score 30.7% to 42%, with +6/+16/+12
points by seed. The later pooling/filter follow-up was roughly flat, so this is
candidate evidence, not validation. Existing docs and resolved plans in this
checkout retain the settings. Hold architecture fixed; explain any environment
or opponent changes. Keep initialization and frozen controls genuinely paired.

Use the Experiment data model and shared runner where supported. Add necessary
positive-control environment configuration to the ordinary execution path rather
than a parallel harness. The notebook generates concise read-only HTML and
retains all outcomes/costs. Reuse existing reporting; ETU-117 owns its independent
presentation improvements. Interpret evidence through the research workflow.

## Allocation and delivery
Use local CPU with one learner thread; inspect current available capacity first.
Initial calibration/positive-control attempts have a 15-minute ceiling each and
one-hour aggregate exploratory ceiling, including failed attempts/evaluation.
These are conservative launch limits, not evidence-derived learning thresholds.
If unsuitable for the selected real path, report the needed revised allocation
rather than silently expanding it. No paid provisioning, no interference with
live campaigns, and no use of mini capacity reserved for ETU-103 then ETU-116.
Freeze a new full-game allocation before starting that level if it cannot fit.

Continue via pursue: implement, compress, refresh and publish. Preserve accepted
contract, runnable definitions and evidence in durable docs before cleanup.
Run focused behavior checks and actual bounded learning evidence; a passing
software test alone does not complete this Task. Publish a clear PR and raise
remaining empirical limits. Larger-model work and ETU-116 remain separate;
do not proclaim current-baseline promotion unless its declared tests pass.

## Implementation decisions (2026-10-06)
The lethal-target-v1 root uses the exact authored match with UR in either seat;
custom deck subsets fall back to a different native catalog and cannot consume
this semantic model. Keep setup identities intact. The ordinary collector receives
native terminal roots through its buffer contract; no alternative learner is added.
`experiments/current-baseline.md` owns the prospective numeric protocol.
Delete — do not maintain: none; this is a new bounded measurement capability.
Remaining: execute the fixed positive control, diagnose failures, then full-game
allocation/evidence, notebook and delivery. No baseline promotion yet.
