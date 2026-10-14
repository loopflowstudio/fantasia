# Call the play app Academy

Decisions are in `naming-decisions.md`. Assumptions about which "etude"
occurrences stay are in `questions.md`. Both are accepted by Jack Heart
(2026-10-13) or recorded as reversible assumptions.

## Done (commits 496b46c7, d529c422, ffd57319, 12ade837)

- `etude/` → `academy/`, `tests/etude` → `tests/academy`; packaging, isort,
  Dockerfile, ASGI entry, scripts, CI and e2e paths follow.
- `ETUDE_*` app variables → `ACADEMY_*`. Remaining `ETUDE_*` are
  experiment-system (`ETUDE_URL`, `ETUDE_TOKEN_FILE`, `ETUDE_DATABASE_URL` in
  the center adapter), the Cloudflare zone variable `CLOUDFLARE_ZONE_ID_ETUDE_GG`
  (domain stays), and history in `docs/plans/etude-fantasia-manifest.md`.
- `deploy/academy-fly.sh` and `deploy/academy-dns.py` renamed. Fly app names,
  Doppler project and `etude.gg` hostnames are unchanged. The play image sets
  its `ACADEMY_*` variables in the Dockerfile, and the Fly apps have no
  runtime secrets, so the current deployment keeps working after landing.
- CLAUDE.md/AGENTS.md naming section carries the Fantasia/Academy/manabot/
  managym/Etude model.
- `git grep -nE "^(from|import) etude"` is empty outside
  `experiments/etude-center-adapter`. `origin/main` has not moved past the base.
- The frozen W2-220 receipt records `-m etude.study_index`. `--verify` in
  `academy/study_index.py` accepts that recorded legacy command and does not
  rewrite the receipt; new receipts carry `academy.study_index`. No other
  frozen receipt names an `etude.*` module.

Check: `uv run pytest tests/academy/test_study_index.py -q` — 13 passed.

## Remaining

- Gate: Python suite, frontend checks, e2e, `./scripts/play` startup. No Rust
  behavior changed beyond names in three `managym/src` files, so `cargo test`
  in debug still applies.
- PR body: the list of remaining "etude" categories from `questions.md`, and
  cutover steps for the live rename (Fly apps in both `fly.toml` files, the
  `case` in `deploy/academy-fly.sh`, the alias table in `deploy/academy-dns.py`,
  Doppler project), which need Jack Heart's confirmation. Jack Heart said the
  PR may land without his approval or a demo.
- Rebase onto MTG-79 if it lands first.
- PR body: `tests/academy` has ten failures that predate the rename. They fail
  identically on base 1770a2cf. CI runs only `test_clean_machine_verifier` from
  that folder. The ten are `test_authored_match_authority`,
  `test_authored_match_parity`, `test_belief_recommendation_flip`, five
  `test_checkpoint_advisor` cases and two `test_public_commitment_parity` cases.
