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

Remaining: publish PR and prepare `scratch/pr-review.html` for Jack Heart's visual
and product review. No merge, auto-merge, or task-completion operation is authorized.
