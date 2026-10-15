# Nightly learnability — reconciled 2026-10-15

Task lf-6700bb9: implementation locally qualified; review publication and reporting
activation remain incomplete. Jack Heart's accepted directive of 2026-10-15 owns
the outcome: few shared models, nightly CPU regression evidence, a public report
in a new manabot Discord, and a review PR without automatic merge. No separate
accepted design exists. No paid compute, cloud launcher credentials, interference
with existing experiments, or additional full-game campaign is authorized.

The implemented protocol uses three generic models (seeds 17/29/43), each fitted
once on 24 mixed cases and scored on those plus 24 held-out cases. Six families,
both public-life-conditioned preferences, 240 fixed updates and probability
>= .90 per case remain frozen. Native consequences, offer/object invariance,
initialization/no-update and identity-removal controls provide separate evidence.
Python ability coverage is projection-only; the debug Rust regression supplies
native two-ability legality/resolution. One seed-197 toy PPO model exercises the
production update and ordinary world-bound checkpoint reload. These choices
implement the directive; they do not establish strategic strength or MTG-118
acceptance. Mixed-setup capacity weights are diagnostic artifacts, not playable
checkpoints. No semantic cohort or per-assertion training is needed.

`manabot/verify/action_cases.py` owns shared fixtures and transforms;
`learning_control.py` owns the extracted PPO control. Structural tests reuse both.
The duplicate test helpers, tuple adapter and transforms were removed. The
supervisor owns total runtime and a 480-second watchdog. Fresh output directories,
incremental JSON/Markdown reports, artifact hashes and nonzero failure exits are
implemented. The GitHub workflow runs the full suite on relevant PRs, scheduled
runs and manual dispatch, with overlap protection and retained failure artifacts.
`--pr` is an explicit one-seed local subset that skips PPO. The local Keychain
publisher has tested failure payloads, delivery receipts and duplicate prevention;
it has never posted.

Frozen qualification at `3b3e35fd` plus its recorded source digest passed all 144
scores in 39.6s wall / 39.4s CPU. PPO held-out wins were 1.0 versus .640625 for
no update, using 65,536 learner samples. Compatible archived runtimes at
`9576dc40` (w4) and `78bf9429` (w5) establish w4 attack ties, w5 attack learning,
and later-family ties in both. Ablations are not historical runtime evidence.
`docs/evidence/learnability/qualification.json` preserves original attempts and
failures; its roughly 113s execution subtotal excludes subsequent compression
checks (34 tests in 4.83s and a one-seed run in 4.92s). Builds are recorded
separately. The compression run retained the same 48 scores and curriculum digest.
Original instruments remain in `.runs/learnability/pre-compress-source/`; raw
weights and reports remain local. Frozen receipts were not rewritten.

The local `origin/main` ref and HEAD both remain `3b3e35fd`; no fetched upstream
change informed this reconciliation. The supplied `.lf/wave/intelligence` is
absent. Legacy `wave/intelligence/GOAL.md` and relevant MEMORY sections were read:
the October 11 baseline and October 8 mirror records separate software delivery
from scientific acceptance and forbid inferred restarts. Memory headings and
immediate directories were inspected; no child MEMORY files exist. Other legacy
memory sections were not fully reviewed. The legacy files remain unchanged.
Proposed memory lesson, pending the selected memory location: capacity fits,
production PPO toy controls and full-game strength are distinct evidence layers;
historical alias qualification requires matching source/native runtimes, never
checkpoint relabeling. This is a proposal, not an added Wave decision.

Remaining: gate/review and publication of the review PR, then the first hosted
full-suite measurement to assess GitHub CPU suitability before merge. Scheduled
execution starts only on the default branch. Discord activation requires the new
server/channel webhook in local Keychain, a genuinely public evidence location,
and a mini-side scheduled download/publication or local-run/publication job.
Neither public hosting nor that scheduler is implemented. The destination and
hosting choice remain unresolved; no public URL or posting receipt exists.
The accepted deliverable explicitly retains this provisioning dependency.

Check: `git diff --check` — passed; existing qualification and compression results
reused, with no additional training or test-suite rerun during reconciliation.

## Review publication — 2026-10-15

Published ready-for-review PR https://github.com/loopflowstudio/manabot/pull/290
at head `e94b0e10643d430f88aa2bff3b61beaeef505d49`; base is `main`, whose
remote tip matched `3b3e35fd` at inspection. Auto-merge is off; Task completion
was not requested or recorded. The PR description preserves the capacity/toy
PPO limits and unresolved Discord/public-hosting/scheduler dependencies.

Publication review added the existing four reporting/publisher contract tests
to the nightly workflow; none of the prior workflows invoked them. That exact
command passed locally (4 tests, 2.08s). Scoped Ruff and diff whitespace checks
passed. Retained full and compression artifact hashes all matched their receipts;
no new training campaign was run. GitHub checks started, with the updated head's
learnability job pending behind the initial run at final inspection. Hosted
runtime and final CI conclusions remain unverified.

Loopflow publication initially committed the added scratch notes. `lf scratch
clear` removed them from the PR diff, then `lf pr publish` updated the PR.
These notes were restored locally after publication; the published diff contains
only the 17 implementation, test, workflow, documentation and evidence files.

## Hosted observation — 2026-10-15

PR #290 at `e94b0e10643d430f88aa2bff3b61beaeef505d49` remains open,
ready for review, with auto-merge off. The pursue Flow completed all steps.
GitHub Actions run 38773826552 passed: the full shared-model diagnostic took
122.7 seconds; dependency/native setup took 39 seconds, and the whole job
took 3m17s. Debug ability resolution and all four publication/reporting contract
tests passed. This supplies the first hosted CPU measurement and fits the
few-minute target. At inspection, Linux/macOS integration checks were still
running; all other reported PR checks passed. Review remains in the present
Task conversation; no merge or Task completion is authorized by this update.

## Broader distinguishability tests — direction 2026-10-15

Jack Heart requested broader regression tests inspired by the attack/decline
aliasing failure. He clarified that the target is learning to distinguish more
kinds of choices, not learning a strategically correct direction of preference.
Land-versus-pass is an example of a separability case, not an instruction to teach
land-drop strategy. Audit native choices, both encoders, object/focus joins and
ordinary policy scoring; add tests that can fit either preference and survive
reordering. Preserve shared-model economics and expose genuinely equivalent
choices rather than demanding arbitrary object-ID discrimination. Tactical
credit-assignment/general-strength experiments proposed in conversation were
not selected. Continue this review's coverage in the current checkout; no
new full-game campaign, merge or Discord activation was requested.

Measured GitHub receipt (run 38773826552): capacity fits 7.62/7.66/7.69s for
seeds 17/29/43; PPO control 92.12s including 84.81s training; full diagnostic
122.69s wall, 122.55s CPU. Local capacity fits are about 3.2s each. Current
workflow already runs full diagnostics on relevant PR updates and nightly;
these measurements do not imply execution on every local commit or all pushes.

### Broader probe results

Added ten native choice pairs in `tests/model/test_choice_separability.py`:
land/pass in second main, cast/pass, block/decline, blocking one of two different
attackers, scry keep/bottom, kicker pay/decline, self/opponent player targets,
revealed-card selection, Learn discards, and waterbend tap candidates. Native
and scalar encoders agree; every offered focus resolves, each representative
choice changes the native successor state, offer/object permutations preserve
scores, masks and deterministic sampling agree, and weights reload. Targeted
field-removal controls recreate forced ties. Two fixed-seed shared models fit
all ten pairs with opposite preferences (180 updates, lr .003, width32, P>=.95).
Identical physical copies share probability and remain equal-scored.

Attempts retained here: initial native fixture run 3 failed / 7 passed in
1.55s (unregistered Scathe Zombies and cast attempted before the main phase).
Corrected fixtures use registered Water Tribe Rallier and advance to legal cast
priority. Initial two shared fits then failed at .5 probability for a chosen
physical copy among identical cards (10 native tests passed; total 3.78s).
Corrected the oracle to score the observable card-definition class, preserving
the .95 threshold and fixed budgets. Twelve tests passed in 3.65s. Replacing the
broad alias control with targeted channel removals passed 12 tests in 3.60s.
Final focused run: 46 passed in 6.91s; Ruff and diff whitespace checks passed.
No new production aliasing defect was found, no model/rules schema changed,
and no full-game strength experiment was launched. The preflight now runs
these probes nightly; existing integration CI also collects them on PRs.
