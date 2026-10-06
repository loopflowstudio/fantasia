# ETU-115 delivery review — 2026-10-06

Reviewed published PR #247, base fd7437dfd84cd1e24785a6d7febee78fceff3d80,
head 20c5581cdbd9087e88d8dd99347f48594e47caf2. Local HEAD matched the
published head and the tree was clean before review artifacts were added.

Reading route: [walkthrough](pr-review.html) follows recipe declaration,
model construction/identity, and bounded measurement/export recovery.
[Design](train-ataraxos-sized-models-through.md) and
[retained evidence](../docs/evidence/ataraxos-scale-2026-10-06.md) own scope
and exact results. No product code, benchmark or training was changed/run.

## Technical feedback and unresolved judgment

The ordinary fields and opt-in 384/8/1536 rung implement the requested size
without changing the default capacity cohort. Existing architecture identity
normalization and frozen compatibility fixtures preserve default contracts.
Retained exports and verification recovery support training/reload feasibility.
The measured 203 slots correct the Task estimate; contention and diagnostic
Adam loss prevent RL-throughput or scaling claims. MPS is model-only evidence.

One source-inspected operational mismatch remains for Jack Heart's review:
scale catches child failures and records failed status, while the CLI ignores
that returned status and returns normally. Unavailable MPS can therefore leave
a failed report with successful shell exit. Automation currently must inspect
scale.json. Consider returning nonzero after saving the report; no change has
been agreed or implemented in this review.

Recipe omission preserves explicit feedforward width; explicit None resets it.
The walkthrough calls out that distinction and the retained verifier failure:
recovery reused completed exports and did not replace failed attempt records.

## Evidence and next action

Desktop and narrow opening/code-section captures were visually inspected.
Fragment captures were blank in lf screenshot, so isolated copies of the same
section markup/styles were captured for code inspection. Code scrolls inside
focusable blocks on narrow screens. Excerpts are extracted from the named Git
revision with pinned links. Prior notes record 65 passing affected checks;
this review inspected tests and logs but did not rerun them.

Jack Heart has not yet supplied feedback or approved design changes in this
review. Next useful action: review the walkthrough and decide whether failure
exit signaling needs follow-up. No merge or Flow navigation decision is recorded.

## Jack Heart's review feedback

After opening the walkthrough in the browser, Jack Heart said “looks great.”
This is positive feedback on the walkthrough; no specific code or design change
was requested. The CLI failure exit-status question remains unresolved.
