# Remote training on RunPod

`manabot remote` compiles an existing self-play TrainingRegime onto a declared
single-GPU rental. TrainingRun and VerifyStore still own training; deployment
owns provisioning, deadlines, transport and deletion. This first capability is
float32 ordinary PPO/Ataraxos self-play, including raw/EMA and live continuation.
Compound, supervised, belief/search, external opponents and process recovery are
rejected before rental. No distributed-learning or strength claim follows.

**Live status, 2026-10-06:** the complete 350-update-per-stage proof passed:
CUDA self-play, raw/EMA return and reload, four terminal exact-replayed arena
games, and confirmed empty inventory. A separately authorized 600-update-per-stage
run with wider deadlines is in progress. No PR review or landing was performed.

## Live attempts, 2026-10-06

Jack Heart authorized **$50 total across every Task attempt**, including the
previous $0.29 shakedown, and required tens of minutes of CUDA self-play before
review. Normal non-force pushes of this Task branch are authorized to make exact
source commits fetchable; opening/readying a PR, landing and completing review
remain prohibited. Each command retains its own smaller cost/deadline limits.

Evidence stays under `.runs/remote-acceptance`; failed directories are retained.
Dollar estimates use observed rental intervals and the declared storage allowance,
not a provider invoice. The prior shakedown's $0.29 is reported expenditure.

| Attempt | Source | Result | Estimated rental cost |
| --- | --- | --- | --- |
| 000 | `d8307606` | No create: unrelated zero-price GPU quotes rejected admission | $0.0000 |
| 001 | `46c80fd2` | Pending-pod port list rejected; exact owned probe manually deleted | $0.0193 |
| 002 | `5f1c34d6` | Guardian passed; bootstrap exceeded the eight-minute setup deadline; deleted | $0.0686 |
| 003 | `5f1c34d6` | Guardian and CUDA smoke passed; first stage interrupted; all 21 bundle files verified; deleted | $0.3260 |
| 004 | `62fc7e15` | 350 updates/stage completed; records/checkpoints returned; four replayed arena games; deleted | $0.3661 |
| 005 | `62fc7e15` | 600 updates/stage with wider watchdogs; in progress | pending |

Attempt 001 retains the original unresolved receipt plus explicit manual
reconciliation. An authenticated query observed the unique receipt-owned pod at
$0.49/hour, 6 vCPUs and 62 GB; the corrected client deleted that exact name and
confirmed empty inventory. Its cost conservatively ends at the later reconciliation
confirmation. Pending `ports=["22/tcp"]` declarations now mean no public mapping;
only published `portMappings` supplies an SSH endpoint. The regression covers both.

Attempt 002 demonstrated real pod-side deletion without laptop DELETE, then hit
its setup deadline during dependency installation. Attempt 003 preserves the same
1,200-update/two-stage recipe and 45-minute training allowance, increasing setup
to 20 minutes and the total command allowance to 75 minutes ($0.775 projected
ceiling). Setup completed in roughly ten minutes. Network-backed `/workspace`
and uv's cross-filesystem copy warning were observed; no isolated throughput
explanation is claimed.

The rented-hardware command `uv run --locked --extra dev pytest
tests/remote/test_device.py -q` passed **2 tests in 189.74 seconds**, including
actual CUDA optimizer work, continuation and raw/EMA CPU reload. It overlapped
main training and is functionality evidence, not a performance benchmark.
Its logs, exit status and fixture artifacts are retained inside the returned
bundle. Pytest's two convenience symlinks were recorded separately and removed
before bundling; all underlying artifact bytes remain intact.

The first main stage stopped after 567 updates / 290,304 optimizer exposures
in 1,354 recorded seconds. It is an interrupted run, not a completed deployment.
Attempt 004 reduced each stage to 350 updates without editing an active run.
It completed in **1,663.91 seconds (27.73 minutes)**: 2,213 self-play games,
369,748 native decisions, 179,200 learner transitions and 358,400 optimizer
exposures. Both stages used `cuda:0` and exported raw, EMA and Adam artifacts.
The selected raw checkpoint SHA-256 is
`d380bc42de41402411a608656d06a21762c9e794d0b65ee3e73a48f417d0ce1a`.
The original run/SQLite and all 12 declared bundle files verified. Four ordinary
arena games covered both seats/deck assignments and completed with exact replay
in 11.75 seconds. Final authenticated inventory was empty. Prior Task expenditure,
including the shakedown and all failures, is **$1.0701 estimated/reported**.

Jack Heart then requested an immediate longer run after confirmed deletion.
Attempt 005 restores 600 updates per stage, with one-hour stage watchdogs,
a two-hour run allowance and a 150-minute rental allowance ($1.55 projected
ceiling). The elapsed-budget schedule uses the larger denominator too; this is
a feasibility run, not a controlled timing-only or strength comparison.
ETU-119 owns the separate persistence fix; no such change enters these attempts.

Saved update coordinates provide wall intervals without changing training.
Attempt 003's median interval rose from 1.69 seconds over early updates to
2.24 seconds over updates 500–567. In attempt 004, stage-one medians over
successive blocks were 1.58, 1.64, 1.77 and 1.91 seconds; stage two was 1.78,
2.03, 3.10 and 2.36 seconds. Blocks use diagnostics [1,100), [100,200),
[200,300), [300,350), differencing adjacent cumulative coordinates.
These intervals include ordinary work and preceding persistence; they do not
isolate the save cost. On failure, the executor assigns unaccounted time to its
last active phase, so failed-run `learning_seconds` is not pure optimizer time.
Jack Heart's separately reported laptop persist timings identify a plausible
contributor, not a measured complete explanation of pod slowdown.

Local checks: **405 passed, 3 skipped** across remote, training and net-opponent
tests. These checks do not substitute for the live deployment. No strength,
scientific comparison or chapter acceptance follows.

## Compile and deploy

Commit source first. Compilation reads source identity but makes no provider
request. Deployment additionally checks that the exact commit/tree are publicly
fetchable from this repository before renting. Push the exact commit to the Task branch before the live gate. A source push
does not require opening or readying a PR for review.

```bash
uv run manabot remote compile --regime experiments/regimes/direct-self-play.json \
  --mix ops/mixes/runpod-small.json --seed 197 --out .runs/remote-plan.json

doppler run --project etude --config prd -- uv run manabot remote run \
  --plan .runs/remote-plan.json --out .runs/remote-example
```

The single-command form takes `--regime`, `--mix` and `--seed` in place of
`--plan`. It prints the complete plan before provisioning and saves it with the
private deployment receipt. There is no interactive prompt. Use a fresh output
directory for every attempt; never replace failed receipts.

The hardware mix declares GPU alternatives in priority order, one worker, vCPUs,
RAM, thread limit, image digest, disks, hourly ceiling, dollar cap, wall time and
setup/transfer/cleanup reserves. Threads resolve to the smallest of requested
threads, rental vCPUs, mix thread limit and the executor's four-thread maximum.
The pod's reported host CPU count is telemetry only. GPU allocation and returned
CPU/RAM/rate are admitted before bootstrap. The first implementation deliberately
caps each deployment below $5; the larger weekly allocation is not a scheduler.

Bootstrap uses uv 0.8.22, Rust 1.98.1, locked dependencies and Python 3.12. The
exact source tree binds bootstrap/guardian code. CUDA is passed to the model,
collector and optimizer owner; unavailable CUDA fails without CPU fallback.
Phase boundaries synchronize the GPU. CUDA receipts add actual device, memory,
capability and runtime; the returned toolchain record includes driver version.
CPU defaults and receipt fields retain their prior meaning.

## Deadlines and cleanup

Every command first rents a short guardian probe, then waits for pod-side deletion.
Training cannot start unless the probe disappears at its deadline without laptop
DELETE. Both rentals share the same command budget and absolute outer deadline;
there is never more than one active rental. The startup guardian is independent
of Python/bootstrap/SSH. It uses the image's provider-supplied pod-scoped
runpodctl configuration, never the laptop account key. That credential's self-delete capability was observed in the retained live probes.

The laptop bounds API/SSH operations and attempts deletion in `finally`, including
interruptions. Provider DELETE must be followed by confirmed absence. A failed
create is reconciled by its unique name; it is never retried speculatively.
Unobserved ambiguous creates stay unresolved even if a brief inventory is empty.
Provider-ordered GPU alternatives use one create request. Unrelated rentals are
never deleted.

```bash
doppler run --project etude --config prd -- uv run manabot remote status
doppler run --project etude --config prd -- uv run manabot remote cleanup \
  --deployment .runs/remote-example/deployment.json
```

`CLEANUP UNCONFIRMED` means possible continued billing, not success. Keep the
receipt and retry cleanup. Estimated cost includes observed rental time and the
declared storage allowance; it is not a provider invoice. Price admission is not
an atomic spending cap. Provider outage, a container that never starts, or laptop
loss before startup can defeat the two guards. No network volume is created.
The provider's [delete operation](https://docs.runpod.io/api-reference/pods/DELETE/pods/podId)
terminates the rental; stopping alone is insufficient because storage remains.

## Returned evidence

Evidence lives beneath the ignored, permission-restricted deployment directory.
The closed SQLite database, original run.json, optimizer files, raw/EMA policies,
toolchain record and training log return unchanged. `bundle.json` binds every
file's producer path, relative destination, size and SHA-256. `Bundle.resolve`
locates a verified local artifact without rewriting producer paths or costs.
Traversal, symlinks, missing files and changed bytes fail admission. TrainingRun
export and authoritative database must agree; only raw/EMA files enter the normal
policy loader. Optimizer files are verified opaque artifacts, not policies.

Incomplete transfers retain whatever arrived, then deletion proceeds. Training
errors retain their closed evidence when retrieval is still possible. Timeout
may prevent retrieval; partial evidence never becomes a completed training run.
Portable process recovery and transparent relocation for all historical report
consumers are not supported.

## Explicit live gate

The helper is not collected by pytest. Prepare a bounded version of the existing
recipe with EMA enabled, then invoke it after the source push:

```bash
uv run python - <<'PY'
import json
from pathlib import Path
recipe = json.loads(Path('experiments/regimes/direct-self-play.json').read_text())
for stage in recipe['stages']:
    stage['learning']['ema'] = 0.9
Path('.runs').mkdir(exist_ok=True)
Path('.runs/remote-proof-regime.json').write_text(json.dumps(recipe, indent=2))
PY
doppler run --project etude --config prd -- uv run python -m tests.remote.live_acceptance \
  --regime .runs/remote-proof-regime.json --mix ops/mixes/runpod-small.json
```

It conservatively limits retained deployments under `.runs/remote-acceptance` to
$4.90 and refuses unresolved prior cost/deletion. The Task totals above separately
include the earlier $0.29 shakedown; the authorized $50 total is not a spending
target. Success requires CUDA
optimizer exposures, raw/EMA reload, complete returned records, and one four-leg
paired-deal arena block through the existing evaluator: both decks/seats,
terminal completion and exact Command replay. Arena cost is separate from rental
cost. This proves the workflow, not strength or chapter acceptance. Do not delete
that directory between retries or infer live acceptance from local fixture tests.

Cleanup recovers estimates from retained or newly observed rental rates, the
original hash-bound plan's storage allowance and intent-to-confirmed-absence
elapsed time. Missing rates, unobserved creates, conflicting rental evidence or
missing/changed plans leave billing unresolved. Repeated cleanup preserves the
first confirmed deletion time; deletion alone never supplies a zero cost.
The helper records initial inventory and requires final inventory to be empty
when it started empty. Otherwise it requires no owned pods; unrelated rentals
are counted and never deleted. Its arena input uses checkpoint training coordinates.
Complete mocked deployment and training/transfer failure and timeout coverage
remain gate work alongside the paid proof.
