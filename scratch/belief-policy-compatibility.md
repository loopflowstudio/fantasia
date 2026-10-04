# Frozen-policy compound compatibility — 2026-10-04

Jack Heart authorized a bounded follow-up to PR205. Existing tests already cover
PPO and Ataraxos raw/EMA collection. Recipe validation incorrectly excludes
compound exports and their downstream belief stages.

This slice admits train_compound → collect_belief(raw) → train_belief, preserves
rejection of nonexistent compound EMA and mixed flat training, and reuses the
existing CompoundPolicy. Collection owns resetting queued Commands at each game
boundary. Private whole-game label ownership, artifact binding and last-complete-
raw selection stay with existing owners. The Env encoder enforces saved tensor
capacity before either policy runs: wide native compound support does not imply
wide sampler collection. Both kinds fail explicitly on capacity overflow.

Acceptance: bounded one-thread compound training/collection/sampler round trip;
flat and compound complete-game collection and capacity rejection. Existing
Ataraxos tests are reused, not duplicated. No scientific cohort, paid compute,
ETU91/ETU95 changes or scientific acceptance claims.

Check: one-thread focused pytest rerun passed 9 (3 unchanged PPO/Ataraxos
round-trip cases passed in the preceding run); Ruff and diff checks passed.
The initial two capacity assertions exposed the encoder's earlier rejection;
expectations now match that supported boundary. No native source changed.
