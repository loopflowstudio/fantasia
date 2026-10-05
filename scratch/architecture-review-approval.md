# Architecture recipe review approval

Jack Heart approved the reviewed ETU-104 design in the parent conversation and requested completing the review session, implementation, and landing on 2026-10-05.

Implement the current docs/plans/modular-architecture-recipes.md, especially section 11: Python experiment files construct existing TrainingRegime objects; model configuration remains within the existing agent configuration; shared validated variation helpers remove duplication; generated JSON/YAML are exports. Preserve the accepted recipe/spec terminology and lessons from Keras/JAX and the other researched implementations. Prefer incremental changes to the near-fit existing AgentHypers over an unjustified framework rewrite.

Adopt actual ETU-102/106 delivery rather than duplicating their model changes. Preserve checkpoint compatibility, identities, and the frozen ETU-91 campaign. The approved bounded software acceptance workflow is at most 15 minutes on one CPU thread per complete attempt; no new paid compute or large scientific campaign. Update stale pending-approval wording in the design coherently during implementation. Deliver through reviewed code, relevant headless tests, a clear PR, CI, and merge; Jack Heart explicitly authorized landing. Do not treat earlier pending-review prose as a fresh approval requirement.
