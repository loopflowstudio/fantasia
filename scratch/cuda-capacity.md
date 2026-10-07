# ETU-103 four-hour continuation

Jack Heart's latest direction supersedes the 12-hour total comparison: six
independent runs, four active collection/update hours each, plus overhead.
No scientific cohort has launched. Historical mini and GPU bundles stay intact.
The detailed revised protocol, cost projection and credential decision are in
experiments/model-capacity.md. Old scratch survives at 0145f77f; it is historical.

PR253 integrates PR254 (ab721cab) and is armed with --next four-hour-capacity.
Its macOS history fixture failed without row details, then passed at exact source
after this checkout's stale native extension was rebuilt. The behavior fixture now
uses the standard 120-second arena allowance and reports row details; all semantic
assertions remain. Its focused test passed. CI is rerunning; no cause is claimed
proven. PR254's owner handled delivery and its checkout was not edited.

Prepared code: TrainSelfPlay.active_seconds stops at complete update boundaries;
collection/learning count, export/setup do not. Ataraxos schedules are unchanged.
The update safety ceiling fails early runs. Monitoring carries an explicit active
time coordinate, suppresses a duplicate final hourly export, and declaratively
selects untouched terminal greedy plus separate random cohorts. The existing
capacity runner exports six ordinary deployment inputs; it does not rent.

Fresh L4/A40 quote $0.49/hour, zero pods, at Unix 1791343703.70. Six seven-hour
rentals plus prior $0.5359766177, shared ETU-123 $3, guardian $0.60 and storage $1
reserves project $26.5559766177. Historical four-game timings project 974–1133 s
per 100 games; 1800 s is provisional, requiring remote admission. No rental yet.

Concrete launch blocker: default AWS credentials are SSO; worker role max is
already 12h, but role chaining is 1h. No AWS keys in Doppler etude/prd; no account
OIDC or us-west-2 Roles Anywhere trust anchor. Repository operator must decide
whether to create a dedicated IAM issuer (assume-worker-role only, key in Doppler,
never on pod) or establish Roles Anywhere certificate trust. No IAM changes made.
Dedicated issuer-profile support is now implemented and tested, with unchanged
job-prefix restriction, returned-expiry checks, chaining rejection and redacted
credential-provider errors. The profile/account identity is still unavailable.
After that decision: admit remote evaluation/live W&B+report path, freeze source,
and submit the six jobs through manabot deploy. CUDA process resume is unavailable.

Check: 63 affected training/credential checks passed after rebuilding native; four credential checks pass after redaction coverage. The inherited real-process disconnect test timed out under combined load, then passed alone in 7.63 s; no lifecycle guarantee is strengthened from that retry.
