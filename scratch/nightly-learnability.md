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
