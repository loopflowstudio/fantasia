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
The original AgentLeafEvaluator sigmoid was incompatible with signed critics,
and compound PUCT lacked a retained-prefix adapter. The compatibility change
below closes those admission gaps. Use measured compute, not equal nominal
simulation counts.

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

## Accepted PUCT compatibility implementation — 2026-10-15

Ship current-policy compatibility first. Preserve PUCT's win-score units
(loss 0/draw .5/win 1): signed critics convert affinely, declared win logits use
sigmoid, unknown scalar semantics fail admission. Preserve unconstrained scalar
estimates (no clipping); reject nonfinite values and incomplete legal support.
Compound roots and child nodes carry the existing original-root cursor and
conditional projection. Advance it independently in each branch, never through
the flat head; zero-prefix-support actions cannot be selected. The live player
retains only the actually chosen prefix and resets at game boundaries.

Delete/replace: unconditional sigmoid interpretation in AgentLeafEvaluator,
compound fallback through Agent.forward, and unrestricted selection of zero-prior
choices. Reuse local_compound's projection/lowering and the existing PUCT tree,
native physical determinization, player factory and arena. No new world/schema,
new planner, learned belief or strength experiment. Preserve random Teacher-1,
terminal scoring, actor perspective, seed/budget accounting and exact branch
mutation. Unit/engine fixtures and a tiny replay smoke (one thread, <120 seconds
per check, no training) establish compatibility; publication is selected by the
active goal “ship puct compatibility.” Broader comparison tooling follows this
unit; Mini baseline remains a prerequisite for scientific comparisons.

Implemented: declared critic units in the ordinary checkpoint loader; affine
signed-to-win-score conversion; exact retained compound support through branches
and actual play; explicit current `agent_puct` arena registration, source/byte
identity checks and game reset. Initial self-play exports now declare their signed
target. `docs/local-policy-search.md` documents the executable contract and limits.
No frozen recipe/artifact migration or strength claim.

Validation: affected suites **70 passed / one historical INT-7 failure** in
36 seconds (`.runs/puct-affected-tests.log`): unchanged `load_shards` requires
`semantic_cards`, absent from the frozen retained shard. Final focused run
**25 passed in 7.45 seconds** (`.runs/puct-final-focused.log`), including 15 new
PUCT cases, existing prefix/parity checks and initial-export metadata regression.
Four untrained arena fixture games (both families, both seats) completed and
Command-replayed. Ruff and diff whitespace checks pass. One broader rerun was
interrupted to select only non-learned compound fixtures; its partial count is
not an acceptance result. The export regression uses tiny ordinary training
fixtures; no training variation, learned-belief fit or scientific cohort launched.
The first new payment assertion exposed a fixture train/eval-mode mismatch
(1.35e-8 probability drift); setting eval before both projections fixes the test
without relaxing exact hidden-world invariance. All logs remain in `.runs/`.
