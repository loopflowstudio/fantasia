# Remote jobs that outlive the submitting laptop

Jack Heart requested design, autonomous implementation and a PR walkthrough before landing. The intended experience is: submit a bounded experiment, close the laptop, and later reconnect to the same job and its evidence. This additive capability should ship as one useful end-to-end PR, not just detached process plumbing.

## Existing authority and evidence

Build on landed ETU-114 (a108ed34). TrainingRun and VerifyStore own learning state and provenance; Experiment owns regimes and evaluation protocol; the existing S3 publication contract owns durable artifacts. Deployment owns rental identity, admission and cleanup. Keep these owners. Read AGENTS.md, manabot/README.md, docs/remote-training.md and the existing experiment/report/storage APIs before coding.

manabot/remote/deploy.py currently calls blocking SSH training, retrieves artifacts and deletes pods in the client's finally block. transport.py already installs an independent pod guardian. That bounds billing but does not make the experiment laptop-independent. ETU-103/PR #253 adds live exports, bulk transfers and capacity reporting; coordinate shared changes and preserve its active writer. Start from landed source; adopt compatible delivered work through normal integration rather than copying an active checkout. Existing sweeps completed before deletion; their subsequent retrieval errors are not proof laptop sleep killed training.

## Contract and main types

Extend manabot.remote, using fully typed domain objects and one lifecycle implementation shared by CLI and Experiment callers.

- RemoteJobSpec: stable caller-supplied or durably generated job ID, immutable plan digest, exact source, existing resolved training/evaluation plan, artifact prefix, hardware admission, absolute deadline and cumulative dollar cap. Persist intent before provider creation. Retrying that ID with different content fails.
- RemoteJobRecord: provider resource identity, lifecycle phase, remote heartbeat/update time, run/evaluation references, artifact generation, cost observations and terminal/error information. A stale heartbeat means unknown/unreachable, not finished. Keep provider absence, execution completion, artifact completeness and cleanup confirmation distinct.
- Remote supervisor: the sole execution owner after acknowledged handoff. It runs the existing learner, bounded milestone evaluator, artifact publisher and finalizer on the rental. The submitting process may disappear without cancellation. No new learning state machine or distributed training engine.

Use durable storage and conditional ownership to prevent concurrent submitters acquiring the same ID. A lost provider-create response must be reconciled by unique job identity before any retry creates resources; if ambiguity cannot be resolved, stop with actionable status. Do not promise exactly-once creation from a local lock. Scope credentials to existing secret policy, redact logs and avoid persisting secrets in public job metadata.

## Public behavior

Expose submit, status, logs/attach, fetch and cancel through the existing `uv run manabot remote` interface. Preserve existing useful run behavior as a wrapper around the shared lifecycle; an optional wait/follow only observes. Print the job ID and reconnection command. Reconnection from a fresh client cannot require the original local receipt or a living SSH session. Reuse current authentication and storage setup.

Submit may require connectivity until remote acceptance; expose the boundary explicitly. An interrupted pre-acceptance submit reconciles safely. After acceptance, setup/training/evaluation/upload/shutdown are remote-owned. Attachment disconnect and Ctrl-C end observation only; cancellation is an explicit remotely acknowledged request. Report unsupported pause/resume or CUDA crash recovery honestly. This PR does not require new exact learner process recovery; never reinterpret reconnect as restarting at initialization.

Keep evaluation resource limits declared. At least one real milestone evaluation must happen while the client is absent, using existing checkpoint/evaluation APIs. Periodically publish consistent run snapshots, logs, committed checkpoints and evaluation results to existing S3 storage. Upload immutable artifacts before publishing a manifest referring to them; validate hashes on retrieval. Do not upload a live SQLite file inconsistently. Notebook/HTML generation consumes these persisted artifacts after rental deletion.

Finalize uploads before normal deletion within a reserved deadline. An independent guardian still enforces the absolute billing limit when the supervisor crashes or storage is unavailable. Missing evidence remains explicit, not falsely completed. Retries never reset the original deadline or cumulative cost allowance. Provider outages may leave deletion unconfirmed; expose that fact and a safe reconciliation command.

## Proof and delivery

Focused automated integration tests exercise real subprocess detachment plus controlled storage/provider boundaries: killed submitter after acceptance, ambiguous creation, duplicate/concurrent submit, mismatched plan, stale heartbeat, upload failure, cancellation, supervisor failure and deadline. Do not equate a tmux demo with lifecycle acceptance.

One bounded live proof uses real CUDA training, an initial evaluation and a later milestone. Exit/kill the client after acknowledgement, verify updates and evaluation advancing from another connection, reattach from a fresh client, then retrieve verified checkpoints and a report after the pod is deleted. Save source, timings, costs, disconnect interval, evaluation evidence and final inventory; make no learning-strength claim from this smoke.

Reserve at most $3 TOTAL for all live proof attempts from ETU-103's existing $15 rental allocation; coordinate that reservation before renting. It is not a fresh allowance, and ETU-114's historic $50 is unavailable. Keep below-$5 deployment guards and live price admission. Leave mini ETU-105 and laptop ETU-118 compute/evidence untouched.

Implement, compress, run focused checks, preserve the lasting contract and proof in docs, and publish a descriptive PR. Prepare and headlessly render scratch/pr-review.html with user workflow, types/APIs, failure cases and observed evidence. Stop for Jack Heart's PR review; do not auto-merge or mark delivered. The task Flow is code (pursue then pr-review), not a design-review or landing Flow.

## Implementation cut

Delete — do not maintain: `deploy.deploy`'s client-owned bootstrap/train/transfer/
finally-delete lifecycle and the CLI's dependence on a local deployment receipt
for new runs. Preserve legacy receipt cleanup, cost admission, guardian proof,
source pinning and immutable artifact verification. Move ordinary run and new
submit/observe/fetch/cancel consumers onto one durable job owner. Existing
worked-example low-level helpers remain for frozen reproduction.
