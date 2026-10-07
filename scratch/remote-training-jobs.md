# Remote jobs that outlive the submitting laptop

Jack Heart requested autonomous implementation and publication, then a source-pinned
PR walkthrough before landing. PR #254 remains unmerged for Jack Heart's review.
The original design is retained at `076bb5e5`; current contract and proof live in
[docs/remote-jobs.md](../docs/remote-jobs.md).

## Reconciled implementation (2026-10-06)

`uv run manabot deploy` is the sole public lifecycle namespace, per Jack Heart's
two naming corrections. Direct `--plan` or `--regime/--mix` submission shares the
explicit `submit` implementation; status, logs/attach, fetch, cancel, reconcile and
report reconnect by ID. No alias or hidden historical namespace is registered.
Internal Python modules and frozen proof commands retain their names.

The client-owned deployment lifecycle was replaced by provider startup and one
remote supervisor. S3 conditional create claims bind exact intent and fence
ambiguous provider requests. Retrying never resets the deadline or rents a
replacement. Stale heartbeat, completed execution, complete evidence and confirmed
deletion remain separate. CUDA process recovery is rejected, never restarted.

TrainingRun/VerifyStore, Experiment, S3 artifact storage and reporting remain their
existing owners. PR253 `e052ac30` was integrated through `lf sync`; its checkout
was untouched. Initial/raw exports, CheckpointQueue, Bundle and live-export
relocation are shared. Arbitrary client SSH callbacks fail before rental; pinned
historical examples retain low-level helpers for reproduction. Capacity science
was not launched.

Scoped SSO worker credentials required a dedicated role trusting the current
principal, with no provider account access. The role-chain deadline is under one
hour including reserves. The first paid attempt exposed missing-key S3 403 behavior;
submission now creates its empty cancellation mailbox before renting. No bucket
listing grant was added. Provider startup begins setup; observed acceptance follows
source and resource admission. The independent guardian owns the absolute deadline.

## Retained proof and remaining delivery

Jack Heart confirmed the $3 reservation inside ETU-103's $15 allocation. Both
ETU-123 attempts total $0.1158450 estimated; inherited ETU-103 spend brings the
shared estimate to $0.6518216. All rentals are deleted. No ETU-105/118 compute or
evidence was changed. No scientific allocation or learning-strength claim follows.

At pinned `def37708`, the client exited at zero updates. The rental completed
160 CUDA updates, an initial evaluation and two later evaluations, 12 complete
games, and final publication/deletion. Another client fetched 48 verified files,
admitted four policies and regenerated notebook/HTML after deletion. The final
status poll lagged at 139; the authoritative database held 160. Current status
uses that database, with a regression; frozen evidence is unchanged.

The final API/reporting corrections are published in PR #254. The walkthrough
binds implementation head `b4e861e4`; later heads change review artifacts only.
Desktop/narrow layout and code excerpts were rendered and inspected. Remaining:
the saved Flow must reach its pr-review boundary, and Jack Heart reviews before
any merge. This running implement Session cannot mark that human review complete. Full private
proof stays in `.runs/etu123-disconnect`; compact hashes/costs are in
`experiments/data/etu123-remote-jobs`. The requested proof was not restarted for
CLI naming or the counter repair.

Check: `uv run pytest tests/remote tests/training/test_checkpoint_queue.py tests/training/test_artifact_storage.py -q` — 94 passed, one CUDA-host skip; live proof above.
