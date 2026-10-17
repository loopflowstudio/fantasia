# Continuation observation

Implementation decision, 2026-10-16: the existing CohortState is the authority
for an admitted insertion deadline. Preserve a validated local snapshot for
outages; it grants no new deadline, job lifetime, or allowance. A scheduler
restart performs one reconciliation before deciding its observation window
expired, even when the local snapshot predates an insertion.

Delete — do not maintain: completed; no remaining targets.
The scheduler's pre-read cutoff and the report companion's memory-only
continuation deadline are removed.

Preserve owner locks, cohort identity validation, absolute cutoff plus 30-minute
observation grace, attempt reservations, redacted errors and original sources.
Retain scheduler state before job observation so provider failure cannot discard
a successfully read insertion. Reuse CohortState for the companion snapshot;
do not introduce another deadline authority or schema.

Acceptance: restart with stale scheduler state reads the admitted extension;
provider failure and subsequent storage outage retain it across restart;
reporting restarts within it without resetting charged attempts; mismatched
cached state fails; outages cannot extend any absolute bound.

Implemented both deletions in the existing service owners; documented the
observation contract in `docs/remote-jobs.md`.
The scheduler enters reconciliation directly and checks expiration after waiting,
without a first-iteration flag. Only reloading authoritative state can discover
an insertion; a tick does not change its deadline. Both service loops carry an
explicit observation cutoff, including grace, rather than adding grace at each
reporting consumer. The restart fixture constructs validated state directly.

Check: `uv run --extra dev --extra artifacts pytest tests/remote/test_cohort_service.py tests/remote/test_cohort_projection.py -q` — 16 passed, 1 opt-in launchd proof skipped; focused Ruff lint/format checks and `git diff --check` passed. Gate owns the wider remote suite and optional real launchd proof.

No implementation acceptance remains in this slice. Publication and any live
controller rollout remain later delivery/operation steps; no live compute or
cohort state was changed. No play/advice/Study code changed.

## Gate — 2026-10-16

Reviewed the full working diff against `4850e500`, the recorded implementation
base and merge base with `origin/main`. MTG-126's authoritative status confirms
this checkout and the running gate; no additional execution or delivery selected.
The implementation and public remote-jobs documentation meet this slice's
contract. Added a regression proving a successful remote read at the exact
expired cutoff retains the snapshot without ticking the scheduler or changing
remote state.

- `MANABOT_TEST_LAUNCHD=1 uv run --extra dev --extra artifacts pytest tests/remote/ -q` — 176 passed, 1 skipped in 41.84s; includes the real launchd kill/restart proof with fake storage/provider state. The CUDA continuation export test requires a CUDA-capable runner and was skipped, not passed.
- `uv run --extra dev ruff check manabot/remote/cohort_service.py manabot/remote/cohort_projection.py tests/remote/test_cohort_service.py tests/remote/test_cohort_projection.py` — passed.
- `uv run --extra dev ruff format --check manabot/remote/cohort_service.py manabot/remote/cohort_projection.py tests/remote/test_cohort_service.py tests/remote/test_cohort_projection.py` — all four files formatted.
- `git diff --check` — passed.

No gate blockers. No Python type-check command is configured in the repository
or CI. No UI, Rust, or dependency changes require additional checks. Native
launchd verification is local macOS evidence; cross-platform CI retains ownership
of its Linux result. Live cloud operation and CUDA recovery are not established
by these fake-provider lifecycle tests.
