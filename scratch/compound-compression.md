# Compound compression

Keep native compound lowering, the recurrent decoder, complete-game credit and
ordinary checkpoint serving. CompoundStatistics owns accepted-game accounting;
the executor projects its totals into StageRecord instead of recounting factors.

Delete — do not maintain: unused CompoundOutput.entropies and CompoundGame.seconds
are removed. Conditional probabilities still support the training regularizers;
executor timing includes collection and replay. No remaining deletion targets.

`OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run pytest tests/training/test_compound.py -q`: 14 passed; changed-module Ruff and diff whitespace checks passed. Gate owns broader acceptance; scientific comparisons remain separately budgeted.
