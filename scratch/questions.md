# ETU-118 open implementation assumptions

- Jack Heart's 2026-10-07 restart direction moves the single sustained cohort to
  mini after ETU-105 CPU release. The remaining original week follows that cohort;
  no duplicate laptop run or separate ETU-116 duration study is inferred.
- The calibration amendment reserves 7200 seconds inside that remaining week,
  including three 1800-second learner caps, 1200 evaluator seconds and 600 seconds
  of coordination/report overhead. It addresses the timeout for the newly selected depth2
  recipe; the approved sustained horizon is 10000 updates, implemented and measured; the fixed mini cohort is running. Live random monitoring uses its own
  25-deal family at initialization and fixed stage milestones, not hourly exports.
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

- Mini preparation exceeded the 600-second overhead subreserve before a retained
  pre-learner PATH failure. Every charge is included in the 4355.137744-second total;
  actual new preparation stayed within the 7200-second amendment. No scientific seed
  was retried and no additional week was allocated.
- The default AWS chain and configured softmax SSO credentials are unavailable on
  mini. Preserve model/evidence bytes; archival requires usable credentials. W&B
  backfill succeeded through update128; later backfill is not automatic.
