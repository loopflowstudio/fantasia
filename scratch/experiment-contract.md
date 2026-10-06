# Accepted Experiment direction

Jack Heart selected this direction and invoked launch-plan on 2026-10-06.
This supersedes the earlier per-campaign monitoring-only scope in etu-113.md.

Build a reproducible, readable Experiment data model above TrainingRegime.
Each experiment has its own declarative Python file and thin executable entry
point. Real depth and history comparisons are the initial consumers: using them
should expose the scheduling and reporting capabilities the shared runner needs.
Do not duplicate that machinery in experiment scripts. Preserve the existing
component/recipe resolver; resolution remains side-effect free.

The shared execution interface accesses configured authorized hardware, launches
regimes and seeds, evaluates milestones during training, and retains checkpoint
identity, failures, recovery history, resource use and total costs. Separate
experiment intent from actual execution records. Reuse TrainingRun, existing
monitoring evaluators and persistence owners. Preserve scientific cohort
isolation and declared budgets. Do not mutate currently running campaigns.

The primary output is ONE editable Jupyter notebook per experiment. It loads
all regimes and exposes data-loading and plotting cells for learning curves,
milestone win rates and uncertainty, cross-regime comparisons, and cost/resource
monitoring. Rerunning cells reads retained evidence without launching training.
Preserve user edits on refresh; local reproduction must not require a tracker.
W&B is already integrated and can remain an optional projection. Other trackers
and cloud provisioning are follow-ups, not prerequisites.

An experiment skill invokes the interface, interprets evidence and updates the
research ledger and durable knowledge. Automatic knowledge rewriting does not
belong in experiment.py. Document this boundary and the skill workflow; do not
invent conclusions from noisy graphs.

Deliver the coherent end-to-end core through a well-described PR, focused checks
and required CI. Demonstrate both real experiment definitions plus tiny fixture
execution and a headlessly executed, editable notebook. No substantive new
training or paid provisioning. Preserve useful design in durable docs before
scratch cleanup. Existing ETU-113 worker remains the sole implementation owner.
