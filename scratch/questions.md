# Remote training decisions — 2026-10-06

- Jack Heart authorized $50 total across all attempts and source branch pushes;
  PR review/readiness and landing remain prohibited. The helper/example retain
  a smaller $4.90 deployment ledger ceiling; add the reported $0.29 shakedown.
- CUDA self-play is float32, one worker, declared rental thread limits. Other
  stages and CUDA recovery remain rejected, preserving local CPU capabilities.
- Pod-side self-deletion is now live-proven. Provider outage can still prevent
  deletion; unknown billing remains unknown and cleanup must be confirmed.
- ETU-119's persistence fix is merged. Earlier frozen runs remain unchanged;
  observed update intervals do not identify all causes of slowdown.
- Jack Heart authorized local-disk setup, then a small worked two-experiment
  example. No public reuse API, mode, flag or idle-policy abstraction is wanted.
  ETU-120 is folded/cancelled; prebuilt images remain separate under ETU-121.
- The example reuses one exact source/lock/native build for two seeds. Changing
  dependency/native inputs needs a fresh environment and is outside this example.
