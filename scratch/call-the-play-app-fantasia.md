# Call the play app Academy

Decisions are in `naming-decisions.md`. Assumptions about which "etude"
occurrences stay are in `questions.md`. Both are accepted by Jack Heart
(2026-10-13) or recorded as reversible assumptions.

## Done (commits 496b46c7, d529c422)

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
