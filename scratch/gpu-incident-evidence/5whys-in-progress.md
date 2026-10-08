# CUDA capacity failure: etu103-four-hour-10351-0

Investigation requested by Jack Heart, 2026-10-07. Frozen source:
`68e0fbe9265a689891615274123587d653b5e66b`. This analysis changes no source,
recipe, controller, model, historical evidence or admission decision. No paid
training was restarted. Proposed repairs below have **not** been applied.

## Outcome and recovery status

The small width64/depth2, scalar value-token, float32 CUDA self-play run failed
before its four-active-hour endpoint. The verified final TrainingRun contains
**17,283 completed updates**, 8,848,896 learner transitions, 2,212,226 optimizer
exposures and 105,751 completed training games. The next batch failed the saved
behavior-distribution check before any optimizer step in that iteration.
The remote status reports 16,694 updates; that is a stale projection, not the
final evidence count. The latest saved policy is the two-hour checkpoint at
update 12,646, not the failure-time policy.

The last successful update records 9,884.381148 active seconds (2.74566 hours)
and 11,316.182494 total training-process seconds. The failed stage's final
collection-plus-learning sum is 11,316.134474 seconds; **do not use that sum as
active training**. Its failure handler absorbed previously unaccounted overhead
into learning time, discussed below. The four-hour endpoint was not reached by
either clock. No final-deal or random diagnostic cohort appears in the manifest.

Remote phase is `failed`, learner exit is 1, final generation 63 has
`artifacts_complete=true`, and the supplied final inventory reports zero pods.
Cleanup is recorded at estimated **$3.63056534815828** for this job, not an
invoice. With the retained shared prior $0.6518216411512489, the observed total
is $4.282386989309529 before other reserved/unmeasured costs. Cleanup cost uses
client confirmation time, so it does not establish the exact physical deletion
time. Neither a smaller actual bill nor a retry allowance is inferred.

Jack Heart's capacity comparison remains incomplete: one failed small-model
attempt, no completed six-run cohort, no capacity winner or promoted baseline.
CUDA process recovery was disabled and remains unsupported. Monitoring weights
cannot restore optimizer, EMA, collector, engine/sampling RNGs or iteration state.

## Evidence inspected

The final manifest is pinned at:

`s3://etudefantasia/manabot/jobs/etu103-four-hour-10351-0/runtime/artifacts/sha256/7d328497646645ef331da8727ea12fe7503c6041fcf4fb2beefd915d61ac23bb`

Version `VizKAtHTXvox_d42Cn5iqnnbp4Ic9acs`, 265,797 bytes. Its local bytes match
that SHA-256. Selected referenced files were downloaded read-only and checked by
the existing `S3ArtifactStore.fetch` size/digest admission. This investigation
did not bulk-download or independently replay every trace.

Retained local investigation directory: `.runs/etu103-failure-investigation/`.
It contains original supplied status/manifest/log/inventory copies, verified
`evidence/`, the reproducible bounded `probe.py`, `probe-result.json`,
`monitor-summary.json`, `run-summary.json`, `controller-exit-evidence.json` and
`focused-tests.log`. Preserve it with the original campaign directory
`.runs/etu103-four-hour-20261007/`; these ignored files are not in Git.

Key content bindings:

| Artifact | SHA-256 |
| --- | --- |
| Final run JSON, 341,671,825 bytes | `e0a543e2a4dceff3c1d3bdfcfd6faa79fe1bb27ac1571adf0c12385b87555d4d` |
| Training error log | `2c0bf989ca7825404ba57349c0dfc5554c90bf3d298616950c3a8b95b25b9d4b` |
| Initial raw policy | `825c24c4f74f9f8c7c240136befc69abb239314e88b47c6c8b355707b8f990ca` |
| One-hour raw policy | `3ff20a3a0fa78c13ad45ab9b0ce1511dea6caf48a6c2aeafded558acadaf8690` |
| Two-hour raw policy | `86c4269978febd800db59c11df83d1b67b7c4da19532daa8b0115a43360b5196` |

The final JSON is exported from the same snapshot's SQLite backup by
`manabot/remote/snapshots.py:snapshot_evidence`; VerifyStore owns the run.
Remote runtime identifies Torch `2.10.0+cu128`, L4 with 23,034 MiB reported
memory, driver 595.91.07, native Linux cp312 extension digest
`01c78078aef84c49e118cd501e912d95ba092757b6f855040d4a215bb7e8c87b`.
The recipe requested float32, 64 streams × 8 transitions, current-self,
one learner thread. Local probes used CPU Torch 2.10.0 and ordinary checkpoint
world/architecture admission, not the remote CUDA/native runtime.

## Chain A: the learner stopped on its numerical/support contract

1. **Why did training stop?** The verified traceback reaches
   `execution.py:1070 -> objectives.py:51 -> ataraxos.py:237`, then raises at
   `_check_distribution` line 44. `training-exit.txt` confirms exit 1.
   `update_move_iteration` checks the entire saved `[T,E,A]` behavior tensor
   before filtering or any optimizer work. Thus one bad, even unselected, row
   stops this iteration. Target calculation precedes that check; the trace does
   not implicate the target calculation or current-minibatch gradients.

2. **Which invariant failed?** The exact predicate is **not recoverable from
   the retained batch evidence**, because that batch was not saved. Shape mismatch
   and empty legal support have different errors and can be excluded for this
   trace. Line 44 combines four remaining predicates:
   nonfinite probabilities; nonpositive mass on a legal action; nonzero mass on
   an illegal action; or row sums outside `allclose(atol=1e-5, rtol=1e-5)`.
   The error wording alone cannot distinguish them.

3. **What makes legal zero probability plausible?** Collection constructs
   `Categorical(logits=logits)`, samples its float32 probabilities, and stores
   those probabilities and the selected log probability in copied NumPy rows
   (`sim/net_opponent.py:322–355`, `417–467`). The learner requires every legal
   probability to be strictly positive, then reconstructs full behavior logs
   with `.log()` for reverse KL (`training/ataraxos.py:28–44`, `87–104`).
   Finite softmax logits are mathematically full-support, but their exponentiated
   float32 representation need not be. There is no enforced legal-logit range
   or shared numerical support policy between collector and learner.

   The local synthetic reproduction passes finite logits `[0,-100,-1e8]` but
   fails `[0,-104,-1e8]`, with the first two actions legal. The failing row is
   exactly `[1,0,0]`: finite, normalized, and zero on padding; only positive legal
   support fails. Its legal normalized log probabilities remain finite.
   This establishes a real reachable implementation failure, **not** that these
   were the remote failing logits. Thresholds depend on dtype/kernel/denormal
   handling; 104 is the observed CPU example, not a claimed CUDA threshold.

4. **Does the trained model approach that boundary?** On the same 256 retained
   real calibration observations, ordinary reloaded initial/one-hour/two-hour
   checkpoints have maximum within-row legal-logit gaps 0.00448 / 54.80448 /
   73.37687 and minimum legal probabilities 0.07686 / 7.90e-25 / 6.79e-33.
   All are finite, normalized within 1.20e-7 and have no legal zeros. A separate
   bounded CPU current-self collection with the two-hour checkpoint, four
   streams, seed 10351, collected 4,096 learner rows in 21.74 seconds; all checks
   passed, minimum legal probability 6.38e-37. It used no optimizer and did not
   reproduce the remote batch. These measurements support increasing numerical
   concentration, while the passing probes explicitly limit the conclusion.

5. **Why can the contract mismatch persist until late?** Collection only needs
   a valid categorical distribution with nonnegative support; it can sample
   a row whose unlikely legal alternatives have rounded to zero. The subsequent
   reverse-KL implementation needs finite logs for all legal behavior actions.
   A failing support check protects that calculation; removing the check alone
   would introduce infinities/undefined products instead of fixing the contract.
   Ataraxos regularization and gradient clipping do not impose a positive
   representable lower bound. The saved iteration schedule reduced tau to
   0.00267722 by update 17,283, but no experiment here establishes that tau decay
   caused the concentration or the failure.

The strongest supported learner explanation is **a collector/learner numerical
support-contract mismatch, with underflow the leading but unconfirmed trigger**.
The missing tensor prevents a definitive causal assignment for this incident.

### Competing explanations and negative evidence

| Explanation | Evidence and remaining limit |
| --- | --- |
| Nonfinite policy/probabilities | All retained loss, value loss, entropy, gradient norm, KL and advantage summaries are finite. Collection's Categorical/multinomial path normally rejects NaN/invalid weights earlier. The last retained gradient norm is 2.83 before clipping; the observed maximum is 63.78. These summaries cover previous selected minibatches, not the failed batch, so a new nonfinite event is not ruled out. |
| Legality/order/buffer mismatch | Collector copies observations and probabilities before advancing the native environment, assembles both from the same `_Pending`, and empties streams at each update boundary. Agent masking uses `actions_valid == 0`; learner uses `> 0`. Existing paired collection tests and the bounded real probe pass. A malformed mask or rare alignment defect cannot be excluded without the failed row and exact observation. |
| Normalization drift/precision | Preserved checkpoints' CPU distributions differ from unit sum by at most 1.20e-7, well inside the check. Remote precision is float32, not an admitted mixed-precision recipe. Extreme logits/cancellation or CUDA-specific behavior remain unmeasured. |
| Changed learner weights corrupt behavior | Collection stores detached copied behavior probabilities; the trace fails before this iteration's optimizer loop. No asynchronous actor/learner is configured. Recomputed current policy is not used as the saved behavior. |
| Chosen-action likelihood inconsistency | A separate later check has a different error. This run did not reach it on the failing batch. |
| OOM, watchdog, credentials, engine illegal action | The retained terminal cause is a Python ValueError, not these failures. Final uploads succeeded. The stage stopped at about 3.14 total hours, below its five-hour watchdog. No causal evidence supports these alternatives. |

## Why shorter validation did not expose this

The hardware complete-loop cells use three fresh updates (one warmup, two timed),
not a sustained training trajectory (`experiments/runners/cuda_performance.py:255`).
The Ataraxos integration fixture uses two tiny 16-transition stages. Analytic
gradient tests use moderate positive float64 distributions; rejection tests
inject zero/negative/NaN distributions directly. They verify rejection but do
not bridge finite trained logits → rounded behavior → the learner's stronger
support requirement. The initial 100-game admission tests rollout/evaluation
publication before learning, not the late optimizer regime.

Existing focused tests still pass: `uv run --no-sync pytest
tests/training/test_ataraxos_gradients.py tests/sim/test_net_opponent.py -q`
reported **26 passed**. That is evidence of a missing boundary case, not proof
that all collectors or all training implementations are correct. A longer smoke
alone is an expensive probabilistic detector; deterministic extreme-logit tests
and saved mature-checkpoint collection directly exercise the suspected boundary.

## Chain B: the serial controller and live report stopped independently

1. The local `controller.log` ends at 2026-10-07 **18:21:09 UTC**, update 803,
   generation 16, phase running. The final learner failure was recorded at
   **21:10:41 UTC**. The remote job continued for nearly three hours after the
   local controller's last log. The learner failure did not cause that earlier
   local stoppage.

2. The launch transcript records the controller as a foreground
   `tools.exec_command` command at 17:58:32 UTC, unified execution session 42610.
   It was not launched under a persistent service. At **18:21:17.520 UTC**, the
   transcript's `item_completed` records that exact command as `failed`, exit
   code **−1**, with no stdout/stderr; the agent turn completed at
   18:21:17.488 UTC. This is strong evidence of command-session lifetime ending
   with the turn. The record does **not** identify the OS signal, sender or
   implementation of process teardown; those details remain unknown.

   Exact source: local transcript
   `/Users/jack/.codex/sessions/2026/10/07/rollout-2026-10-07T10-24-28-01a11765-26c7-7032-aa33-0cf1768f6218.jsonl`.
   The compact timestamp/exit extract and transcript digest are retained in
   `controller-exit-evidence.json`; no credential values were extracted.

3. Ownership was split: ETU-123's remote supervisor owns **one accepted job**,
   its evaluation queue, S3 generations and shutdown. The six-run sequence and
   report/W&B projection live in this local controller. The disconnect proof
   showed the remote learner survives submitter exit; it did not prove the
   local sequence survives the conversation or laptop. A lock file prevents
   duplicate controllers but does not supervise or restart one.

4. `project()` launches the report child with a 120-second timeout and catches
   report failures. The last report log completes and the controller kept
   emitting status afterward. There is no retained evidence that rendering or
   W&B killed it. Once the parent disappeared, no new generation was fetched
   or projected: the saved local `latest.json` still points at generation 10,
   while remote S3 reached 63 and finished three evaluations. Independent manual
   observations fetched generation 15 but were not an ongoing controller.

5. Even a surviving controller would correctly refuse the next rental after
   this failed attempt: after cleanup it requires phase completed, complete
   artifacts, a completed TrainingRun, ≥14,400 active seconds and six completed
   evaluation cohorts. That deliberate stop is separate from the premature
   lifetime failure. Restarting the frozen controller should not be presented
   as permission to skip or replace this failed seed.

No new submit intent for a later job was found in the retained campaign directory.
The empty provider inventory and first-job failure are consistent with that.
This investigation does not infer unrecorded remote creation from local absence.

## Chain C: evidence survived, but projections and accounting mislead

**Stale terminal progress.** `supervisor.py` reads updates before synchronous
snapshot publication, then polls the learner. On nonzero exit it breaks without
rereading the final TrainingRun; only its success branch refreshes final counts.
Final snapshot generation 63 exports 17,283 updates, but `RemoteJobRecord`
retains 16,694 (589 behind). Large snapshot work can widen the gap: final run JSON
is 342 MB, SQLite is 216 MB, evaluator job JSON files retain 132/271 MB snapshots,
and the training dashboard is 38.5 MB. These sizes and code order explain how
staleness is possible; they do not measure exact upload latency or prove the
learner failed because of I/O. Final heartbeat is 21:20:07 UTC.

**Failure-time active-cost inflation.** Successful updates measure collection
and learning locally; persistence runs afterward and `diagnostic_seconds` remains
zero on this path. On exception, `execution.py:1307–1316` takes total stage time
minus accumulated phase times and adds the entire residual to `phase`, which was
`learning_seconds`. That includes earlier initialization wait/persistence/other
unaccounted overhead, not just the failed learner call. The final phase sum
exceeds the last successful active coordinate by **1,431.753326 seconds** even
though total wall time advanced only about 0.46 seconds after that coordinate.
Keep the frozen receipt unchanged; analysis must label that sum invalid for
active-budget attainment and retain the last committed coordinate separately.
The collected failing batch may also exceed the last successful transition
counters, which update only after successful learning.

**Evidence sufficiency.** Final artifacts suffice to establish the exception,
completed work, earlier policy bytes, monitoring and cleanup status. They do
not suffice to recover the exact failing predicate or replay training at failure.
There is no failed-batch tensor, legal logits/log probabilities, failure-time
model, optimizer/EMA/RNG/collector snapshot, or full training trajectory journal.
`recovery_artifact` is null; snapshot publication only includes already committed
artifacts and selected logs. `artifacts_complete` means that manifest's retained
files were published, not that training completed or all debugging state exists.
The publisher also omits `supervisor.log`; pod deletion command output/return
code is suppressed, so exact deletion timing versus deadline cleanup is unresolved.

## Retained monitoring, with its limits

The verified monitor JSONs report 300 terminated, exactly replayed games and zero
failures. This analysis inspected their recorded replay results; it did not rerun
the traces. Each milestone repeats 25 development deals × four seat/deck legs.
Saved 95% intervals resample deal blocks and condition on a single checkpoint.

| Milestone | Update | Active seconds | Greedy wins / 100 | Saved score interval | Allies / 50 | Lessons / 50 |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| Initial | 0 | 0 | 30 | [24, 36]% | 30 | 0 |
| One hour | 6,083 | 3,600.009 | 61 | [54, 69]% | 46 | 15 |
| Two hours | 12,646 | 7,200.292 | 63 | [57, 69]% | 49 | 14 |

These are incomplete single-seed exploratory monitoring observations. The large
Allies/Lessons difference is visible; it establishes neither its mechanism nor
general strength. The scientific final deals remain unused in the retained
manifest. No endpoint result, capacity comparison, seed uncertainty or new
stopping rule is substituted for the missing cohort.

## Proportionate prevention and how to validate it

All items are proposals, not applied fixes or new scientific authorization.

1. **Make the failure diagnosable first.** Separate the four distribution
   predicates and save a bounded private incident artifact before raising:
   update/row/action IDs, exact mask/probabilities/normalized collection logs,
   dtype/device, row sums, min legal/max illegal mass, nonfinite counts, and a
   small viewer-safe observation slice. Bind source/model/recipe and hashes.
   Capture model/optimizer/RNG state only with an explicit bounded storage
   contract; never dump locals/environment variables. Fault-inject each predicate
   and verify that final S3 publication retains the distinct diagnostic after
   learner exit. Preserve the original failure if diagnostic export fails.

2. **Unify finite-precision behavior semantics.** Prefer a reviewed contract
   storing normalized collection log probabilities and using log-space ratios
   and KL terms, with explicit masks and checks against the actual sampling
   path. Test extreme finite legal logits, legal permutations, padded actions,
   selected likelihoods, finite losses/gradients and ordinary-probability parity
   on CPU and CUDA. Do not silently replace behavior zeros with epsilon only
   in the learner or merely relax the check. A probability floor/mixture applied
   consistently during both sampling and learning is an alternative, but changes
   the policy/recipe and needs a new freeze. Float64 alone moves the boundary;
   it is not a general finite-logit solution. Stable logs repair the demonstrated
   representational defect, but cannot be claimed to fix the original run's
   unknown predicate until targeted evidence supports that attribution.

3. **Give the cohort a durable owner.** Persist sequencing/reporting with a
   managed controller that survives conversation and laptop exit; distinguish
   its lease/heartbeat from each remote learner's. Use existing job IDs and
   creation fences on reconnect, retaining no-replacement and failed-cohort
   boundaries. A local detached process alone still depends on the laptop.
   Test session termination with two fake jobs, replay the same durable state,
   prove exactly-once admission and failure halt, and independently catch up
   report projections from pinned S3 generations without restarting learning.

4. **Refresh terminal projections from final evidence.** On every terminal path,
   read counts/status from the final snapshot/VerifyStore cut and bind the status
   record to that cut. Test a learner that advances and fails during a deliberately
   slow upload. The final record must agree with the manifest's run even when
   the earlier heartbeat is stale. Separately profile snapshot size/work before
   prescribing a new storage architecture; incremental monitoring receipts may
   be enough. Report age/source generation explicitly.

5. **Keep phase accounting honest on exceptions.** Charge only the interrupted
   operation's measured elapsed time to that operation. Account for initialization
   waits and persistence separately throughout execution. Test an injected learner
   failure after a long fake initialization wait and slow persistence: neither
   delay may increase active collection/learning. Preserve failed-batch attempted
   work separately from committed updates/exposures and leave frozen receipts as-is.

6. **Retain cleanup evidence cheaply.** Record redacted deletion attempt time,
   return status and final remote supervisory diagnostics before teardown where
   possible; retain the independent absolute guardian deadline. A cleanup proof
   must distinguish provider-confirmed absence, command success and inferred time.
   No extra rental is needed to unit-test these records.

## Remaining questions and concrete next action

The original failing tensor and last 4,637 updates' model states are absent;
there is no honest exact replay of update 17,284 from the retained two-hour
weights. CUDA's actual failing predicate, logit gap and denormal behavior remain
unknown. Prior diagnostic means cannot answer those questions. The command
session exit record strongly locates the controller lifetime failure, but does
not identify the OS signal. Cleanup is confirmed absent, with exact provider
deletion time unmeasured.

Next recovery action: deliver the bounded distribution diagnostics/numerical
contract, terminal-status and clock repairs through ordinary software review,
with deterministic local tests and an admitted CUDA check when separately
scheduled. Recover reports read-only from generation 63 and label this attempt
failed; do not run the frozen sequence as a substitute for a repair. Preserve
the $3.63056534815828 estimate in the cumulative ledger. Before any scientific
restart, the operator must explicitly decide the new source/cohort and remaining
budget after accounting for this attempt. A fresh seed-10351 run would be a new
attempt, never continuation of this CUDA process. The requested investigation
ends here; it neither launches paid work nor treats proposed remedies as approved
scientific amendments.

Validation result: verified selected generation-63 artifacts; CPU numerical and
4,096-row saved-policy probes retained; 26 existing focused tests passed. Frozen
HEAD/controller/recipe unchanged. Analysis alone has not repaired the system.
