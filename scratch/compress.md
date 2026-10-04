# ETU-93 compression

Selection indexes own PPO's pre-shuffle order; derive its mask from those
indexes instead of sorting twice. Both learners share the empty-safe selected
mean, and the move learner reuses its reference distribution for diagnostics.
The protocol's combined deal-family checks already cover range, duplicates and
overlap, so the redundant development-only checks are removed.

Delete — do not maintain: no remaining deletion targets. Keep both estimators,
filter semantics, frozen recipe defaults and evidence identities unchanged.

`uv run pytest tests/training/test_omitted_controls.py tests/training/test_rl_objectives.py tests/training/test_ataraxos_gradients.py tests/training/test_study.py -q`: 72 passed; Ruff check/format and diff whitespace checks passed. Gate owns broader verification; scientific acceptance remains unmeasured.
