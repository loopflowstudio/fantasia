# ETU-104 architecture design

2026-10-05: Draft for Jack Heart's review; research/documentation only.
The complete durable proposal and primary-source comparison are in
[the design](../docs/plans/modular-architecture-recipes.md), with a
[self-contained HTML review](../docs/plans/modular-architecture-recipes.html).
This file indexes that owner rather than duplicating the design.

The proposal uses strict architecture specs and local builders while preserving
TrainingRegime, TrainingRun, ordinary checkpoint admission and the existing arena.
Current source inspection separates program GRU, compound prefix, public game
history and frozen-policy sampler lifecycles. Baseline fixed-slot value pooling
is preserved as a control; recent-event input is an explicit information treatment.
ETU-106's live directive already approves focused value-token testing, not this
framework. Its final implementation and the independent capacity ladder must be
consumed without duplicate modules or altered frozen recipes.

Research inspected pinned public implementations from torchtune, big_vision,
Transformers, Ray and DreamerV3, plus primary papers and Hydra documentation.
Unavailable URLs and maintenance limits are recorded in the design. A local uv
environment was created to inspect/render documents; no training or engine change.

Remaining: Jack Heart's substantial design discussion, feedback, then acceptance,
rejection or deferral. The later steer asks for a separate review-design Session;
this headless result cannot supply human feedback or release implementation.
No architecture-framework implementation, Task completion or scientific run is
implied by readiness. No active ETU-91 checkout was accessed or changed.

Check: uv-run documentation validator passed (12 unique HTML anchors, all local links, no scripts); lf context fits all budgets. Browser rendering unavailable.

Delivery: `cd6323a0` checkpoints the durable design, HTML and Wave memory.
Loopflow leaves scratch notes local. `lf session ready` failed with
`this command requires an active session` / `environment variable not found`.
No review Session was opened or completed. Human review remains pending;
artifact creation does not establish approval.
