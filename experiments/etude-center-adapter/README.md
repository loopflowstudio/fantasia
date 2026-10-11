# Private Fantasia adapter

This tenant-side package reads retained receipts or explicitly enumerated GET-only
native objects and posts through `etude_client`. It imports no server or Fantasia
runtime. It is a development workspace dependency, not part of the server image.
No publication or license is implied.

Set `ETUDE_URL` and `ETUDE_TOKEN_FILE` to a private write token (never a database
DSN). From this checkout:

```sh
uv run --python 3.12 etude-fantasia retained ../fantasia capacity-recovery-v3
uv run --python 3.12 etude-fantasia retained ../fantasia research-evidence
uv run --python 3.12 etude-fantasia native EXPERIMENT_UUID selection.json objects.json
uv run --python 3.12 etude-fantasia s3 EXPERIMENT_UUID s3://BUCKET/PREFIX JOB_ID
```

Native cuts validate all dependencies before one atomic ingestion. A failed cut
updates collection health without replacing retained facts. Historical collections
are bounded batches, as before; replay resumes safely after a failed batch.
Exact source bytes are retained when bounded; oversized runs are streamed and
verified by version, size and digest with complete ancestry and explicit omissions.
References never count as retained evidence. Source clocks are never fetch clocks.
See `docs/operations.md` for grants, recovery and live-access limits.

Use `retained ... --revision COMMIT` for exact original-revision replay. Without
it, matching working bytes are attributed to HEAD and dirty bytes stay unpinned;
a new revision is new provenance even when its bytes are identical. Research
citations already pin their own revisions and reject a global revision override.

`Reader` owns the cache, digest/size validation, large-source references and
envelopes. `fantasia.py` and `live_fantasia.py` only translate their distinct
schemas; the latter is the sole native dependency traversal. Restricted transports
perform I/O, and `cli.py` owns the sole CLI/session path. The stream parser remains
necessary for the large run and cannot be replaced with an unbounded JSON load.
