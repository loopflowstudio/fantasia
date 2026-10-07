# Remote jobs that outlive the submitting laptop

Jack Heart requested autonomous implementation and publication, then a source-pinned
PR walkthrough before landing. Jack Heart approved PR #254 on 2026-10-06 (recorded comment
83e7f9e0-724c-4302-aacd-c625803a4d73) and authorized `lf land -c` after preparation/CI.
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

Resource admission now belongs to `Resource.validate_for`; cancellation reads
belong to `job_store`. Both client and supervisor consume those shared contracts,
so the worker no longer imports the submission client. Behavior and persisted
schemas are unchanged.

## Delete — do not maintain

Completed: client-owned bootstrap/train/transfer/finally-delete orchestration,
the old CLI namespace, and the client-private `_bound_resource` helper. Keep
legacy receipt cleanup and worked-example transport helpers for frozen
reproduction. No further deletion targets remain in this cut.

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

The refreshed walkthrough pins source `81100af3`, including the shared-contract
refactor at `8ecf6e45`; subsequent handoff edits change review artifacts and these
notes only. All eight code excerpts match the pinned source exactly. The fetch/report
transcript remains attributed to its earlier deploy-only review pass at `b4e861e4`.
Rendering is unavailable in this headless Session; retained desktop/narrow PNGs
predate this refresh. HTML and the focused code-capture page are updated.

The publication copy retains deploy-only commands, the completed live proof and
its source limits. CI run `37566288029` has passed Python, protocol conformance
and clean-machine play plus the visual gate; Rust is still running, with no
reported failures at this check. Gate owns any remaining affected-suite checks.
Jack Heart's recorded “254 looks fine” satisfies the saved review boundary; no
repeat review is required. Landing is authorized with Task completion after merge.
Four-hour credential support is outside this PR; ETU-103 remains limited to the
current SSO window below 3,540 seconds including reserves. Full private
proof stays in `.runs/etu123-disconnect`; compact hashes/costs are in
`experiments/data/etu123-remote-jobs`. The requested proof was not restarted for
CLI naming or the counter repair.

Check: `uv run pytest tests/remote/test_jobs.py tests/remote/test_cli.py -q` — 32 passed after the shared-contract refactor; focused Ruff and diff checks passed. Earlier 94-check gate and live proof remain retained. Handoff check: eight exact source excerpts, internal links, capture-page pin and `git diff --check` passed; rendering unavailable.
