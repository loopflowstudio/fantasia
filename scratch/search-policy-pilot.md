# Policy pilot evidence — archived, Mini baseline pending

Full prospective protocols, failures, repairs, receipts, hashes and costs are
preserved at `a5ba5dbc3895b51683e616d86165ccef61094ce3:scratch/search-policy-pilot.md`.
All local artifact directories remain intact. No historical result is relabeled.
Main subsequently advanced to w6 at `3b3e35fd`; the w5 development pair below is
historical and no longer runtime-admissible. No replacement pilot is selected.

- October 14 w4 attempt (`.runs/search-policy-pilot-20261014`): flat exceeded
  the 4 GiB watchdog; compound failed lowering an attacker declaration into a
  later turn. Both failures were retained. No selected checkpoints or arena.
- October 15 repaired w4 pilot (`.runs/search-policy-pilot-20261015`): both
  completed; eight-game arena 4–4 and 1,140 Commands replayed cleanly. The flat
  encoder nevertheless aliased attack/decline, forcing 50/50. This score cannot
  support a representation comparison. Exact old flat bytes reproduce the tie.
- Signed w5/input-v2 prototype (`.runs/search-policy-pilot-w5-20261015`): both
  completed; eight-game arena flat 5–3 and 1,288 Commands replayed cleanly.
  Superseded when Jack Heart selected stacking on PR288's 1/0 encoding; its
  checkpoints are rejected by the selected runtime, never silently adapted.
- PR288 development pair (`.runs/search-policy-pilot-pr288-20261015`):
  source `238801b7789571d53d49b763653c0d768892a683`, parent PR288 head
  `d9bbfe29beac2d23b2f74581f52f203b015a2c59`, w5/input-v1. Flat run
  `942f1505b7f7467f996674c2491fd964`, compound `8304bed90a1d4f0ea89c8275fa43c55a`.
  Four iterations each, seed 141001, CPU thread/worker 1, no learned beliefs.
  Flat: 5.634 wall/5.591 CPU seconds, 746,422,272-byte peak, 1,024 rows/12 games.
  Compound: 24.690 wall/24.563 CPU seconds, 1,041,448,960-byte peak,
  1,207 factors/eight games. Final raw exports load successfully.
  Arena: **4–4**, eight games, 1,328 Commands replayed without mismatch,
  20.663 seconds. Real attack root yields distinct logits with native/Python
  parity. This demonstrates plumbing and learnability, not strategic strength.

That pair's `training.sqlite`, `arena/`, `flat-declaration-probe.json`
and `pilot-evidence.json` retain full provenance; manifest SHA-256:
`9e8b6a85f5f60cb07e2e1c8c5064a91366acd0e155af6dbd5379b254b799e764`.
Combined validation: 395 debug Rust tests and 193 Python checks passed/one
skipped. No full-suite green claim. Earlier collection failures and frozen-w4
fixture failures remain in the archived notes/logs.

All pilots were preregistered, CPU-only, one fresh pair at a time, stage/run
caps 300/360 seconds, 4 GiB threshold, eight paired development games with
60 seconds/4,000 Commands per game and a 600-second outer cap. No held-out
strength study, learned belief training or paid resources were selected.
The three-seed training comparison and MMD/KL/PUCT strength experiments are
now held for the Mini baseline. Integration fixtures may use these saved
checkpoints; they do not become the baseline by convenience.
