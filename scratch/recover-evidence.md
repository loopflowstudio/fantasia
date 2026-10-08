# ETU-126 reconnect evidence

Initial PR258 is published with auto-merge requested and recover-evidence as its
next serial PR. The native launchd proof remains under .runs/etu126-launchd-proof-2.
Incident source copies are retained in .runs/etu126-incident-evidence and c508b7f1;
Loopflow staged/cleared scratch during delivery. This agent is not a scheduler.

Read-only review found fetch_job creates a generation directory with exist_ok=False,
so an interrupted fetch cannot retry; logs calls full fetch_job for every new
observed generation. Follow-up reuses verified completed files, installs new files
atomically, rejects conflicting bytes and fetches only log+manifest for logs/attach.
Final-manifest admission shares the same job_manifest reader.

ETU-127's active scratch contract registers failure snapshots in rejected_artifacts.
The existing retained_artifacts owner already includes those; add a snapshot-path
regression without touching learner code. All original source/evidence remains.

Next: focused/affected checks, second coherent delivery after PR258 merges. Automatic
client-offline report/W&B projection remains separate; live recovery still requires
ETU-127's delivered fix, selected online host/credentials, new source/protocol and
inclusive remaining-$30 admission. No Mini or GPU work started.

Validation: isolated remote suite had 122 passing checks, 2 skips and one fixture
failure (inherited placeholder raw artifact outside bundle). Clearing that unused
fixture artifact fixed it; both snapshot tests then passed. Five focused retrieval
checks passed; no production source changed after the isolated run. Current total
is 123 passed / 2 skipped across the affected remote suite. PR258 CI has passed
Rust/debug and initial gates; integration jobs are still running. Repository-wide
lf pr reconcile also reports stale missing checkouts for unrelated historical PRs;
PR258 itself remains open, so no merge is claimed.


PR258 merged at a71acbe9 with its complete CI matrix passing; Loopflow rotated
this checkout to PR2 and retained the local retrieval follow-up as b0bba5d1.
The ETU-127 numerical fix is published as PR259 but is not yet merged/CUDA-validated.

Expanded this coherent evidence-delivery slice with an optional independent
report service. It reads only existing Dashboard exports, saves JSON/HTML first,
and projects W&B with retained errors and acknowledged-prefix retry. A persisted
report-process budget and child-owned absolute deadline bound network work;
scheduling has no telemetry dependency. Host ownership now uses stable OS machine
identity, avoiding duplicate-hostname collisions. Settled services exit; unresolved
observations stop at the declared 30-minute cleanup/report grace.

Next: run affected gate including the changed native launchd owner path, update
PR2 copy around evidence/reports, publish/land. Then coordinate ETU-103 only after
PR259 merges; live restart still needs a selected always-on credentialed host and
new frozen attempt/budget admission. No scientific target or allocation changed.

Current gate: 152 checks passed and one expected skip in the isolated remote +
Experiment run, including native launchd restart. A projection budget test's broad
Popen mock also intercepted the new macOS machine-ID read; the fixture now pins
that unrelated host identity, and all three projection checks pass. Thus the
current affected result is 153 passed / 1 skip, with no production change after
the gate. Ruff and diff whitespace checks passed.

The generated local Work seed is reported above its 16k goal budget while this
large PR patch is embedded; memory/scratch remain within limits. No authoritative
Task directive was dropped and no budget was raised. The code and supplied Task
brief were read in full. Runtime-generated goal composition has no authored local
file to trim safely here.
