# ETU-77 bounded navigation change — 2026-10-05

Status: implementation candidate; human usability acceptance remains open.

Current Learn already implements the approved three-mode selector. Native w4
supports full finite Lesson retrieval; historical ETU-75 acceptance limits still
apply. ActionPanel receives original atomic offers and already highlights board
focus on keyboard focus. Model-facing ETU-107 is outside this change.

Six bounded seeded Random games in both deck assignments reproduced nine targets,
eight cleanup discards, ten Learn offers and six block choices. Retain exact
prefixes, native digest and viewer frames for target, discard, Learn, block and
optional cost. Search is a simpler reversible hypothesis than inventing target
or cost groups: labels already carry the intended card/action, while small
binary prompts and Learn's accepted modes need no extra stage.

Add optional label filtering at eight choices, keeping full lists by default.
Show matched/total count, Clear and Escape; clear hover evidence on edits and
scope query to the existing update/board-selection key plus Learn mode. Filter
only presentation: original offer IDs and ordinary Commands remain unchanged.
Duplicate labels must never be merged or dropped. Existing focus highlights
still distinguish physical copies on the board.

Delete — do not maintain: none; this extends the existing ActionPanel owner.

Proof: native prefix replay with exact offers/digest, headless browser filtering,
keyboard selection, empty results, cancellation, duplicate preservation and
recovery reset. Preserve existing Learn/combat checks; pinned Linux visuals go
to CI. A local walkthrough will replay these prefixes against the real backend.
No coaching-free human outcome or chapter closure is claimed.

Implemented and compressed: the filter stays in ActionPanel; the real backend
walkthrough reuses retained prefixes. Durable coverage and unresolved product
choices live in docs/choice-navigation.md and Game memory. No child Game memory
files exist. Fixed the existing PresentationStage unit count to include Pause;
the release accessibility assertion now identifies the turn status separately
from the new filter count. New browser checks join the release CI configuration.

Checks: frontend build/check + 100 unit tests; 13 focused dev/built browser checks;
release matrix on macOS with screenshots ignored; 6 native fixture/matrix checks
pass. Pinned Linux visual comparison is deferred to CI; existing references and
tolerances remain unchanged. Human usability and duplicate-copy clarity remain
open, and Task delivery must not complete ETU-77.
