# Search-update research: live decisions and evidence

Jack Heart selected MMD/KL/PUCT comparisons, recursive action uniformity, no
learned beliefs, and compound-policy training versus non-compound policies.
Current execution and all pilot identities/results: `search-policy-pilot.md`.
Full source-checked research, derivation, evidence registry, historical receipts,
protocol variants and contrary evidence are preserved at git commit
`219719a0aa73eb5852903862b7cd719e8d4fc3e3:scratch/mmd-findings.md`.
This condensed note replaces that ambient copy, not its evidence.

## System model

`manabot/sim/local_update.py::regularized_update` already implements full MMD:
maximize `p·Q - beta KL(p||p0) - alpha KL(p||rho)`; solution on positive base
support is `softmax((Q + beta log p0 + alpha log rho)/(beta+alpha))`.
`beta=1/eta`; alpha zero is KL-only. Current defaults: alpha .02, beta 1,
one world, depth 2. Current rho is uniform over canonical root offers. Constant
rho still changes entropy/temperature; it is not a no-op. Rho equal to p0 simply
increases trust. No network weights change during search.

The same frozen checkpoint owns base policy, rollout and signed leaf value;
terminal scores are -1/0/+1. Compound continuations condition on original viewer
root and retained prefix, never an unrelated flat head. Keep exact base zeros,
canonical offers and hidden-information boundaries. Current API requires rho
positive everywhere and rejects lost supported mass/nonfinite supported Q.
A probability-valued Q converted to signed units requires doubling alpha/beta.

All selected search arms use `physical-compatible-hand/v1`: physically compatible
hands without replacement, conditioned on public minima/pool/hand size; not
uniform count vectors or a behavioral posterior. Action magnet and hidden-world
prior are different concepts. No learned-belief fitting or comparison is selected.

PUCT uses adaptive per-world trees, a total traversal budget, and max-visits play
(tie by Q). Flat MC uses per-action rollouts and Q argmax. They generate different
evidence from fixed-policy local rollout. Unvisited PUCT Q=.5 is not evidence.
The current AgentLeafEvaluator sigmoid is incompatible with signed critics;
compound PUCT also lacks a verified retained-prefix adapter. Both are admission
gaps. Use measured compute, not equal nominal simulation counts.

## Selected experiment structure

1. **Hold for the Mini baseline** (Jack Heart's latest direction). The fresh
   flat/compound pair only calibrates integration. Freeze the new baseline's exact
   checkpoint, recipe, world/input and evaluation evidence before variations.
   The earlier three-seed-pair training comparison is deferred; compute remains
   unallocated. Different credit units, estimators, regularization and parameter
   counts still prevent attributing a recipe contrast solely to representation.
2. On identical retained root evidence compare raw, KL-only, offer-uniform MMD,
   recursive-uniform MMD, and Q-argmax diagnostic. Current MMD identity is a wiring
   control. Proposed development: 64 roots, 8-world batches with 1/2/4/8 prefixes,
   depth 2; beta .25/1/4 development only. No root scoring has run.
3. Full games compare within each policy family, including PUCT once admitted.
   Pair deals/seats/deck assignments and freeze budgets/tuning before held-out play.
   Later trajectories diverge, so full games are not shared-rollout isolation.
   Bootstrap deal blocks; independent training seeds are the method-level units.
   Earlier 384-game and later conversational sizes are alternatives, not cumulative
   allocations. Recalculate after calibration; main compute is not allocated.

Recursive uniformity means uniform legal children at each authoritative
construction prefix, multiplied along a path and marginalized onto next canonical
Commands. Forced factors have mass one. Uniform full leaves is different. Reuse
native legality and compound projection; do not invent families from labels or
cross reveals/opponent/revision boundaries. Require positive reference on all
positive-base actions; off-support zero validation needs explicit handling.
Normalization, prefix conditioning, canonical aggregation, hidden-world invariance
and payment-support tests precede scoring.

Optional synthetic sensitivity tilts explicitly legal world weights, not learned
beliefs. At fixed beta/world treatment measure regret against known fixture values,
wrong-action mass, entropy, KL to base and failures. More samples can concentrate
around biased Q; no real-game terminal outcome is certified root ground truth.

## Evidence limits and sources

No current-world MMD-vs-KL or MMD-vs-PUCT strength result was found. Delivered local
search/compound code is correctness evidence. Historical w2 INT-7 improved value
calibration but weakened complete PUCT players; INT-8 rejected learned priors;
INT-17 was a systems failure without calibration curves. Exp-10 passed against
V-greedy yet lost matched-cost random-rollout search. These counterexamples do
not establish current MMD performance. Exact reports/hashes remain in the archived
registry. The five-fixture offline algebra probe passed, but was not an engine test.

Primary sources checked in the original pass:
- https://arxiv.org/html/2304.13138v3 — two-KL objective/update equivalence.
- https://arxiv.org/html/2206.05825v4 — underlying MMD method.
- https://www.nature.com/articles/s41586-026-11036-y — Ataraxos methods,
  supplement S3.7 and Extended Data Table 1. Its alpha .002/beta .02, depth 40,
  ~1,000 rollout settings are not manabot defaults; its result is not an MTG claim.

The proposed ETU-118 final raw seeds 11851–11853 (pilot 11851) were never loaded;
recorded local bytes are absent. Do not substitute development checkpoints or
assume w4 files admit under a repaired input contract. The October 15 pilot
confirmed a flat encoder bug forcing attack/decline to 50/50; Jack Heart selected
its repair and retraining. The Task is now stacked on PR288 and its shared
w5/input-v1 encoder. A fresh flat/compound development pair completed; details
and superseded prototype identities are in the pilot note. The eight-game 4–4
result certifies integration only; main strength/search comparisons remain pending. Broader MTG-107 interface redesign, Academy deployment, paid
compute and unrelated belief/distillation programs remain outside scope.
