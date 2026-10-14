# Call the play app Academy

Decisions are in `naming-decisions.md`. Assumptions about which "etude"
occurrences stay are in `questions.md`. Both are accepted by Jack Heart
(2026-10-13) or recorded as reversible assumptions.

## Done (commits 496b46c7, d529c422, ffd57319, 12ade837, 7a51c5ef)

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
- The deploy scripts manage both the landing site and play, so their prose
  names the hosted apps and domains for Fantasia (Jack Heart, 7a51c5ef); the
  filenames keep the `academy-` prefix.
- PR #283 body lists every remaining "etude" category, the cutover steps that
  need Jack Heart's confirmation, and the ten pre-existing `tests/academy`
  failures (identical on base 1770a2cf; CI runs only
  `test_clean_machine_verifier` from that folder).

Check: `uv run pytest tests/academy/test_study_index.py -q` — 13 passed.

## Remaining

- Gate (d2d5e1c4): all six CI jobs pass (Rust debug, Python unit,
  conformance, visual reference, clean-machine play). Local
  `uv run pytest tests/academy -q`: 271 passed, the same 10 pre-existing
  failures. Ruff check/format findings in changed paths are identical to base
  (81 / 4 files) and CI does not enforce ruff. Rust edits are comment-only.
  Not run locally: full Python suite outside `tests/academy`, Playwright e2e
  beyond CI's clean-machine and visual jobs.
- Rebase onto MTG-79 if it lands first; `origin/main` has not moved past the
  base.
- Live cutover (Fly apps, Doppler, DNS) stays out of this PR and needs Jack
  Heart's confirmation. Jack Heart said the PR may land without his approval
  or a demo.
