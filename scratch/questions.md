# ETU-123 assumptions and coordination

2026-10-06: Remote jobs use private versioned S3 for immutable intent, conditional
creation claims, supervisor status and artifact manifests. A create claim is never
reissued: an unobserved provider operation remains ambiguous even when inventory
is temporarily empty. No automatic process restart or lease stealing is admitted.
A fresh client observes/fetches by ID using the normal AWS/RunPod credentials.

The ETU-103 contribution request failed: `Task input belongs to a stale or different
Flow`. Read-only Task status confirms Jack Heart's shared $3 reservation direction,
but the shared spend ledger/reservation is not confirmed. No rental is permitted
until that coordination succeeds. PR253 is published and unmerged at e052ac30;
its active checkout is unchanged. Implementation uses landed APIs.
