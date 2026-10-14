# Slow-runner test budgets (lf-1973442)

- PR #284, head 077eb0f7 (dd55c3b1 + switch to default budgets). Evidence from PR #283 run
  38506247618 (macOS): monitor games took 7.5–30s; one 586-decision random-opponent game hit
  the 30s cap -> slowness, not a hang.
- `game_seconds` in `_bounded_game` includes spawn + torch import. Production defaults
  (120s/game, 600s/cohort) unchanged; tests now use them as hang guards.
- Done: both tests use default budgets; failures print per-attempt/per-row reasons
  (`_experiment_failures`, `failure_summary`). main has not moved since base 1770a2cf.
- Remaining: Integration (ubuntu+macos, gated on Rust Tests) has not reported yet — runs
  38512443186 (dd55c3b1) and 38512623897 (077eb0f7) in progress 2026-10-13. Need several
  consecutive green runs on both OSes, then land, sync #283, and confirm its CI.
- Check: `gh run view 38512623897` — Integration pending (Rust Tests in progress).
