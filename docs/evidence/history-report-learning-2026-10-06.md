# History report: learning trends and evidence limits

Jack Heart requested readable reports and an investigation of repeated entropy
near ln(2). The reporting demonstration uses saved evidence only; it launches no training or
evaluation. The validation scope error described below is separate from that demonstration.
The shared notebook generator preserves existing files and writes read-only HTML.

## Retained result

The completed `etu106-history-input-continuation` study contains two evaluated
checkpoints (64,000 and 128,000 learner transitions) for history-off/on across
training seeds 10631–10633. Each scientific cell contains 100 complete games;
1,200 games have exact replay. Both checkpoints are labeled **development** in the
frozen export. No initialization evaluation is retained. This study does not
establish improvement over initialization or a positive learning control.

| Arm | Midpoint seed scores | Endpoint seed scores |
| --- | --- | --- |
| History off | 39%, 26%, 26% | 26%, 26%, 28% |
| History on | 30%, 25%, 24% | 15%, 34%, 31% |

The saved on−off contrast is −4 points [−11.34, +1.33] at midpoint and 0 points
[−11, +9.33] at endpoint (paired training-seed/common-deal 95% percentile bootstrap).
The saved disposition is unresolved. Equal endpoints do not establish equivalence;
three seeds and one scripted opponent do not establish general strength. The
history-on arm also changes information and parameter count. The observed common
training-cost window is 735.31–1151.19 seconds; cutoff comparisons are not
matched-cost effects. Sparse checkpoints cannot resolve learning-speed dynamics.

The earlier `etu106-live-monitor` evidence has one training seed per arm and a
separate monitoring deal namespace/protocol. Its midpoint/endpoint records are shown on a separate dashboard; it also lacks
an evaluated initialization. Monitoring registrations have different observation
ABIs, so histories stay in separate per-run panels, without a cross-arm comparison. Monitoring is inspected development evidence, not independent method
uncertainty. The generator preserves the original coordinates and per-checkpoint
deal intervals without pooling either cohort.

## Entropy investigation

The six scientific run exports contain 3,000 update records and 2,965 entropy
values. **1,044 / 2,965** fall within 0.001 nat of ln(2). Counts by arm/seed:

| Arm / seed | Near ln(2) / entropy records | Empty-filter updates | Selected rows / collected rows |
| --- | ---: | ---: | ---: |
| off / 10631 | 121 / 496 | 4 | 14,103 / 128,000 |
| off / 10632 | 153 / 496 | 4 | 14,352 / 128,000 |
| off / 10633 | 238 / 492 | 8 | 10,958 / 128,000 |
| on / 10631 | 199 / 494 | 6 | 9,566 / 128,000 |
| on / 10632 | 171 / 496 | 4 | 19,379 / 128,000 |
| on / 10633 | 162 / 491 | 9 | 16,225 / 128,000 |

Measured explanation of the **instrument**: `ataraxos.update` overwrites entropy
and losses at each optimized timestep; the final retained value describes only
the last optimized minibatch. The 35 empty-filter updates retain no optimized
entropy/loss. Update-wide selection-group counts cannot identify the last
minibatch's legal support or its action mix.

Hypothesis about the **policy**: many last minibatches may contain nearly uniform
binary decisions. The observed numbers are consistent with this, but do not prove
it. The exports do not retain last-minibatch support sizes or probabilities;
no retrospective normalization or update-wide entropy can be recovered. Entropy
alone says nothing about whether the chosen actions win games. A future instrument
could retain sample-weighted update diagnostics and legal-support counts, but that
is separate work, not an invented historical aggregate.

## Reproduce the report without playing games

Source evidence remains read-only at:
`/Users/jack/src/etude.test-ataraxos-inspired-model-representations/.runs/etu106-history-input-continuation`.
The prototype/user-edited notebooks in
`/Users/jack/src/etude.agent-9039d61b/.runs/history-retrospective-report` are untouched.

```bash
uv run --extra notebook python -m experiments.runners.report_history \
  /Users/jack/src/etude.test-ataraxos-inspired-model-representations/.runs/etu106-history-input-continuation \
  .runs/etu117-demo \
  --monitoring /Users/jack/src/etude.test-ataraxos-inspired-model-representations/.runs/etu106-live-monitor
```

Open `scientific/comparison.html` first: independent seeds, descriptive uncertainty,
missing initialization, then optional per-regime diagnostics and raw downloads.
Open `monitoring/comparison.html` separately to review the earlier monitoring.
Each directory has its own editable `report-generator.ipynb`. Run All regenerates
HTML; creating or refreshing the report never replaces an existing notebook.
Changed source copies fail rather than silently replacing evidence. The output
`source-manifest.json` binds copied bytes to original paths/hashes.

The supervisor charged 10,945.66 seconds including the prior 91.16-second failed
calibration; the 2,888.45 evaluation seconds are already included. Run exports keep
collection, learning, export, diagnostics and sampled resources. The report does
not reinterpret these costs as normalized compute or retroactively create a
heartbeat for the completed legacy study.

Headless notebook execution and HTML structure/link validation are software checks.
No rendering environment was supplied, so visual presentation awaits Jack Heart's
review. Publication is authorized; landing remains forbidden pending that review.

A broader inherited pytest selection accidentally ran tiny training fixtures and
started a live monitoring attempt. It was interrupted after 18 checks passed;
that attempt has zero completed monitoring rows and is retained separately in
`.runs/etu117-interrupted-validation`. This exceeded the intended saved-data-only
validation scope. It supplies no scientific evidence and did not modify source
experiments. Subsequent checks select only offline reporting tests.
