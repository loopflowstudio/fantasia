# Remote training delivery review — 2026-10-06

[Walkthrough](pr-review.html) · [Design](remote-training-design.md) ·
[Live evidence and contract](../docs/remote-training.md).

Refreshed for PR #252, base d7b69fc016c9b9d90c48190a414eb0cff6fe94f9,
head 6d718f770b4be0064ca300f9558a3fb3f8f4d6d8. This review refresh is local.

## Command naming feedback

Jack Heart suggested `cloud` in place of `remote`, then raised `manabot deploy`
and requested an updated review. The proposed public surface is:

- `uv run manabot deploy --regime recipe.json --mix hardware.json --out .runs/deployment`
- `uv run manabot deploy plan --regime recipe.json --mix hardware.json --out plan.json`
- `uv run manabot deploy --plan plan.json --out .runs/deployment`
- `uv run manabot deploy status`
- `uv run manabot deploy cleanup --deployment receipt.json`

Default invocation deploys; `plan` previews placement and price. RunPod remains
in the hardware mix. Current implementation still uses `remote run` and
`remote compile`. No product code changed. Compatibility aliases and internal
module naming remain unresolved; the review update does not imply full design
approval or a merge/navigation decision.

## Deployment type naming

Jack Heart flagged `Attempt` and `Receipt` as vague. Proposed replacements:
`RentalAttempt` for each intended guardian or training pod rental, and
`DeploymentReceipt` for the full operation's plan binding, attempts, returned
policies, cost and outcome. These names distinguish pod-level state from the
whole deployment and from existing training receipts. The walkthrough retains
real source under its current names; no implementation rename has been made.

## Evidence refresh

The prior review's unproved-live status is superseded by the current remote
contract: attempts 004–006 retain CUDA work, returned policies and four terminal
replayed arena games with deletion; 007 proves two-run setup reuse separately.
Total recorded Task cost is $1.6591 estimated/reported including prior failures
and shakedown. Zero pods is a dated observation, not a new inventory query.
Reports were inspected, not rerun; no rental occurred in this review update.
The original local compile at d8307606 produced the $0.310 projection retained
in the walkthrough. Full mocked default success/timeout coverage is still not
claimed. No strength or chapter acceptance follows.

Next useful action: review the proposed command surface, then carry accepted
feedback into the CLI, help, cleanup hints and documentation together. Keep
recorded transcripts and frozen receipts unchanged. No Flow navigation is chosen.

## Jack Heart's approval

Jack Heart approved the review in this conversation: “yeah loos fine approved”.
This includes the proposed `manabot deploy` command surface and the
`RentalAttempt` / `DeploymentReceipt` names. Apply those changes together across
CLI help, cleanup hints, imports, tests and documentation; preserve frozen
receipts and historical transcripts. The naming changes are not yet implemented.
This is human review approval; the following Flow step owns navigation and
remaining delivery work.

Review completion could not be recorded in Loopflow: both `lf session ready`
and the supplied `lf session complete` command failed because the configured
custom Home's development store is incompatible. Approval is retained here;
Session completion remains pending. No Home migration or replacement attempted.
