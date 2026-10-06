# ETU-118 open implementation assumptions

- Jack Heart authorized the current laptop for the sustained allocation. ETU-116's
  mini sequencing remains unchanged. Compatible evidence will be shared; no second
  laptop study is inferred.
- Active runtime will mean occupied elapsed time while the machine is awake, not
  process CPU time. Evaluator overlap must also be retained as additive process
  occupancy; CPU seconds are separate. Known sleep and safe-pause downtime are
  excluded. Abrupt restart intervals that cannot be measured remain explicitly
  uncertain and conservatively charged, never relabeled measured active compute.
  Clock/reboot accounting and actual process interruption/recovery passed bounded checks; physical lid closure remains untested.
- Begin with manual checkpoint-safe pause only. No automatic statistical plateau
  rule: repeated strength estimates and lag/freshness evidence support Jack Heart's
  decision. An operational failure cannot silently restart a scientific seed.
- Immutable committed updates may not repeat. Work after the last committed
  recovery snapshot can repeat after interruption, with its prior cost retained.
  This is recovery semantics, not a promise of zero repeated machine instructions.

- Admission retains a 4 GiB disk reserve and projects recovery/evaluation storage
  from calibration. Insufficient capacity rejects a horizon without deleting
  another campaign's evidence.
