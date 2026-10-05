# ETU-106: focused value-model contrasts

2026-10-05. Kickoff design; implementation and measurements remain pending.
Jack Heart authorized focused software delivery and cheap bounded sanity checks.
The latest steer prioritizes historical mean, validity-masked mean, one-layer
value token and two-layer width-64 value token. Scalar versus categorical
outcomes remain an independent factor. This design does not approve ETU-104's
general framework or a scientific campaign.

## Outcome and demo

A researcher resolves eight explicit width-64 recipes, runs them through the
ordinary TrainingRegime executor, reloads every exported checkpoint, and compares
their complete-game results through the existing arena and offline report.
The report shows configuration, failures, learner-step and elapsed-cost curves,
and marks strength conclusions unresolved. No Etude protocol or world change is
needed. This serves Trained Challengers' reproducible-training measure; workflow
smoke alone satisfies neither full-game improvement nor human-challenger KRs.

Proposed headless demo command after implementation:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run python -m experiments.runners.run_value_models --profile smoke --out .runs/etu106-value-smoke
```

The experiment-specific runner composes existing TrainingRun, EvaluationProtocol,
arena replay and report machinery. It is not a second trainer or evidence store.

## Findings and source boundaries

- `manabot/model/agent.py` uses one post-normalized GameObjectAttention block.
  Attention zeros padded outputs, but the critic applies Linear/ReLU before
  fixed-slot mean pooling. Its bias can make padding nonzero again; even with
  zero bias, averaging all slots changes scale with occupancy. Masked pooling
  is a generic padding correction hypothesis, not evidence of stronger play.
- `Agent.forward_distribution` already emits scalar or loss/draw/win logits.
  `forward` converts WDL to P(win)-P(loss). `training/ataraxos.py` already owns
  categorical lambda targets and cross-entropy. `TrainingRegime` rejects
  categorical ordinary PPO, compound and incompatible supervised objectives.
  Reuse those contracts rather than adding another categorical implementation.
- `sim/flat_mc.py:load_checkpoint_agent` rebuilds from saved AgentHypers, checks
  world/input identity, then strictly loads weights. Mean versus masked mean
  can have identical weight shapes: metadata, not shape, owns this distinction.
- Current compound decoding has its own masked context and prefix critic.
  Changing the ordinary value head does not change that critic. New aggregation
  modes must reject compound configuration until explicitly implemented there.
- Agent does not read recent-event tensors. Its semantic program GRU is not
  temporal game memory. Neither fact proves the cause of control failures.
- The [actual supplement, S2 and S3.6/Table S10](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-11036-y/MediaObjects/41586_2026_11036_MOESM1_ESM.pdf)
  confirms engineered history and an eight-layer width-384 pre-normalized move
  network. Those are source-backed hypotheses, not a prescription for MTG.
  The Nature main page/figure could not be fetched during kickoff; the supplied
  value-token description is not independently verified here. The chosen token
  is an explicit MTG design, not a claimed exact paper reproduction.
- `etude/server.py:GameSession`, `trace.py`, `attempts.py`, and
  `experience_protocol.py` already own execution, saved traces and canonical wire
  data. TraceEvent distinguishes automatic passes from human actions. Preserve
  these owners; do not claim a model reload demonstrates human completion or
  policy-free/crash-durable replay. `configured_opponent` and GameSession check
  actual content/setup. Do not use the Interactive-mirror fingerprint helper
  as selected Allies/Lessons identity.

## Chosen architecture

Add narrow typed AgentHypers fields `value_aggregation` with values
`historical_mean`, `masked_mean`, `value_token`, and `attention_layers` in {1,2}.
Defaults remain historical mean and one layer. All eight recipes use width64,
four heads, current post-normalization, current semantic inputs, and ordinary
flat legal offers. Two layers are measured only in the token arm initially.
Depth is the shared object stack depth, not an extra critic-only transformer.

Keep the first attention module and historical value-head parameter names,
construction order and mathematics intact. Additional attention layers use a
separate ModuleList populated only when needed. Old current-world checkpoints
without the new fields resolve to the historical one-layer path with identical
outputs; never port incompatible world bytes or rewrite frozen manifests.

For masked mean, apply the same per-object Linear/ReLU, then reduce only valid
rows and divide by their valid count. Reject an all-invalid root explicitly.
Do not multiply NaNs by zero and call them masked: test finite invalid payload
isolation, and maintain the existing input validation boundary.

For value token, append one learned, always-valid token to the object sequence
before the shared attention stack. It has neutral ownership (no hero/villain
perspective offset). Existing real-object indexes remain unchanged; strip the
token before action-focus gathering. Read the final token through the existing
critic MLP with the pooling operation bypassed. This lets valid objects and
the token exchange information, so policy representations can change as well:
call it a shared value-token architecture, not an isolated critic intervention.
Apply ownership encoding once per stack, not repeatedly per layer. Mask padding
at each block. No positional MTG board encoding is introduced.

Reject token or depth>1 with attention disabled, invalid head/width combinations,
and nonhistorical aggregation/depth on compound checkpoints. Historical compound
behavior remains intact. Ordinary belief rows, when configured, participate in
the same validity contract; no actual hidden world or query truth enters inputs.
Retain scalar/WDL as the existing independent `value_kind` field.

No global default switch follows from smoke. Historical pooling remains only
the compatibility path and named baseline. No dynamic architecture registry,
checkpoint adaptation, second categorical head, new session store or silent
fallback is introduced. No existing mechanism is deleted in this additive slice.

## Runnable protocol and limits

The eight cells cross four variants (historical/1, masked/1, token/1, token/2)
with scalar and WDL. Freeze AtaraxosMoveLearning in all cells, including scalar;
only its existing value-target/objective branch differs by outcome factor.
Use identical authored Allies/Lessons decks and sideboards, current runtime
world/ABI, observation capacity, optimizer/schedules and supported legal domain.
Retain full resolved JSON and digests before execution.

Proposed bounded implementation proof: CPU one thread, seed 1061, two linked
stages per cell, each one update of four streams x 64 transitions. Each cell
has a 60-second total watchdog; the full study has a 900-second process ceiling
including arena, export and report. One held-out paired deal 910106 and anchor
deal 920106, four deck/seat legs, raw checkpoints at both stages, random anchor.
Use the existing paired arena selection; no cherry-picking cells or checkpoints.
At most one full smoke attempt in the initial implementation pass. A timeout or
failed cell remains incomplete, with its costs and artifacts retained; it does
not authorize a longer retry. These are proposed cheap-check limits, not a new
scientific budget. Do not run this during kickoff.

Record native steps, learner transitions, optimizer exposures, complete games,
parameters, collection/learning/export/arena costs, inference latency and observed
host contention. Keep interrupted games and illegal/capacity failures. Do not
claim equal inference compute merely because all arms use one CPU thread;
report latency differences under the common policy-only envelope. Report curves
against both learner transitions and cumulative active training cost. Compare
cost only on observed overlap using the last available checkpoint at each cutoff;
no extrapolation, winner selection or cross-seed uncertainty from this smoke.

The notebook/report regenerates offline from retained exports, contains the
eight resolved configurations and every attempt, and separates software promotion
from strength decisions. Masked padding invariance and token functionality may
pass; scientific superiority remains unresolved. A later multi-seed campaign
requires separately frozen budgets, cohort, held-out paired deals, anchors and
success thresholds. No ETU-91 file, process, frozen checkout or allocation changes;
no paid compute. W&B dashboards remain ETU-101's responsibility.

## Implementation sequence and acceptance

**This slice:** model configuration, masking/token/depth implementation and strict
checkpoint round trips. Focused test: `uv run pytest tests/model/test_value_aggregation.py
tests/model/test_categorical_value.py tests/model/test_agent.py` (new aggregation
test file). Verify padding payload/count invariance for masked/token modes,
valid-row sensitivity, finite gradients into token/attention/critic, preserved
action-focus indexes, WDL signed expectation and unchanged historical outputs.
Test actual hidden-world swaps with identical viewer observations; do not settle
for randomly generated tensors as information-safety proof. Test missing old
fields, declared mode round trips, bad metadata/weights, disabled attention and
compound rejection. Fixed deterministic fixtures establish loader behavior only.

Then add eight reproducible recipes and a thin experiment runner. Extend the
existing EvaluationProtocol study literal with `value-models`, without relaxing
existing frozen-study validators. Exercise executor continuation, raw/EMA export
admission and ordinary checkpoint player use with both deck assignments. The
gate command adds `tests/training/test_value_models.py`, existing
`tests/training/test_ataraxos_regime.py` and `tests/training/test_study.py`, then the
single bounded smoke and offline regeneration. Actual supplied candidate bytes
and selected-world admission remain required for a playable-candidate claim.

Finish with durable protocol/report documentation and ordinary PR/CI delivery
through the selected delivery steps. This kickoff does not publish or land code.
No Rust changes are planned; if needed later, native debug tests and the pinned
extension rebuild become required.

## Follow-on priority and unresolved science

Explicit viewer-safe recent-event input comes next. Begin a small-capacity x
history-on/off factorial, then repeat at one larger capacity point using the
capacity tooling; keep aggregation and learning rule fixed. Record that history
changes information, so compare its effect rather than asserting a pure capacity
gain. Pre/post normalization and richer action conditioning remain separate
contrasts. Learned recurrent memory needs reset, sequence-training, state export
and compute contracts and remains deferred. Richer belief encoders belong in
coordination with the existing frozen-policy sampler owner, with held-out joint
NLL/calibration preceding matched-cost search; no duplicate belief experiment.
ETU-104's broader architecture-recipe design still requires its own review.

Check: source/API inspection completed at db820056; no training or implementation
tests run during kickoff. Gate commands above are pending implementation.
