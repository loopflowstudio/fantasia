# Compound-policy sampling search

2026-10-04 — kickoff implementation design for ETU-95. Jack Heart authorized
software implementation, checks, publication and landing. Scientific acceptance
has moved to ETU-99; this design does not authorize training or a new study.

## Outcome and demonstration

A frozen ordinary or supported compound checkpoint supplies the base policy,
rollout policy and signed value estimates for bounded local search. A caller can
inject either physical compatible-hand sampling or an admitted learned sampler
without constructing possible-world support. Returned canonical action targets
retain private provenance and load through the existing distillation readers.

The headless demonstration is a fixture test: load checkpoint bytes, forbid native
support enumeration, search an attacker/cast root under each sampler, serialize
and reload its target, and replay every retained branch Command. Repeat with the
same seed and verify equality excluding elapsed time. No optimizer is needed.
Existing local artifacts in `.runs/etu95-learned-search-integrated` may supplement
portable fixtures after current-world admission; their presence is not permission
to regenerate or port them.

## Findings and chosen approach

The branch starts at `72385a90`. PRs 211/214 already supply local targets,
learned-hand materialization and real-game replay. The remaining changes are
integration changes, not a replacement teacher or replay store.

* `LocalUpdateTeacher` rejects compound policies and couples loading to
  `FrozenPolicyLikelihood`. Its `predict` calls the flat policy head, which is
  not the behavior distribution of a compound checkpoint. Removing only the
  admission check would produce mislabeled targets and leaf values.
* `CompoundDecoder` exposes conditional probabilities and prefix values;
  `sample_compound` lowers a complete submission through native authority.
  `CompoundPolicy` queues the resulting Commands. The decoder supports complete
  teacher forcing, but not forced prefixes followed by stochastic completion.
* Native `compound_offers` preserves ordinary offer IDs for priority choices,
  replacing supported casts with compound target selection. Attack declarations
  use a set-valued offer. Other decisions use ordinary search offers. Native
  `compound_commands` lowers a whole submission on an exact fork.
* Learned sampling already uses `public_sampler_input` and direct native count
  materialization. Compatible-prior play still constructs `BeliefTracker` on each
  transition; the support limit is checked after enumeration. This must change.
* `sample_physical_deal` already samples the constrained physical measure without
  enumeration and subtracts known minima before distributing unknown slots.
* Existing local readers validate action-aligned targets against
  `LocalUpdateReceipt`. Keep that contract; compound joint declarations cannot
  simply be placed in flat action columns.

Use exact conditional distributions over the next canonical Command, retaining
the original compound root observation, offer projection and decoder prefix.
At priority roots the first factor selects the ordinary action; after selection,
sample the target suffix conditionally. At attacker roots the relevant binary
factor selects the next canonical attack/no-attack Command. Condition continuation
on that choice using the same decoder state and viewer root, not a fresh policy
evaluation on a newly visible microstep. Use native lowering to validate routing
to canonical Commands. Never enumerate all attacker subsets.

The implementation must prove these correspondences against native lowering,
including forced/optionless factors, before admitting a compound root. An
unrecognized factor-to-Command boundary fails explicitly. Blockers and payments
remain separate ordinary decisions, as in the shipped compound player.

A rollout owns independent per-seat compound continuation state. It drains a
sampled suffix without resampling; stale revision, actor changes or unexpected
offers fail closed. Root counterfactual branches condition on their forced first
action, sample the remaining suffix, then use ordinary compound decisions.
At a depth cutoff inside a declaration, use its decoder prefix value with the
original root context. Record both canonical Command count and decoder-factor
count; do not silently change the configured depth clock. Terminal values remain
authoritative signed outcomes.

For actual search play, keep the retained prefix across canonical decisions and
compute action-aligned updates at those prefixes. For base-policy teacher
collection, sample the complete base declaration once and drain its Commands;
targets at intermediate prefixes must condition on the same retained root.
Receipts bind the prefix and root so replay cannot substitute a fresh observation.
Flat students may consume canonical conditional targets as behavior-cloning
labels; this does not claim they preserve the teacher's joint declaration policy.

### Sampling authority

Introduce a small typed search-facing sampler protocol and immutable sample batch
in the local-search package. Preparation binds current viewer history, native
constraint snapshot, distribution identity and supported query. Sampling takes
an explicit seed/count and returns counts plus joint log probabilities, exact
artifact identities where applicable, and cost. Materialization uses only
`Env.materialize_sampled_hand` and the retained native snapshot.

Both constrained-prior and learned implementations use this boundary. Constrained
prior binds the physical-deal method and public constraints; learned sampling also
binds checkpoint, dataset, schema, world and generating policy. Do not invent a
learned artifact for the prior or canonical indexes for directly sampled hands.
Use sequential draws to preserve cheap/full seed prefixes. Revalidate injected
output dimensions, constraints, identity, finite probabilities and source root
before executing branches; injection cannot bypass admission.

Production samplers support `True` initially. Other queries fail before rollout
because calibrated conditional sampling/mass is not implemented. Keep exact
enumeration only as an explicitly selected tiny diagnostic reference, with its
existing query semantics and history gaps; it is never an automatic fallback or
the production default. Compound exact-history likelihood remains unsupported.

### Ownership and consumers

managym remains the authority for constraints, hidden materialization, legal
offers, lowering and Commands. Reuse `SelectedFullCloneBackend` branch audit,
TrainingRun/VerifyStore, local shards, arena traces and the ordinary checkpoint
loader. No new session, identity registry or replay store is needed.

Coordinate the narrow prefix-completion API with ETU-94 before editing its
decoder. Prefer adding execution/projection code under `manabot/sim`; the model
change, if needed, only exposes existing conditional computation. Do not modify
ETU-94 training objectives or interpret the dormant flat head as compound policy.

Cut over `LocalUpdatePlayer`, `make_player`, regime collection and arena
registration/fingerprinting to sampler and policy capability admission. Extend
the existing receipt reader with discriminated direct-sampling evidence and
compound prefix provenance. Historical receipt bytes retain their own schema;
no evidence is rewritten. Update source fingerprints to include extracted policy
and sampling implementation owners, not just `local_update.py`.

`GameSession` already owns canonical decisions and authority transitions;
`Trace` carries private canonical replay and `AttemptStore` persistence. Automatic
passes advance authority but are not deliberate decision ordinals. The ordinary
loader binds setup, ABI and content, and configured Etude opponents additionally
bind retained bundle/runtime bytes. No synthetic fixture can establish real
candidate or human-play admission. The table protocol remains unchanged.

## Alternatives rejected

* Flat-head inference for compound artifacts: estimates the wrong policy/value.
* Resampling each canonical microstep: loses the original recurrent prefix and
  changes the joint policy.
* Enumerating compound declarations or hidden support: exponential cost defeats
  the requested bounded path.
* Searching a sampled subset of declarations and calling its normalization a
  complete action distribution: changes target semantics and existing readers.
* Implicit prior fallback or approximate query masses: hides unavailable evidence.

## Internal slices

1. **This slice: sampling boundary.** Replace production prior enumeration and
   learned-specific branching with the common typed interface; retain tiny exact
   reference explicitly. Focused test forbids every native support constructor
   through player startup, observation updates, search and replay for both samplers.
2. Add compound prefix-conditioned inference/continuation and native Command
   routing. Test cast targets, multiple attackers, singleton offers, forced
   factors, blockers/payments, two seats, interruption and depth cutoffs.
3. Integrate collection, receipts/readers, arena replay and public projection.
   Targets must survive save/load with unchanged probabilities and provenance.
4. Compress duplicate sampler/policy orchestration, document supported paths,
   reconcile Wave memory, verify at gate, then publish/land through Loopflow.

Remove production construction of prior trackers and the blanket compound
rejection after their replacements pass. Keep `BeliefTracker` and its independent
tests for tiny reference use. Remove learned-only orchestration duplicated by the
common sampler; preserve historical receipt parsing and all existing privacy
checks. Do not fork a second local teacher implementation.

## Acceptance and operational boundaries

Gate runs a bounded fixture-only suite, with new cases in
`tests/sim/test_local_update_sampling.py` and
`tests/sim/test_local_update_compound.py`, plus existing reader/advice tests:

```bash
uv run pytest -q tests/sim/test_local_update_sampling.py tests/sim/test_local_update_compound.py
uv run ruff check manabot/sim tests/sim
```

The new files are planned, not present yet. Reuse tests without invoking existing
helpers that fit samplers or execute training regimes. Save deterministic model
fixtures without optimizer steps when portable retained artifacts are absent.
Native changes, if required for authoritative routing, require debug cargo tests
and a rebuild confined to this checkout before Python integration checks.

Required evidence: normalized full canonical action rows; decoder conditional
probability parity on tiny exhaustively checked declarations; identical seeded
branch tapes; hidden-world-swap invariance; direct/prior tiny-reference frequency
agreement; exact raw/EMA and sampler-policy identity rejection; stale history,
unknown query, malformed samples and capacity failures; deadline expiry even in
sampling or suffix execution; private evidence absent from advice projections.
No partial timed-out target may be accepted. Costs include preparation, sampling,
lowering, rollouts and value evaluation. Forwards/native calls are cooperative;
arena subprocess limits provide the outer bound.

Search strength, new training, iterative improvement, sampler calibration, live
advice registration and human-play success are excluded. ETU-99 owns scientific
comparisons; ETU-96 owns offline sampler quality. ETU-91 source, extension,
artifacts, plans and 168-hour allocation remain untouched.

Check result: source inspection at `72385a90` confirms the integration gaps above;
fixture execution is pending implementation. No training or tests ran in kickoff.
