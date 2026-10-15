# manabot

The trainable agent of Fantasia: environment wrappers, models, search,
training, and verification. You train *a* manabot; this package is how.

## Quickstart

```bash
uv run manabot train              # --preset local: bounded laptop run
uv run manabot train --preset simple    # full PPO run (CUDA, W&B)
uv run manabot sim --preset sim --set sim.hero=attention --set sim.villain=simple
uv run manabot belief-demo        # engine-derived belief/intervention proof
uv run manabot belief-learn-demo  # held-out frozen-population belief proof
```

The default `local` preset is the certified laptop path: it trains a small
manabot on CPU in under a minute, needs no W&B account or CUDA, and saves
checkpoints to `.runs/local/step_N.pt`. The `simple` and `attention` presets
are real training runs: they expect a CUDA machine (see
[remote training](../docs/remote-training.md)) and track to the `manabot` Weights &
Biases project. New checkpoints stay local until explicitly published to
[S3 artifact storage](../docs/training-monitoring.md#s3-model-and-artifact-storage).
W&B tracks metrics and S3 references; the historical W&B model reader remains
available for previously published checkpoints.

Override any hyperparameter with `--set dotted.path=value`; presets live in
`manabot/config/presets.py`.

For an identified Allies/Lessons opponent, use the bounded
[train/export/play workflow](../docs/local-trained-challenger.md). It uses the
existing search-distillation trainer and a server-pinned candidate; players see
the bot's identity in the ordinary table. The `local` PPO preset above remains
a separate default-deck training smoke.

Build named curated matches with `MatchHypers.authored(pack_key, hero_deck,
villain_deck)` so both main decks and sideboards come from managym's compiled
setup. Custom `hero_sideboard` / `villain_sideboard` maps default to empty and
require positive integer counts. `Match.swapped()` moves both lists together;
`Env.reset(options={"match": match})` also replaces the setup used by auto-reset.


Submit bounded cloud work and reconnect after the laptop disconnects with
[`manabot deploy submit/status/fetch`](../docs/remote-jobs.md). Training, checkpoint
evaluation, verified S3 snapshots and shutdown belong to the remote job; reconnecting
does not restart the learner or promise CUDA process recovery.
Use `Experiment.cohort` and `manabot deploy cohort start` on an always-on host to
sequence a frozen cohort independently of the submitting terminal or chat.
Cohort status/cancellation reconnect through the same private control storage.
New self-play jobs use exact absolute update checkpoints (`checkpoint_updates`,
default 1,000); freeze targets and shared intervals before launch. Operational
lease and spending limits remain in hours/dollars. See [cadence and continuation](../docs/training-monitoring.md#new-training-and-live-dashboards).

## World identity

Ordinary checkpoints require `world_binding` from
`manabot.model.world.checkpoint_world(actual_player_configs, observation_space)`.
This binds native `WORLD_VERSION`, rules schemas, full deck/sideboard pairs,
content manifest and input schema. Missing or mismatched bindings fail before
weights load. Seat reversal preserves each deck's sideboard. BC and value
writers require explicit `player_configs`; never infer training setup from
tensor dimensions or the default deck.

For the compiled Allies/Lessons matchup, use
`AgentSpec(semantic_pack="ur-lessons-vs-gw-allies")`. The ordinary model joins
viewer-safe `semantic_cards` transport IDs to complete checked catalog programs,
including characteristics and referenced definitions; `known_hand` contains
public definition minima, not hidden hand slots. Selected compiled checkpoints
without that semantic input fail admission. Generic uncompiled training keeps
its existing bounded feature model. These models do not certify strength or
semantic transfer; no previous checkpoint is relabeled compatible.

An observation/action-shape or rules-meaning change is a world version.
The current world is **w6** (`managym.WORLD_VERSION`); its rules, tensor shape,
and compatibility limits are in [WORLDS.md](../WORLDS.md). Earlier checkpoints,
including w5 artifacts with aliased object and mode choices, are not compatible
with w6. The local
