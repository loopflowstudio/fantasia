# Assumptions

2026-10-07: Immediate per-session revocation and portable CUDA recovery are not
available in the current S3-only worker/provider path. Per Jack Heart's explicit
clarification, bounded allocations remain executable; long renewal/replacement
and in-place extensions fail admission. Cancellation does not revoke a copied
STS token; its artifact permissions expire at the allocation deadline.

2026-10-07: A collection stopped at the allocation cutoff discards its unfinished
batch. Raw/EMA exports represent the last completed optimizer update. Existing
CPU recovery snapshots retain the last complete boundary, with all spent time
charged; incomplete work is never represented as completed target steps.
