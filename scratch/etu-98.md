# ETU-98 — bounded training recovery (2026-10-04)

Jack Heart authorized implementation and lf delivery; ETU-91's running checkout
and frozen protocols remain untouched. No costly scoring or paid compute.

Demo: interrupt a small real self-play regime after a durable update, resume in
a fresh attempt directory, and compare final model/Adam/EMA and collector state
with uninterrupted execution at identical iteration schedule coordinates.

The executor currently exports Adam but loses native environments and RNGs.
Native vector environments expose no durable snapshot. This slice records a
bounded native action replay journal, verifies reconstructed observation buffers,
and snapshots learner, Adam, EMA, all RNGs, collector statistics and schedule at
complete update boundaries. Source/runtime/recipe/seed mismatches reject recovery.
A journal ceiling bounds storage and restore time; this is not a scalable native
snapshot claim. Recovery initially admits a single CPU self-play stage only.
Unsupported mixed/supervised regimes fail admission rather than partially resume.

VerifyStore remains authoritative. Immutable snapshot artifacts are committed
before use; a new linked attempt preserves the failed parent and charges all
prior execution plus reconstruction against the original watchdog allowance.
Only the latest committed boundary can recover; no seed substitution or best-model
selection. Existing elapsed-budget schedules remain unchanged; opt-in iteration
schedules separate scientific coordinates from runtime variation and permit exact
same-runtime CPU tensor equivalence (not byte-identical checkpoint containers).

Focused tests cover real games, optimizer/EMA equivalence, failure after snapshot,
corruption, incompatible identity, exhausted budget and immutable failed evidence.
Measurements distinguish microsteps, learner rows, complete games, exposures,
collection/update/export/reconstruction and end-to-end cost. Remaining scientific
acceptance includes CPU/MPS full-loop comparison, multi-seed timing variability,
clone/world-sampling measurements and calibrated complete-cohort projections.
No inference-only rate can satisfy those requirements. Retain 168-hour campaign cap.

No existing path is slated for deletion. Add recovery to the existing executor.
Check result: six focused recovery tests passed (16.95 seconds), including real subprocess os._exit, exact resumed model/Adam equivalence and live-writer rejection. Root continued after the worker hit its account usage limit. Local POSIX leases survive as files but release on process death; recovery retains old run.json, settles the canonical parent with explicitly estimated unobserved time, and rejects foreign-host or backwards-clock accounting. Before delivery, finish typing/formatting, integrate latest main, test existing execution behavior and document measured scope. Scientific throughput and broader multi-stage recovery remain open.
