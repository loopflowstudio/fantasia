# Assumptions made during the Academy rename

- "Etude Fantasia" was replaced by "Fantasia" where the text meant the whole
  project (README title and opening, architecture title, package
  descriptions, deploy and wave overviews) and by "Academy" where it meant the
  thing a player uses (frontend, website, server title, Game wave). The
  website says "Academy" throughout because the brief lists it with
  player-visible surfaces.
- "Sepia Etude" is kept as the name of the visual language. It names a
  palette, not the app, and the brief did not ask for a new design name.
- The paper (`paper/`, including `etude.pdf` and the title "Etude Fantasia")
  is unchanged. Retitling a paper is an authorial choice outside a mechanical
  rename.
- Dated research and plan documents (`docs/research`, `docs/plans`) keep their
  prose and filenames as history; only file paths inside three plan documents
  were updated so they still resolve.
- Preregistered experiment write-ups (`experiments/*.md`) and the hashed
  benchmark contract `docs/benchmarks/study-branch-contract-v1.md` are
  unchanged.
- Wire headers (`x-etude-*`, `X-Etude-Next-Cursor`), browser storage keys
  (`etude.gui.*`, `etude.play.*`, `etude.score.notes.*`), the
  `etude:local-challenger` bot identity and `etude.*` schema and hash-domain
  identifiers are kept rather than migrated, so returning players keep saved
  state and a cached client keeps working across the deploy.
- Fly app names, the Doppler project, Cloudflare zone variables, the S3 bucket
  and the wandb project keep their names. Only repository files changed.
- Links to this repository were corrected from `loopflowstudio/etude` to
  `loopflowstudio/fantasia` in the README, the website and three live docs.
  Links inside training report generators and frozen visual-reference notes
  were left alone.
- `deploy/academy-fly.sh` and `deploy/academy-dns.py` keep their `academy-`
  filenames even though their prose now names the hosted apps and domains for
  Fantasia (7a51c5ef). Renaming them to `fantasia-*` is a reversible follow-up
  if wanted.
