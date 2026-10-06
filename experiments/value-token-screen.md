# Scalar value-token screen — ETU-106

Jack Heart requested this prospective screen on 2026-10-05 after PR #222 merged.
This preparation does not launch training. The separate `value-token-screen` /
`screening` profile preserves the eight-arm value-model smoke and the existing
three-anchor scientific protocols. ETU-91's checkout, cohort and allocation are
untouched. No paid compute is included.

## Question and fixed contrast

Does changing aggregation improve learning against the fixed scripted opponent
at this small capacity, without changing information, learning rules or action
coverage? Historical mean, validity-masked mean and learned value token all use
width 64, four heads, one post-normalized attention layer and a scalar critic.
All other resolved settings are equal: Ataraxos move learning, semantic
Allies/Lessons observations, authored sideboards, ordinary flat decisions,
current-policy self-play, CPU and one thread. The shared value token also changes
policy representations; this cannot isolate a critic-only effect. No history,
compound decoder, belief sampler, categorical head or additional depth is added.

Each of seeds **10611, 10612, 10613** runs every arm. Initial shared parameters
use the same seed, but added token parameters and different policies cause later
RNG trajectories to diverge. Alternating forward/reverse arm order reduces one
order confound; it does not remove laptop contention.

Each run has two linked **400-update** stages, four streams and 64 transitions
per stream per update: midpoint at 102,400 learner transitions and end at 204,800.
Continuation retains the optimizer and collector. These are update-count
midpoint/end checkpoints, not assertions of equal elapsed time. Raw checkpoints
alone enter evaluation; EMA exports do not add replicates. Across nine runs,
7,200 updates and 1,843,200 learner transitions are scheduled.

Every checkpoint plays **100 games** against the source-pinned `scripted_greedy`
player: 25 deals **961060–961084**, each with all four deck/seat legs. The same
deals and candidate/reference action-seed aliases pair arms, seeds and
checkpoints. Total: **18 cells / 1,800 games**, no candidate-versus-candidate
matches, random anchor, PUCT anchor or extra endpoint cohort. The arena retains
terminal outcomes, exact replay, commands, failures and inference latency.
Evaluation deals are reserved separately from training seed streams; this does
not promise that no training game shares an opening hand.

## Allocation and stop policy

The hard ceiling is **eight laptop hours**, with at most **six hours of training**
and **two hours of evaluation plus reporting**. Unused training time cannot expand
evaluation. Each run has a 2,400-second watchdog; each stage has 1,190 seconds,
leaving setup/export margin. Watchdog expiry is failure, not a shortened successful
arm. Counts are fixed before execution and never increased to fill spare time.
The short retained ETU-106 smoke motivates 400 updates per half; extrapolation
is provisional and does not establish a long-run six-hour runtime.

At **two hours from launch**, `diagnostic-2h.json` records completed updates,
remaining-training projection, disk reserve and continue/stop. During training,
project remaining updates at the slowest observed run's seconds per completed
update, with 25% headroom. Stop if that forecast exceeds the six-hour training
ceiling, no completed-update rate is available, a run failed, or free disk falls
below 4 GiB. The check does not inspect scores or select a winning arm. If already
in evaluation, it records training completion and checks the same reserve.
The Python timer is delivered when the interpreter regains control; a native call
can delay it. Existing collector deadlines additionally bound rollout work.

Before launch, require the 2 GiB projected output allowance plus 4 GiB reserve.
This is a conservative reservation, not a measured peak. Stop immediately on any
training/export error, invalid/incomplete/replay-failing arena cell, game timeout
(120 seconds), command cap (10,000), phase deadline or total deadline. Finite JSON
receipts reject nonfinite diagnostics. Preserve all failed/partial attempts and
artifacts; there is no automatic retry, seed replacement, count adjustment or
training resume. A diagnostic stop requires a separately frozen next allocation.
If the process dies abruptly, elapsed cost is unknown until reconciled; never
infer unused budget from the last receipt.

## Prediction and interpretation

Prospective prediction: the absolute mean paired endpoint score differences
versus historical pooling will be below **5 percentage points for the token** and
below **3 points for masked mean**. This is a hypothesis, not prior evidence.

Report every seed at both checkpoints, learner-transition curves and cumulative
training-hour curves. At common observed cost use the last checkpoint available;
no interpolation, extrapolation or comparison outside overlapping cost support.
The existing report supplies per-arm training-seed/common-deal bootstrap intervals;
three seeds give descriptive uncertainty. Game-level intervals alone cannot
establish an architecture effect. Evaluation/replay costs remain separately
visible and counted toward the overall allocation.

A candidate merits a confirmatory follow-up only if its endpoint mean paired
score improvement is at least 5 points, no seed is negative, the shared-cost
comparison agrees, all games replay, and measured inference seconds per decision
are at most 1.25 times historical. A mean loss of at least 5 points in all-negative
seeds rejects that candidate for this recipe. Otherwise keep it unresolved.
These are screening dispositions, not automatic default changes or admission.
The candidate-to-historical paired differences must use matching seed/deal blocks;
per-arm confidence intervals are not difference intervals. Midpoint is diagnostic,
not a candidate-selection opportunity; the same fixed evaluation deals are reused,
so there is no untouched confirmation set.

One thread is a serving envelope, not matched inference compute: token attention
costs more. A scripted opponent can reward exploitable behavior. This screen
cannot establish general strength, exploitability, control competence, categorical
superiority, human-challenger success, or an isolated value-head mechanism.

## Resolved plan and exact launch

The committed [resolved plan](plans/value-token-screen.json) binds recipes, seeds,
deals, native extension, engine/model/content/setup/ABI sources, runner sources,
analysis notebook and dependency declarations. It is a same-checkout prospective
plan; loading it after source or native-extension drift fails before training.
It does not certify another machine's installed dependencies. Keep this checkout's
imported sources and native extension stable throughout a launched cohort.

From the repository root, the eventual launch command is:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run python -m experiments.runners.run_value_screen --plan experiments/plans/value-token-screen.json --out .runs/etu106-value-token-screen
```

This command is delivered to the repository session; **it was not run during
preparation**. The output directory must not exist. Do not launch alongside a
new competing campaign. Do not move, restart or modify ETU-91 to make room.

To resolve a new prospective plan without training after a deliberate source
change (retain the previous plan and review its changed identities first):

```bash
uv run python -m experiments.runners.run_value_screen --write-plan /tmp/value-token-screen-next.json
```

Offline analysis, including failed attempts with available receipts:

```bash
uv run python -m experiments.runners.run_value_screen --report-only .runs/etu106-value-token-screen
```

Software validation uses bounded fixtures: plan rejection, unchanged legacy
restrictions, full 18-cell scheduling, early arena failure, source-drift rejection,
two-hour forecast stop/continue and repeatable executed report/notebook outputs.
Fixture games and checkpoints are synthetic; they supply no strength or timing
measurement. Scientific execution remains unrun.

Gate (2026-10-05): the affected screen/value/study/architecture-recipe suites
passed **31 tests**; focused Ruff checks/format and `git diff --check` passed.
The committed resolved plan reproduces current source/runtime identities without
training. CI owns its broader matrix; no Rust or model code changed here.
