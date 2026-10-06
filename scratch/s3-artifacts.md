# S3 artifact storage — 2026-10-06

Jack Heart accepted W&B as the metrics/viewing layer with model and durable
artifact bytes in S3. The latest proposed destination is
`s3://etudefantasia/manabot/`, superseding `s3://etudegg/manabot/`.
W&B destination remains `loopflow-studio/etude`.

Implemented explicit retained TrainingRun publication, content-addressed objects,
conditional creation, SHA-256 upload/readback verification, provenance manifests,
and atomic verified cache downloads. Ordinary checkpoint loading accepts pinned
StoredArtifact references and retains existing model/world admission. The older
trainer stops sending checkpoint bytes to W&B; historical W&B reads remain.
The dashboard CLI accepts an exact-run-bound manifest and publishes its metadata
without model files. See [the usage contract](../docs/training-monitoring.md#s3-model-and-artifact-storage).

Scope: stopped/completed run snapshots, named stage artifacts (including rejected
ones), monitoring checkpoints, fixed validation and recovery exports. This is not
recursive directory backup, automatic live archival, portable training recovery,
or a migration of historical absolute paths. Single objects over 5 GiB fail.
The publisher does not create buckets, delete objects, or change permissions.
Jack Heart separately authorized bucket creation after the initial access check.

Validation: 10 focused offline storage/checkpoint/backfill checks passed across
the focused invocations; lint, formatting and diff checks passed. Saved-evidence
preflight verified all 36 artifacts (30,879,360 bytes) across the six history runs.
No training, evaluation games or source evidence mutations occurred.

Jack Heart completed AWS login and authorized creating `etudefantasia`. Created
in `us-west-2`, with bucket-owner-enforced ownership, all public-access blocks,
AES256 default encryption and versioning. Six runs are now archived: 48 objects,
93,001,518 bytes, including the 36 artifact blobs plus exact producer exports and
manifests. Every upload passed full readback; all references include version IDs.
An independently downloaded manifest matched the local manifest; its endpoint raw
checkpoint passed ordinary world/schema/model loading (138,498 parameters).
No training or games ran. Six W&B training streams now contain matching S3 metadata
with original friendly names restored. History remains 500 rows per stream.

The first publication uploaded blobs but failed writing a manifest into a missing
local directory. The publisher now creates the directory before network writes;
retry reused the blobs and preserves the version ID returned by readback. Seven
focused storage tests pass after this fix, including nested output and retry.
The first W&B verification assumed nested summary keys; the live API flattens
them with dots. Verification now checks every flattened storage field exactly.

Receipts: `.runs/etu117-demo/s3/{bucket-verification,roundtrip-verification,wandb-reference-verification}.json`
and one `artifacts.json` plus `artifacts.receipt.json` per run. Bucket inventory
matches these 48 referenced objects exactly. No live blocker remains. Automatic
live archival and removal of local originals remain outside this implementation;
publication is explicit. No PR landing is authorized.
