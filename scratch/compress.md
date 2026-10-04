# Local-update compression

Local labels are derived during receipt admission and reused across minibatches
and epoch evaluation; public evaluation still admits its inputs. The source
shards remain immutable. Receipt constructors name provenance fields explicitly,
collection serializes each receipt once, and arena discovers local players once.
No obsolete public path was identified for deletion in this additive change.
Scientific acceptance and unsupported exact-history paths remain as documented in
`docs/local-policy-search.md`; this pass allocates no scientific run.

Validation: `uv run pytest tests/sim/test_local_update.py tests/training/test_local_update_stages.py tests/sim/test_search_supervised.py tests/sim/test_distill.py tests/sim/test_distill_datagen.py tests/training/test_regimes.py -q` — 35 passed in 21.94 s; changed-file Ruff and `git diff --check` passed; gate owns broader verification.
