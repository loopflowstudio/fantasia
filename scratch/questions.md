# ETU-123 implementation decisions

2026-10-06: Permanent S3 create claims fence uncertain provider operations. No
lease takeover or process restart is admitted. New IDs are never a retry mechanism.

Jack Heart confirmed PR253 shared API freeze and the $3 reservation within the
same $15 ETU-103 allocation. Its five prior rentals total $0.5359766177 and are
deleted. PR253 e052ac30 was integrated with `lf sync`; its checkout is unchanged.
Historical ETU-103 calibration assumptions remain at that commit. Scientific
capacity execution remains blocked on delivered integration, not launched here.

SSO cannot issue GetFederationToken. The explicitly configured manabot-remote-jobs
role trusts the current AWS principal and grants only job-control reads and
runtime evidence writes. Job-specific session policy narrows it further. SSO
role chaining admits less than one hour including reserves; longer jobs require
an appropriate non-chained credential source and still expire after their deadline.
No provider account key is forwarded. No other existing role was changed.

Remote execution begins from provider startup, so setup too survives the client.
Acceptance is observed after source setup and resource admission. Missing setup
heartbeats remain unavailable; the shell guardian owns the original deadline.
