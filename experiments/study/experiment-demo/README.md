# Editable Experiment demo

Open [comparison.ipynb](comparison.ipynb): one headlessly executed notebook with
35 editable plots for both model widths and both training seeds, milestone rates
and deal uncertainty, comparisons, resource diagnostics and costs. Rerun its cells
from this directory to refresh these retained inputs without training or tracker
access. The last cell demonstrates preservation of an added personal note.

This is a tiny software fixture, not a scientific comparison. Four single-update
TrainingRuns produced four raw milestone cohorts and 16 exact-replayed games.
The final execution receipt records 50.78 elapsed seconds and 61.30 additive
learner/evaluator process seconds, including 47.17 evaluator seconds. Notebook
execution was a separate headless acceptance check. One monitoring deal per cohort
cannot establish useful uncertainty or strength. No defaults or scientific plans
changed. Earlier process/game timeout attempts remain in the Task checkout's
`.runs/etu113-validation/{initial-timeout,game-timeout}`.

These 14 notebook/record exports were copied byte-for-byte from the final gate
fixture; `manifest.json` pins their bytes. Absolute source/checkpoint/trace paths
inside them retain their original provenance. Model binaries, SQLite and command
tapes remain in the original Task checkout under `.runs/etu113-validation/gate`;
they are unnecessary for notebook plotting and are not republished here. Copying
the exports does not re-admit a checkpoint or claim a fresh replay.

The editable declaration is
[experiment_demo.py](../../runners/experiment_demo.py). The shared runner generates
this same notebook for ordinary executions. See the
[execution guide](../../../docs/experiment-execution.md) for launch, placement,
continuation, budget and interpretation contracts.
