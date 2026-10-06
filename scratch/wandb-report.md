# W&B graph report — 2026-10-06

Jack Heart requested a new report using W&B graphs. The published version is
[History input — learning and evidence](https://wandb.ai/loopflow-studio/etude/reports/History-input-%E2%80%94-learning-and-evidence--VmlldzoxODA2NzM3Ng==).
It uses the selected `loopflow-studio/etude` project without changing visibility.

Scientific score panels lead: separate arms with three seeds, matched transitions
and explicitly unequal recorded cost, then saved paired effect/95% bound series.
Seven content-bound evaluation projections contain fourteen retained rows. They
are distinct from the six training and two monitoring histories. Cohort admission
is shared with the Matplotlib renderer; no second statistical estimator was added.
Initialization remains unavailable and the endpoint effect remains unresolved.

Each arm's diagnostics collapse behind a heading, with native EMA 0.8, original
curves available, separate objective/value/entropy/KL and raw retention. W&B can
bridge missing samples; that difference from the earlier trailing-window report
is explicit. Monitoring stays separate per arm and single seed. All runsets filter
exact IDs and automatic run aggregation is disabled. Models remain in S3.

The create-once generator at `.runs/etu117-demo/wandb-report/report-generator.ipynb`
only reads saved sources and writes an editable report plan and HTML viewer.
Publication is explicit and creates a new native report, preserving earlier
manual edits. Original notebooks and reports were not overwritten. The report
plan, URL receipt, executed notebook, HTML and API verification are retained in
that directory. The [evidence guide](../docs/evidence/history-report-learning-2026-10-06.md#wb-graph-version)
owns reproduction. W&B Reports requires the new optional wandb-workspaces package;
its dependency updates W&B from 0.25.0 to 0.30.0.

Validation: 11 focused offline report/backfill checks passed; headless generation
preserved notebook bytes and reproduced the published plan digest after refresh.
API readback recovered the native report and exactly matched all fourteen new
score/effect rows. No training, games, artifact uploads or live-campaign changes.
`lf screenshot` returned a blank hosted page; visual rendering and interactions
are not verified. Jack Heart accepted the report as “good enough” and requested shipping on
2026-10-06. No specific browser observations were reported. Earlier no-landing
direction is superseded by that explicit authorization. Next: deliver this PR
through Loopflow; retain the evidence and notebook originals.
