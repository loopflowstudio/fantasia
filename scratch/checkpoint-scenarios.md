# Checkpoint tactical scenarios — 2026-10-04

Jack Heart authorized ETU-97 software delivery and landing, with scientific
acceptance moved to ETU-99. No training is part of this change.

The demo is a CLI taking scenario-to-checkpoint assignments and producing a
readable offline report and arena Command traces. Each saved checkpoint must
admit the exact historical custom deck pair and saved observation capacity on
the current world. Selected-match checkpoints remain unsupported for these
roots; changing their binding would invalidate the instrument.

Reuse SCENARIOS and the native injection API for versioned roots, ordinary
`make_player(kind=checkpoint)` for decisions, and arena serialization/replay.
Persist root recipe/source/world binding, checkpoint digest, deterministic mode,
seed, all commands, stop reason, behavioral measurements and failures. Prefix
replay must be explicitly diagnostic; ordinary arena replay still requires a
complete game. Revalidate reference/contrast outcomes separately from policy
scores. Historical correct-line labels are local scripted premises, not proofs
of optimality. Belief-history attachment is unsupported for injected roots.

Acceptance: deterministic fixture checkpoints score all five scenarios without
training; policy-free replay verifies all roots/commands; wrong world/setup and
capacity reject; trace tampering fails; reports regenerate offline. Preserve old
experiment evidence. No deletion targets or native changes are needed.

Implementation complete. Deterministic fixture checkpoints cover all five roots;
hidden-hand swap, strict admission, failed prefixes and offline report replay
are tested. S2 correctness uses resolved removal; tracker intent remains only a
behavioral measurement. No scientific acceptance is claimed.

Checks: 37 affected Python checks passed with importlib collection; after main sync/native rebuild, 21 affected checks including compound replay passed; 7 native scenario tests passed in debug; final report-only regression and Ruff passed. CI owns the broader platform matrix.
