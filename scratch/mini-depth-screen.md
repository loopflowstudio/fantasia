# ETU-103 mini depth screen

Jack Heart authorized the first mini screen on 2026-10-06: depth 1 versus 2,
width64/heads4, scalar value-token/no-history, eight hours inclusive of all phases.
The exact protocol is experiments/model-capacity.md. ETU-91 and ETU-106 laptop
checkouts/native/processes are untouched; no laptop training occurred.

Source: eac2535fce48866756a50347a261c250b2c5c76e (PR246). Mini remains pinned
to that clean commit at /Users/jack/src/etude. Existing native SHA256 is
f12d239e1034b0f4f7f2e820da5e1fce10c4bc426dd56d511214e641d4e1fa8b; source diff
against the prior mini checkout b43066d was empty under managym. Existing remote
.runs remains retained. Notebook dependencies were installed before launch.
LF mini main sync was a no-op; authorized git fallback pinned the published commit.

Detached supervisor PID 78829 was verified PPID1 with live preflight child 78833.
Root: jack@100.96.227.95:/Users/jack/src/etude/.runs/etu103-mini-depth-20261006-1
Sibling .launch.json/.launch.log hold launcher receipt/output. supervisor.json
binds start 1791306295.444871 and deadline 1791335095.444872 (28800 seconds).
Calibration must finish and write resolved-plan.json before scientific training.
No retries, score-based selection or default/promotion claim is authorized.

Checks: local focused suite 67 passed/2 intentional skips; mini affected/native
fixtures 69 passed/3 skips; campaign preflight 10 passed/1 skip; focused Ruff clean.
PR246 auto-merge was requested with lf land. lf pr reconcile returned errors for
unrelated already-removed worktrees; no repair attempted. GitHub is merge authority.

Verified scientific launch: both calibrations completed (107.6083/133.8007 s
process time); total preflight/calibration 263.2274 s. Timing-only admission froze
700 updates per seed-arm, 350/350 stages, three paired seeds 10341–10343.
Plan SHA256: 4fc10d1a93bc2a514ea6f4e1c304ef4851393aad1343e59e944323e2ca907b7c.
Training child 79369 was live with six durable updates; supervisor 78829 alive
285 s after launch, 28,514 s remaining. No scores or scientific result yet.
Plan, calibration, preflight and launch-time supervisor snapshots are copied to
local .runs/etu103-mini-depth-launch; authoritative live evidence remains remote.
Do not update remote source/native while this campaign runs. Raw scoring follows
all six complete training runs; EMA remains retained and unscored.
