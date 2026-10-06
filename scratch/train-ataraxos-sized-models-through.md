# Ataraxos-scale ordinary models

ETU-115 · 2026-10-06 · Implementation plan from Jack Heart's Task direction.
The requested software and short laptop measurements are authorized. This plan
does not approve a scientific cohort, rented compute or ETU-107's draft design.

## Outcome and demo

A recipe author selects depth 8, width 384 and feedforward width 1,536 through
AgentSpec and ordinary recipe composition. Before committing to a training run,
the author can inspect actual parameters, attention slots, memory estimates and
measured laptop forward/update cost. A tiny ordinary CPU TrainingRegime trains,
exports and reloads that model through the existing checkpoint loader.

Demo: extend the existing calibration entry point with an explicit scale probe:

```bash
uv run -m experiments.runners.calibrate_training --scale --out .runs/etu115-scale
```

This is a proposed command to implement. It prints/writes one row per rung and
device, including failures/unavailable measurements, and points to retained
TrainingRun artifacts and the large model's ordinary reload receipt. Report
forward observations/s and optimizer sample exposures/s separately from complete
collector throughput. No arena score is needed for this Task.

## Findings that determine the implementation

* `AgentSpec.attention_layers` and recipes.AttentionDepth are Literal[1, 2].
  Agent already constructs a ModuleList for additional layers and iterates it.
  GameObjectAttention uses a heads × width MLP, post-normalization, ReLU and
  ownership injection only in the first block. Preserve these equations.
* `architecture_identity` hashes the complete serialized AgentSpec plus
  observation settings under layout_version 1. Adding a serialized null would
  invalidate old receipts and regime digests. `recent_events` already supplies
  the appropriate omitted-default convention. Keep old model construction order,
  weight names and initialization bytes; there is no reason to port checkpoints.
* The default visible attention sequence is **202 slots**, from two players,
  2 × 60 cards and 2 × 40 permanents. A value token makes **203**. Actions (64)
  and events (32) are not appended to that sequence. Belief inputs append their
  actual schema-bound rows and one global row; recent-event input adds a pooled
  context, not event tokens. Report configured and measured shapes, rather than
  inheriting the Task's rough 270–300 estimate.
* Padding masks exclude invalid keys and block outputs are zeroed. However,
  the historical critic applies a biased projection and averages all slots.
  Removing slots and pooling the shorter sequence changes its result. Action
  focus indexes and ownership are also tied to the fixed layout. Packing valid
  objects could preserve mathematical semantics if it remaps ownership/focus and
  scatters outputs back to the original zero-filled layout before downstream
  consumers (or exactly preserves the old critic denominator/bias contribution).
  Masked/token critics do not have that denominator problem. Different kernels
  may still change floating-point results. **Do not implement packing here**;
  document this finding and keep observation capacity/world ABI unchanged.
* ETU-103's `capacity_study.CapacityWorkload` has exactly three counts, uses the
  three existing cases, and budgets nine runs. Adding a fourth default case would
  either fail indexing or silently alter an existing scientific plan. Add the
  new rung as explicit opt-in to the same ladder API, used by the scale probe;
  preserve the old default experiment, preset bytes and scientific protocol.
* ETU-107's current `scratch/etu-107-unify-model-facing-decisions-with-engine-owned-legality-and.md`
  was inspected through `lf task file` on 2026-10-06. It is a proposal awaiting
  review: native typed choices/prefix support and model candidate joins/scoring.
  Shared files include AgentSpec and Agent, but the attention constructor is a
  separable edit. Do not touch compound scoring, offered-choice semantics or
  input joins. Recheck its diff before implementation if the review has advanced.
* ETU-114's generic `gpubench.py` and `throughput-probe.txt` were inspected through
  `lf task file`. The stand-in uses TransformerEncoderLayer with pre-normalization
  and eight heads at width 384, unlike this model. Its 8×384 float32 batch-256
  GPU rates were 2,676/919 forward/train samples/s at 64 tokens and 593/204 at
  256 tokens (about 4.5×, not 10×). Batch 1,536 at 256 tokens failed in both
  tested precisions. These are contextual generic-probe numbers, not manabot
  measurements or permission to rent hardware. Do not copy its CPU memory zero
  as a measurement. ETU-114 remains owner of device/stage execution.

## Configuration and compatibility

Change depth to a validated positive integer, without inventing a new small
upper limit. Add `attention_feedforward_dim: int | None`, positive when present,
default None and excluded from serialization when None. None means the existing
heads × width expansion. Pass the resolved dimension to every attention block.
Keep attention-off and compound depth restrictions; reject a custom feedforward
setting when attention is disabled rather than pretending it affects the model.
Compound depth support is outside scope; its one attention block may use the
same explicit feedforward setting if normal admission permits it.

Architecture hashing omits the new field when unset. For an explicit dimension
equal to heads × width, normalize only the architecture identity payload to the
historical omitted form: those equations and weights are identical. Recipe
provenance may retain that explicit author choice. Nondefault dimensions enter
the existing hash. No global layout-version bump, new receipt version, relaxed
loader or alternate state dict is needed. Existing receipts still load unchanged.

Extend `with_capacity` with the optional feedforward dimension and remove the
two-depth typing restriction. Omission preserves a base recipe's existing setting;
an explicit None requests the historical expansion. Use the recipe module's
existing variation/revalidation conventions and an omission sentinel if needed.
Expose the large case through an explicit ladder selector such as
`experiment(base, include_ataraxos=True)` / `regimes(...)`. The new case is
width384/depth8/heads4/feedforward1536, holding all other model and learning
settings fixed. Four heads preserve the local comparison; this is size parity,
not reproduction of the Stratego architecture or its performance.

AgentSpec remains the only configuration owner, architecture_receipt owns actual
parameter counts, TrainingRun/VerifyStore own training status/cost/artifacts,
and the benchmark report is a derived view. Exact parameter totals must be
counted on the semantic model, not asserted to equal the generic probe's 14.2M.
Existing selected-world loader checks remain mandatory: authored Allies/Lessons
decks and sideboards, semantic input and unchanged world/setup bindings.

## Bounded measurement design

Use four rungs (64/1, 64/2, 128/2, 384/8), scalar value-token, history off,
semantic Allies/Lessons observations at the existing default capacity. Keep
each resolved recipe, architecture identity, input digest, runtime/source,
hardware/OS/Torch identity, seeds, threads, actual batch and timing method.

One CPU thread, float32, batch 4 for each model/device; no giant batch search.
Capture a real viewer-safe batch once using native observations and reuse it.
Measure construction and first call separately. After two warmups, perform
three timed windows per forward/update phase, each targeting two seconds with
a finite iteration cap. Count actual completed samples and elapsed time; report
each window and median/range. Synchronize MPS before and after timing. Update
means forward + a documented finite scalar/WDL-compatible diagnostic loss +
backward + Adam step; label it as a model optimizer microbenchmark, not the
Ataraxos learner or end-to-end training speed. Use fresh model/optimizer per
device and phase where required to avoid cross-phase weight/allocator confounds.
Report parameters, buffers, tensor input bytes and parameter/gradient/Adam byte
estimates separately from sampled process RSS and available MPS allocator
readings. Activation memory is batch/backend dependent; estimated static bytes
are not a fit guarantee or measured peak. Keep host contention visible.

Separately run a CPU recipe fixture per rung through the existing executor:
one stage, one update, one stream, 8 learner transitions, zero advantage floor,
and ordinary raw export/reload. Assert positive optimizer exposure and actual
weight change. This is the training integration proof, separate from diagnostic
update timing. No new MPS execution support: standalone probe only. Explicitly
record unavailable MPS, unsupported operations, OOM or timeout without CPU
fallback masquerading as MPS success.

Allocate at most 900 elapsed laptop seconds for the entire retained measurement
attempt, including setup/training/probes/report, with subprocess deadlines of at
most 90 seconds per model/device probe and 90 seconds per recipe fixture, bounded
by the remaining total. Retain partial results and failures; no automatic retries
or budget extension. No rented hardware or scientific cohort. Isolated subprocess
measurement avoids attributing a previous rung's allocator high-water mark to
the next. New output directories only; large raw artifacts remain ignored.

## Implementation sequence and acceptance

1. **This slice: configuration and attention compatibility.** Capture old recipe
   digests, architecture receipts and deterministic output/weight fixtures from
   base `fd7437dfd84cd1e24785a6d7febee78fceff3d80` before editing. Add depth/MLP
   fields and narrow constructors/helper changes. Replace tests that reject depth
   3 with meaningful invalid-depth and strict wrong-weight-layout checks.
2. Extend the existing ladder explicitly, preserving all three default case
   digests and ETU-103 plans. Add scale reporting/probe support alongside the
   existing calibration runner, with typed results and bounded subprocesses.
   Keep old `--capacity` behavior/budgets unchanged.
3. Exercise the deep semantic model through positive optimizer work, raw export,
   `load_checkpoint_agent` and matching policy/value outputs. Check malformed
   feedforward metadata, missing/deeper weights and changed receipt rejection.
   Assert observed attention length equals report accounting for each rung.
4. Run the single bounded laptop measurement and retain a compact report in
   `docs/training-calibration.md` or linked dated evidence. Include commands,
   actual parameter/slot/memory/rate rows, costs, failures and interpretation
   limits. No strength ranking, chapter acceptance or default model promotion.

Headless focused gate:

```bash
uv run pytest tests/model/test_capacity.py tests/model/test_value_aggregation.py tests/model/test_categorical_value.py tests/training/test_architecture_recipes.py tests/training/test_experiments.py tests/training/test_capacity_study.py
```

Add focused probe/deadline/report checks and the deep training/export fixture
to the existing calibration/model tests. Gate should inspect the retained real
benchmark rather than repeat it just to reproduce timing. Frozen historical
receipt fixtures must come from base code, not be regenerated by new code.

No deletion is required beyond obsolete depth-3 rejection assertions and the
Literal depth alias. Do not remove old capacity cases, presets or compatibility
tests. No new checkpoint/session/identity store: GameSession already owns play,
Trace carries auto-pass flags and private canonical replay, and the ordinary
loader validates world and architecture before strict weight load. This Task
does not need table protocol changes or claim human game/crash-durability proof.

Check: `uv run python` runtime inspection failed before model construction because
this fresh checkout lacks `managym._managym`; static slot/configuration findings
above come from source. Build the pinned native extension per AGENTS.md before
runtime tests. No model benchmark, training or strength measurement has run here.
