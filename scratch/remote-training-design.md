# Remote training: compile a regime onto a hardware mix and run it on RunPod

2026-10-06. Draft design from Jack Heart's direction in conversation. The
direction and constraints below are Jack's; the data model, command names and
file layout were agent-selected and remain unreviewed by Jack. Reconciled against
implementation and live evidence on 2026-10-06; the bounded proof passed.

## Live execution update — 2026-10-06

Jack Heart authorized $50 across failures and successes, exact-source branch
pushes, and real CUDA self-play before review. PR review/readiness and landing
remain prohibited. The [remote contract](../docs/remote-training.md) owns exact
attempts, costs, artifact identities and limits.

Attempts 004 and 005 completed 700 and 1,200 CUDA updates in 27.73 and 42.96
minutes. Both returned verified raw/EMA/Adam and authoritative records, and each
played four terminal exact-replayed arena games. All failed attempts remain.
The rented-hardware CUDA suite passed two tests. Inventory was empty afterward.
Main's ETU-119 persistence fix is merged; neither completed run was rewritten.

Jack Heart then required local-disk setup and a small worked reuse example.
Attempt 006 put source/environment/cache under /opt/manabot, keeping returned
evidence on /workspace. Bootstrap took 90 seconds (uv sync 53, native build 20);
the comparable environment-to-toolchain interval fell from 486 to 71 seconds.
This is one observation per placement, not a controlled performance claim.
Sixteen CUDA updates and four replayed arena games passed; inventory was empty.
Total including shakedown through 006 is $1.6160 estimated/reported, not invoiced.
The existing five-minute example setup reserve is supported by this bounded run.

The two-experiment example passed at f4189656. Both seeds returned verified
records/raw/EMA exports and ordinary loader admission. Training took 30.06/25.58 s;
setup was 114.57/0 s, charged once. The pod was deleted and inventory was empty.
Total including every failure and shakedown is $1.6591 estimated/reported. It sets up one pod once,
runs seeds 197/198 at the same pinned commit with --no-sync, returns separate
records and deletes under one hard deadline. No public API, reuse mode or flag
was added; the default remains one self-deleting deployment. The earlier idle
reuse abstraction requirement was superseded. ETU-120 is folded/cancelled;
prebuilt images remain ETU-121. ETU-108/larger-model work stays separate.

Check: remote suite 45 passed/one local CUDA skip; merged persistence/continuation
checks 3 passed; worked-example success/failure checks 2 passed. Real two-run
example passed; the final remote suite passed 47 checks with one local CUDA skip. No strength or chapter acceptance follows.

## Direction from Jack Heart (accepted)

- Build "a great framework for compiling and deploying training regimes onto
  specific hardware mixes", all on RunPod for now. Fly.io or AWS may host CPU
  workloads later; do not build for them yet, but do not preclude them.
- Purpose is initial direction setting: learn the performance characteristics
  of larger models, at least Ataraxos-sized. Not an attempt to match Ataraxos's
  training scale (16 H100s for a week).
- Budget: up to &#36;250/week on GPU, paired with up to &#36;250/week on CPU. No need
  to spend it all. The goal is a clear target: which distribution of compute
  reaches milestone Y in time X at cost &#36;Z, with informed reasoning.
- No account information in the repository. Plain inventory statements are
  fine, e.g. "we currently have 1 GPU of type L4 rented on RunPod".
- Do not rent the real training machine until the software is explored. Cheap
  short rentals to find process bugs are approved.

## Evidence from the 2026-10-06 shakedown

One RunPod L4 pod (Secure Cloud, &#36;0.49/hour, 6 vCPU, 62 GB), deleted after
about 35 minutes; cost &#36;0.29. Source `fd7437df`. One run each; no repeats.

- Clean clone to working environment in about 90 s: `uv sync --python 3.12
  --extra dev --extra play` 62 s (CUDA torch 2.10.0+cu128 resolves from the
  existing lock), `uv run maturin develop --release --features python` 20 s.
- `tests/training tests/sim/test_net_opponent.py`: 361 passed, 2 skipped in
  553 s with `--extra dev --extra notebook`. Without the notebook extra one
  test fails on `nbclient`.
- `torch.cuda.is_available()` is true with the pinned build.
- **The pod reports the host's 48 CPUs** through `nproc`, `lscpu` and
  `os.sched_getaffinity`; it was allocated 6. `/sys/fs/cgroup/cpu.max` is
  absent. Core counts must come from the rental declaration.
- `runpodctl` 2.14.0 `pod create` has no auto-terminate or stop-after flag.
- Stock was "Low" for every card under &#36;0.80/hour; two of three create
  attempts failed with "no longer any instances available".
- Simulator benchmark (`distributed_benchmark --mode simulator`): 25,555
  surfaced decisions/s on one EPYC 9254 core, against 33,521 on the mini.
- Generic transformer encoder probe on the L4 (not manabot's model):

| Model | Tokens | Batch | Precision | Train samples/s | Peak GPU GB |
| --- | --- | --- | --- | --- | --- |
| 1x64 | 64 | 1536 | bf16 | 113,003 | 0.4 |
| 2x128 | 256 | 1536 | bf16 | 6,724 | 4.6 |
| 4x256 | 256 | 1536 | bf16 | 1,668 | 17.1 |
| 8x384 ff1536 | 64 | 1536 | bf16 | 2,135 | 12.6 |
| 8x384 ff1536 | 256 | 256 | fp32 | 204 | 14.7 |
| 8x384 ff1536 | 256 | 1536 | either | out of memory (23 GB) | — |

  One CPU thread trains 8x384 at 256 tokens at about 2 samples/s.
- Default observation capacity is roughly 270–300 token slots (60 cards and
  40 permanents per player, 64 actions, players). Token count therefore
  decides both memory and throughput; this was not measured on manabot.

At shakedown source `fd7437df`, `Execution.device` was CPU-only, workers
`Literal[1]`, threads at most 4 (`manabot/training/models.py`);
`AgentSpec.attention_layers` is `Literal[1, 2]` and the feedforward size is
fixed at heads × width (`manabot/infra/hypers.py`, `manabot/model/agent.py`).
That source still held the parked AWS machinery, since removed by this Task.

## Implementation plan (reconciled 2026-10-06)

Status: Jack Heart's direction and Task acceptance above are binding. The
implemented choices below are agent-selected and reversible, not a claim of
human design approval. Remaining acceptance work is identified separately. No rental or training occurred during kickoff.
The current chapter is Trained Challengers. This delivers its reproducible
training infrastructure; a bounded deployment is not strength, general demo
admission, or human-play acceptance. ETU-108 and the larger-model Task remain
independent.

### Demo and command surface

From the laptop:

```bash
uv run manabot remote compile --regime regime.json --mix ops/mixes/runpod-small.json --seed 197 --out plan.json
doppler run --project etude --config prd -- uv run manabot remote run --plan plan.json --out .runs/remote-smoke
```

Also permit `remote run --regime ... --mix ... --seed ... --out ...` to compile,
write and display the same plan before provisioning, with no interactive prompt.
`remote status` lists current rentals and hourly charges; `remote cleanup
--deployment ...` retries deletion for an owned deployment. These commands are implemented and attempt 004 supplies the bounded live proof.

Success prints the evidence directory, verified checkpoint paths, estimated
dollars and confirmed deletion. Receipt timestamps retain observed rental
elapsed time, not invoiced billing. The explicit live helper then exercises the
returned checkpoint through the existing laptop arena. `status` reads inventory
counts and aggregate hourly compute charges; it does not reconcile receipts.
Training success with missing artifacts or unconfirmed deletion fails deployment.

### Findings that determine the design

- The original CPU-only schema concealed three device owners. Execution now
  passes CUDA to Agent, SeatRoutedCollector and Experiment before optimizer
  construction; PPO/Ataraxos use `trainer.experiment.device`. Float32, one
  worker and one to four declared threads remain the supported limits.
- `recovery.py::UpdateSnapshot` captures CPU Torch RNG and restores on CPU.
  It promises same-host recovery, not CUDA or portable process recovery.
  CUDA recovery must fail admission in this slice, including automatic recovery
  snapshot configuration. Existing CPU recovery remains unchanged.
- Monitoring reload now preserves CUDA device 0 RNG as well as CPU RNG.
  Collection and learning boundaries synchronize CUDA for charged timings;
  the GPU execution check remains skipped on this CPU host.
- `VerifyStore` owns TrainingRun/stage records; run.json is an export. Records
  and artifact references contain absolute producer paths. A copied SQLite file
  alone is insufficient to locate returned artifacts. Preserve original bytes
  and use one verified relocation manifest, described below.
- The ordinary `load_checkpoint_agent` already maps weights to CPU and validates
  saved architecture, observation and world binding. Returned CUDA policy
  exports need no state-dict port. Optimizer/recovery files are not policies.
- `arena.match.selected_match()` supplies the authored Allies/Lessons setup.
  Supply the actual match and observation space to `runtime_fingerprints`;
  its default Interactive mirror is not the selected-world identity.
  `play_cell` and `arena.replay` already own bounded games and Command replay.
- `GameSession` owns play state, canonical decisions and AttemptStore; `Trace`
  retains end state and optional authority-private canonical replay. The table
  Command binds match, revision, prompt and offer. Remote training does not
  require another session, replay protocol or checkpoint identity store.
  This Task makes no new crash-durability claim about play traces or automatic
  passes being human decisions.
- The shakedown's reported host cores are not rented cores. Thread allocation
  must never use affinity, `os.cpu_count()` or cgroup discovery as authority.
- RunPod supports pod creation, listing and deletion through its documented
  REST v1 control plane. Creation declares minimum CPU/RAM per GPU and returns
  assigned resources and hourly cost; the inspected create schema has no
  maximum-price field. Client price checks are admission, not an atomic provider
  spending cap. [Create API](https://docs.runpod.io/api-reference/pods/POST/pods).
- Stopping preserves billable volume storage; termination removes pod-local
  storage. Retrieve before deletion, use no network volume, and confirm absence
  after DELETE. [Lifecycle](https://docs.runpod.io/pods/manage-pods),
  [delete API](https://docs.runpod.io/api-reference/pods/DELETE/pods/podId).
- Official runpodctl documentation describes an automatically provisioned
  pod-scoped key. This does not prove that the chosen image/key can self-delete.
  The first bounded rental must exercise deadline self-deletion before the
  training proof, with laptop cleanup armed. Installed local CLI is 2.14.0;
  do not assume current upstream flags exist there.
  [Official CLI source](https://github.com/runpod/runpodctl/blob/main/README.md).

### Chosen architecture

Keep execution in `manabot.training`; put deployment lifecycle in the packaged
`manabot.remote` module, exposed by `manabot.cli`. `ops/` becomes checked-in
hardware examples and a short pointer to `docs/remote-training.md`, not a second
trainer. A small typed RunPod client implements create/get/list/delete and
price/resource inspection over HTTPS with bounded timeouts. Do not introduce
an AWS/Fly provider hierarchy. Provider is currently literal `runpod`.

Three records have different owners:

1. **HardwareMix / DeploymentPlan**: frozen, versioned Pydantic values. A mix
   contains one literal training role with one GPU,
   ordered GPU type alternatives, declared vCPUs/RAM, disk sizes, pinned image,
   thread limit, hourly ceiling, total dollar cap and total wall allowance.
   Compilation retains input regime bytes/digest and emits a complete validated
   resolved TrainingRegime, source commit/tree, lock digest, seed, cost
   projection and reserved setup/transfer/cleanup time. The source tree binds
   bootstrap/guardian bytes; no separate bootstrap digest or placement table
   is needed for this one-role implementation.
   Source must be committed and available to the pod; reject source drift on
   launch. No credentials, account IDs, SSH identities or live pod IDs enter
   these shareable files.
2. **Deployment receipt**: private operational state outside Git, under the
   requested ignored run directory, permission-restricted. It binds plan digest,
   unique deployment name, rental attempts, provider handles, deadlines,
   observed prices, latest phase and deletion evidence. The separate bundle
   manifest owns transfer hashes; the receipt is not a phase-event ledger.
   It does not duplicate training metrics. Persist intent before create and pod
   identity immediately after create. Never serialize raw provider responses,
   environment maps, headers or account information into public evidence.
3. **TrainingRun / VerifyStore**: unchanged training authority on the pod.
   Download a closed database or SQLite backup plus the full run artifact tree.
   Preserve original database, run.json and checkpoint bytes. A transport
   manifest maps producer absolute paths to local relative paths and binds
   sizes/digests. A single typed resolver verifies files beneath the bundle root
   and returns the local checkpoint path for ordinary loading/evaluation.
   It must reject traversal, symlinks, missing files and digest mismatch. It
   never rewrites frozen producer paths or costs. Remote process recovery and
   transparent support by every historical report consumer are not promised.

The first deployment compiler accepts self-contained ordinary `train_self_play`
regimes (PPO or Ataraxos, scalar or WDL, raw/EMA), including successive live
stages on the same device. It rejects external artifact dependencies, compound,
belief/search/supervised stages, recovery and unsupported devices before rental.
This is an explicit capability boundary, not permission to ignore those stages
or silently run them on CPU. Local CPU regimes keep all existing operations.
Later stage capabilities can extend this same compiler without another executor.

For this slice workers remain one: that is the executor's supported concurrency,
not an inferred machine capacity. Resolve threads to
`min(requested_threads, declared_vcpus, mix.thread_limit, 4)` and show the resulting value; validate
positive resource quantities. Streams are algorithm settings and stay unchanged.
Reject insufficient assigned CPU/RAM/GPU before bootstrapping training. Declared
memory is an admission bound, not a claim of enforced process RSS or freedom
from CUDA OOM.

CUDA wiring sets the model, collector, frozen behavior copies/EMA and Experiment
to the declared device before constructing the optimizer. Keep initialization
order stable for CPU. Validate continuation device equality. Synchronize CUDA
before/after charged phase boundaries; retain actual GPU model/memory, driver,
Torch/CUDA versions and assigned resources alongside host observations. Add GPU
receipt fields only for CUDA; existing CPU receipt meaning and recipe defaults
must remain unchanged. No AMP or precision treatment is introduced.

### Rental lifecycle, deadlines and cost

Use one deployment lock and one active pod at a time. Create a unique opaque
name per attempt. Filter declared GPU types by price, submit admitted alternatives
in one create with provider `custom` priority, then verify returned rate and
resources. No client-side create retry is implemented. An over-ceiling rental is deleted immediately and its cost recorded;
no training starts. Never retry a timed-out create blindly: reconcile by the
unique deployment name, delete any owned ambiguous matches, and require confirmed
absence before another create. If reconciliation fails, stop and report possible
billing. Never delete unrelated rentals.

The plan projects `(hourly compute ceiling + storage allowance) * total hours`,
with setup, transfer and cleanup reserves inside that allowance. Count provisioning, image pull, bootstrap,
training, evaluation on pod if any, retrieval, failure and deletion time. Reserve
five minutes for setup, five for transfer and two for cleanup in the small
example; require stage watchdog totals plus reserves to fit the rental allowance.
Returned compute rate is checked against the ceiling; storage remains a declared
allowance, not a fetched invoice. The absolute command deadline starts before
the guardian probe and is never extended for training. Probe and bootstrap share
the setup allowance; there is no dynamic deadline shortening by rate.
Estimated accrual and provider billing evidence are distinct. Record unknown
billing as unknown, never zero. The weekly allocations are authorization ceilings,
not a scheduler or permission to run a larger experiment.

Install a pod guardian as part of container startup, before source checkout or
Python bootstrap. It uses the original absolute deadline and pod-scoped credential
through the image-provided runpodctl configuration, then deletes its own pod. It must survive SSH loss and training-child
failure. The checked-in shell guardian invokes image-provided runpodctl independently
of the uv environment;
never copy the laptop's Doppler account key to the pod. If scoped self-delete is
not supported, stop the bounded probe and return the capability failure; do not
weaken the deadline contract or escalate credentials implicitly.

The laptop concurrently supervises all phases with timed subprocess/network
calls and a `finally` deletion path for ordinary exceptions and signals. At
normal completion it downloads and verifies artifacts, then deletes. At the
SSH phase deadline it stops waiting and enters deletion; it does not attempt
a second retrieval after timeout or independently prove child-process exit.
Pod termination remains the training-stop boundary. Missing evidence stays visible.
The guardian is not proof against provider outage, a container that never starts,
or simultaneous laptop loss before startup. Such states retain an unsettled
receipt and explicit cleanup command; no claim of a guaranteed dollar cap under
provider failure. `remote cleanup` retries deletion using the private receipt;
`remote status` only reads inventory.

A deletion acknowledgement alone is insufficient: GET must confirm missing or
list must confirm absence. Retry deletion within the cleanup reserve; on exhaustion
exit nonzero with prominent `CLEANUP UNCONFIRMED`, owned pod handle, hourly rate
and the cleanup command. Do not report “nothing billing” when the API is down.

### Bootstrap and retrieval

Use HTTPS for the pinned public source commit and SSH for control/file transfer.
Credential lookup stays in the caller's Doppler environment; credentials never
enter argv, saved commands, plans, logs or run bundles. SSH uses a generated
per-deployment key beneath ignored `.runs`, a dedicated known-hosts file, and first-use
host-key binding; unexpected subsequent keys fail closed. Do not disable host-key
checking globally. Runtime pod/address handles stay in private receipts only.

Clone source to `/opt/manabot/repo` and set `UV_CACHE_DIR=/opt/manabot/uv-cache`;
keep only evidence/recipes on `/workspace`. Bootstrap with `uv sync --locked --python 3.12 --extra play`, then from repository
root `uv run maturin develop --release --features python --manifest-path
managym/Cargo.toml`. Pin/record uv, Rust and image identity; keep all Python
commands under uv. Execute `uv run manabot train --regime ... --seed ... --out ...`
through the existing CLI. Training output is redirected into the returned evidence
log; there is no live log stream. Receipts retain the latest deployment phase.
A CUDA availability failure aborts instead of falling back to CPU.

Successful transfer verifies every declared artifact, including non-policy files,
and closes/backs up SQLite before final hashing. Select raw/EMA policy artifacts
explicitly for loader admission. A failed transfer retains the partial bundle and
manifest state, does not fabricate a completed TrainingRun, and never extends
rental life past the deadline. Download resume is unimplemented; deployment
requires a fresh directory. Portable process recovery remains unsupported.

### Alternatives and failure lessons

- Wrapping the old AWS job manager would inherit SSM, Docker bootstrap and a
  second job database with no needed RunPod behavior. Delete that path instead.
- Shelling out to arbitrary installed runpodctl versions makes response parsing,
  ambiguous creates and cleanup brittle. Use the documented REST surface for
  the laptop; a pinned guardian implementation owns pod deletion.
- Copying rewritten TrainingRuns would silently change frozen evidence. Keep
  originals and resolve physical locations separately.
- Multi-pod collection or a large cluster planner would delay the concrete win.
  Named roles preserve room for later CPU evaluation without implementing it.
- Successful use means a plan explains cost and placement, a small recipe reaches
  GPU execution without hand setup, and interruptions still have visible cleanup.
  The failure to avoid is a green training log beside a lost checkpoint or a
  forgotten bill. Neither more abstract providers nor more strength metrics
  addresses that failure.

### Delete — do not maintain

- Removed: `ops/{aws,bootstrap,job,provider,sandbox}.py`, `ops/__init__.py`,
  the AWS Dockerfiles, shell entry points and YAML specs, their exclusive
  `tests/ops/` fixtures, and the boto3/ops dependencies. Git retains them.
- Removed: `manabot/remote/pack.py`. The producer invokes
  `uv run python -m manabot.remote.bundle`; the bundle module owns manifest
  writing, safe destination paths and byte verification together.
- No remaining deletion targets. Preserve immutable shakedown evidence.

### Implementation state (2026-10-06)

The parked AWS modules, images, specs and exclusive tests are removed, with boto3
and the ops extra. `manabot.remote` now supplies validated plans, declared
placement, a bounded RunPod client, startup guardian, SSH bootstrap, immutable
bundle resolution and compile/run/status/cleanup commands. CUDA reaches ordinary
self-play model/collector/Experiment before optimizer construction; continuation
requires the same device. Unsupported CUDA stages and recovery fail admission.

The provider supports ordered GPU alternatives in one create using `custom`
priority; the implementation uses that instead of multiple create attempts.
Ambiguous creation is never retried. An empty inventory alone cannot settle an
unobserved timed-out create; cleanup watches for delayed provisioning and keeps
unknown billing visible. Both the guardian probe and training share one command
deadline. A new command requires a fresh receipt directory.

Source must be committed and publicly fetchable before rental. The example image
uses its resolved immutable Docker Hub manifest digest. Bootstrap pins uv 0.8.22
and Rust 1.98.1, records toolchain/GPU driver versions and uses the locked Python
3.12 runtime. Plans bind the complete source tree, including bootstrap/guardian.
SSH receives only PATH/HOME/SSH_AUTH_SOCK from the laptop, excluding Doppler/account
keys. First-use host keys stay in the private deployment directory.

The explicit `tests.remote.live_acceptance` helper accounts all retained attempts
under `.runs/remote-acceptance` against $4.90, requires raw/EMA optimizer work,
verifies returned TrainingRun/SQLite and artifacts, and uses the existing arena
monitor evaluator for one four-leg terminal/replayed block. It passed in attempt 004; real hardware and local checks are recorded above.
Mocked checks alone do not establish this result.

A read-only authenticated inventory query on 2026-10-06 found zero pods. The
initial urllib request returned HTTP 403; supplying a User-Agent resolved it.
No rental or remote training occurred. The missing local native extension was
rebuilt from this checkout for focused tests; no native source changed.

Bundle destinations share one validator before transfer and before reading;
canonical paths and unique manifest entries prevent aliases or duplicate writes.
Whole-bundle verification visits each entry directly instead of repeatedly
searching the manifest. Producer TrainingRun and artifact bytes remain unchanged.

Artifact admission verifies bytes once, then matches TrainingRun artifact sizes
and digests to the verified manifest. VerifyStore reconstructs run and stage rows
through its existing reader with a read-only connection; reading only the run
row incorrectly omitted stages and rejected real returned evidence. SCP upload
and download share command construction. No remaining deletion targets arose.

### Headless acceptance at gate

Commands available for gate:

```bash
uv run --extra dev --extra notebook pytest tests/remote tests/training tests/sim/test_net_opponent.py
uv run --extra dev ruff check manabot/remote manabot/training tests/remote
```

The notebook extra avoids the known optional-dependency failure. Existing tests
cover declared thread clamping, cost/reserve admission, CUDA rejection and
continuation, bundle corruption/path admission, credential isolation, ambiguous
creates, bootstrap interruption, rate mismatch and deletion failure. They do
not yet exercise a complete mocked successful deploy or training/transfer timeout
and failure paths. Gate retains those lifecycle checks and CPU regression checks;
the earlier broad coverage list was a requirement, not completed evidence.

A live acceptance helper under `tests/remote/` is explicitly invoked, never
rented by ordinary pytest discovery. Its one command consumes an existing tiny
selected-match self-play regime and the example mix. Across all attempts the
live proof has a **total cap below &#36;5**, with at most one pod active. First use
a short-deadline rental to prove pod-side deletion while the laptop observes but
does not trigger it; then deploy the small training regime with both guards.
Count that guard probe and failures in the same cap. Do not launch the second
attempt until the first is confirmed absent.

Required evidence: actual CUDA parameters and optimizer work, raw and EMA exports,
TrainingRun/SQLite and all declared artifacts returned with hashes, and one
four-leg paired-deal arena block on the laptop through the ordinary checkpoint
player (both seats/deck assignments), all terminal and exact-replayed without
failures/truncation. Reuse `play_cell`, registrations and selected-match identity;
no custom gameplay proof loop. Local arena cost is reported separately. A loader
call alone is insufficient. No synthetic weight fixture substitutes for these
trained bytes. Complete the final provider inventory check; it must show no owned
pod, and if the account began empty, no pods at all. Unrelated rentals are only
reported, never removed.

The implementation inventory observation above is dated, not a claim about
present rentals. Docs must record the live proof's dated inventory and
actual/estimated cost distinction. If auth, availability, scoped
self-deletion or compatible local native runtime prevents the proof, retain the
precise failure and leave live acceptance open.

The bounded live gate passed in attempt 004. Earlier cleanup-cost and inventory gaps were
repaired in `4348b5a0`; `eab86deb` then corrected complete-record admission and
simplified transfer. The focused regressions cover retained/observed rates,
missing evidence, duplicate rentals, changed plans, repeated cleanup, and
initial/final inventory combinations without deleting unrelated pods. These
resolved those two implementation gaps; live proof subsequently passed. Complete
mocked deployment and training/transfer failure/timeout coverage remain open.

The selected Intelligence scope has no child MEMORY.md files; its metrics
subdirectory retains historical evidence contracts. Current chapter limits and
ETU-108/larger-model ownership remain unchanged. The requested bounded proofs are complete; no framework reuse API is authorized.
Review/landing remain prohibited in this execution. Preserve ignored run evidence.

Historical focused check: `uv run --extra dev pytest tests/remote tests/training/test_regimes.py -q` — 50 passed, one CUDA-host skip. Later checks and real-hardware results are recorded above and in the remote contract.

## Explicitly not in this Task

Deeper/wider architecture, observation capacity, mixed precision, wide batched
collection, performance mapping, a week-long strength run, CPU offload,
multi-machine learners, cloud process resume and automatic scientific promotion.
ETU-108 owns distributed-RL research. No ETU-91/106 frozen evidence changes.

## Proposed follow-up milestones (not accepted)

1. Shakedown — supplied evidence: &#36;0.29.
2. Performance map for the model ladder up to Ataraxos size: proposed &#36;20–40.
3. First strength result: an Ataraxos-sized policy improving on the width-64
   monitoring plateau (54%, 58%, 58% at about 3, 7, 10 laptop hours; one seed,
   100 monitoring games each). Proposed bars of 70% versus scripted greedy and
   60% head-to-head need a separately frozen protocol and allocation.
