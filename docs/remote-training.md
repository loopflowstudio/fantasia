# Remote training on RunPod

`manabot remote` compiles an existing self-play TrainingRegime onto a declared
single-GPU rental. TrainingRun and VerifyStore still own training; deployment
owns provisioning, deadlines, transport and deletion. This first capability is
float32 ordinary PPO/Ataraxos self-play, including raw/EMA and live continuation.
Compound, supervised, belief/search, external opponents and process recovery are
rejected before rental. No distributed-learning or strength claim follows.

**Implementation status, 2026-10-06:** local compilation, relocation and failure
checks pass. CUDA execution and the paid end-to-end proof remain live gate work.
The authenticated provider inventory reported **zero rented pods** on this date.
No pod was created during implementation. The example image is pinned to the
Docker Hub manifest digest resolved on this date from RunPod's PyTorch 2.8.0 /
CUDA 12.8.1 Ubuntu 22.04 image; the locked project supplies its own Python/Torch.

## Compile and deploy

Commit source first. Compilation reads source identity but makes no provider
request. Deployment additionally checks that the exact commit/tree are publicly
fetchable from this repository before renting. Publish through the normal
Loopflow delivery step before the live gate.

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
runpodctl configuration, never the laptop account key. That credential's live
self-delete capability remains unproven until the gate runs.

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
recipe with EMA enabled, then invoke it after publication:

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

It charges all retained attempts under `.runs/remote-acceptance` to one $4.90
allocation and refuses unresolved prior cost/deletion. Success requires CUDA
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
