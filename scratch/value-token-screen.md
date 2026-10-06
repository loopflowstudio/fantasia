# ETU-106 follow-up preparation

Jack Heart requested a separate three-arm scalar screen after PR #222 merged.
`lf task status ETU-106` found the Task open at stale review; `lf pr next
value-token-screen` rotated PR 2 onto current main be6260d9, including ETU-104's
merged recipe helpers. No old review is treated as approval of this diff.

The durable protocol is experiments/value-token-screen.md. No scientific training
or paid compute runs here; fixtures exercise scheduling and failure behavior.
Deliver through gate and pr-publish; preserve Task for unrun empirical work.

Gate: `uv run pytest tests/training/test_value_screen.py tests/training/test_value_models.py tests/training/test_study.py tests/training/test_architecture_recipes.py -q` — 31 passed; focused Ruff and diff whitespace passed; CI owns broader matrix.
