# Executable training regimes

A `TrainingRegime` is an ordered recipe; a `TrainingRun` is one bounded execution
with resolved settings, named seed streams, artifacts, measured costs and status.
ETU-89 owns this infrastructure. ETU-90 owns its direct-RL treatment correctness;
ETU-91 owns the comparison/ablation protocols and analysis.

```bash
uv run manabot train --regime experiments/regimes/direct-self-play.json --seed 197 --out .runs/direct-pilot
uv run manabot train --regime experiments/regimes/search-distillation.json --seed 197 --out .runs/search-pilot
```

The supplied recipes are bounded pilots, not the proposed week-long experiment.
The ordinary preset command remains available. Combining `--regime` with a
preset or `--set` fails rather than silently ignoring overrides. Choose a new
output directory for every attempt; checkpoints are not process-resume files.

Stages are `collect_search`, `train_supervised`, and `train_self_play`.
A supervised stage's `datasets` name earlier collection outputs. Its `initial`
names an earlier supervised stage, carrying learner and Adam state; each source
game keeps its identity and validation assignment as the corpus grows. Game IDs
are unique within the run, and IDs divisible by ten form validation. At least
one complete game must exist in each partition. Self-play `initial` carries the
live collector/learner/optimizer within the same execution; streams pause at the
exact update boundary. External checkpoint reuse is not supported as implicit
resume. Unsupported operations, forward references, and incompatible runtime
worlds fail validation.

The recipe reuses `AgentHypers`, `ObservationSpaceHypers`, and authored
`MatchHypers`, including both sideboards. Architecture and match binding live
once per regime. Every stage declares its CPU device, float32 precision, one
worker, thread count, wall and memory limits. Learning settings independently
select estimators, filtering, regularization reference, schedules, and EMA.
The policy stays on the acting viewer's tensor inputs; private teacher metadata
is not a model input. Learner and behavior weights are raw; EMA is a separately
named evaluation output with its iteration clock, never a hidden behavior swap.

`VerifyStore` is the canonical SQLite owner for runs and stages. `run.json` is
an export of committed state. Files are atomically published before their
SHA-256 identities enter stage records. Each checkpoint uses the ordinary
writer and reload path; the ETU-75 world/setup contract owns compatibility.
A failed or interrupted stage retains its error, elapsed cost and previously
published artifacts. The final selection rule is the last complete raw output,
not the best seed or best observed evaluation score.

Collection, optimization and export time are separate from evaluation time.
Records distinguish complete games, environment decisions, learner transitions,
and optimizer exposures. Runtime/source/content/tensor identities and hardware
are saved at creation. The reproducibility contract is resolved settings and
artifact provenance, not byte-identical stochastic training or exact process
continuation. A fresh execution owns fresh costs; no pre-existing corpus is free.

[Learning-speed protocol](../experiments/training-regimes.md) and
[ablation protocol](../experiments/ataraxos-mtg-ablations.md) describe the bounded
smokes and the separately proposed scientific studies.
