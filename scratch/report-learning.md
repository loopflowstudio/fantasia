# ETU-117 report improvements

Jack Heart requested saved-data-only reporting and publication for review on
2026-10-06. No substantive training, evaluation or landing is authorized here.

Implemented per-regime diagnostic panels with a labeled trailing window, gaps at
missing values/update coordinates, raw downloads and sample/skip accounting.
Checkpoint strength leads: scientific Study exports and monitoring remain separate.
Scientific intervals reuse the existing seed/common-deal bootstrap. Monitoring
ABI differences prevent cross-arm panels; explicit within-run histories remain
available. Create-once notebooks preserve source edits.

Delete — do not maintain: replaced the default combined RL-loss panel. The public
raw metric API survives for existing edited notebooks. No evidence is deleted.
Compression reuses the existing bootstrap, scalar projection and report renderer;
no competing experiment execution or statistical authority was introduced.

The saved history demo is `.runs/etu117-demo/{scientific,monitoring}/comparison.html`,
with editable generators and source/copy hashes. Both lack initialization. The
scientific endpoint difference remains unresolved; near-ln(2) entropy cannot be
attributed to binary support from these exports. The durable report documents
measured counts, cost, sampling and the separate positive-control requirement.

Validation: `uv run pytest tests/training/test_experiment_report.py -q` — 8 passed;
headless scientific/monitoring notebooks and HTML/link checks passed. Rendering
was unavailable; no visual approval is claimed. An accidentally broader inherited
suite ran tiny training fixtures and started monitoring, then was interrupted
(18 checks had passed, no completed monitoring rows). Its retained temporary
receipts are `.runs/etu117-interrupted-validation`; originals remain untouched.

Published PR #249: https://github.com/loopflowstudio/etude/pull/249.
`scratch/pr-review.html` traces refresh, cohort admission and diagnostic sampling
to pinned code. Jack Heart's visual/product review remains pending. No merge,
auto-merge, or task-completion operation was requested.

## Dashboard demo — 2026-10-06

The current design is the reporting contract above; the
[durable evidence guide](../docs/evidence/history-report-learning-2026-10-06.md)
owns reproduction and interpretation. The saved scientific and monitoring HTML
were captured through `lf screenshot` at 1440×900, without executing notebooks,
training, or evaluation. Captures are retained at
`.runs/etu117-demo/scientific-review.png` and
`.runs/etu117-demo/monitoring-review.png`. This supersedes the earlier rendering
limitation for these two opening viewports only.

Agent observation: both opening views render legible strength plots. Scientific
seed curves and descriptive intervals are separate from the earlier one-seed
monitoring panels. Initialization is explicitly unavailable in the scientific
summary. The scientific introduction is dense and pushes much of the first plot
below the fold. Proposal, not an agreed revision: shorten the opening summary
and move detailed limitations beside or below the relevant plots.

Review route: open scientific/comparison.html, compare the three seed lines at
64,000 and 128,000 transitions, then expand “Policy, value, regularization and
sample retention.” Inspect separate policy/value/entropy/KL panels, labeled
trailing smoothing and skips; follow the metric documentation and raw JSON link.
Open monitoring/comparison.html separately. Its intervals condition on individual
checkpoints and cannot supply independent training-seed uncertainty.

Jack Heart has not yet supplied observations or acceptance in this demo session.
No design revision is agreed. Interactive expansion/download behavior and the
complete diagnostic layout have not been visually verified in this pass; no
in-app browser control tool is exposed. Recommended next action: Jack Heart
reviews the linked dashboards for readability and whether evidence limits are
clear, then records concrete feedback here before any landing decision.

## W&B setup — 2026-10-06

Jack Heart requested W&B installation and a working integration, authenticated
locally, and explicitly selected `loopflow-studio/etude`. This supersedes the
initial proposed `manabot` destination for these uploads. The first process was
interrupted during imports, before any upload. W&B 0.25.0 was already installed.

The existing exporter published six 500-row training dashboards and two separate
two-row monitoring dashboards to https://wandb.ai/loopflow-studio/etude.
All eight remote runs finished; API readback verified all 3,004 rows and every
saved scalar against the local dashboards. Readable run names, cohort tags and
sampling notes were applied. Local dashboards, delivery receipts and
`remote-verification.json` remain under `.runs/etu117-demo/wandb/`.
No training, evaluations, or source-artifact mutations ran. Scientific strength
results remain in the scientific HTML; these uploads do not import that study's
checkpoint scores. W&B system metrics describe the uploader, not historical
training. Visual workspace review remains separate from API verification.

Future backfill must explicitly pass `--project etude --entity loopflow-studio`
to `uv run python -m manabot.training.monitoring`; the historical CLI default
remains `manabot`. Preserve stable run IDs and existing prefix checks. This
setup request does not authorize landing PR #249.
