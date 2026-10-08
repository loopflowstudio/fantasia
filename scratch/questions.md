# ETU-126 continuation — 2026-10-08

Jack Heart authorized optimizer-preserving continuation of the first small run to
100,000 total updates after science job1, without interrupting live work or
replacing the remaining paired jobs. The supplied instruction requires a 100,000
learning-rate/regularization denominator. This is a substantive unresolved
schedule definition: the frozen Ataraxos recipe explicitly has no total-update
normalization (`target_count_rescales_rates: false`). Its formulas are
`clip(0.5 / iteration**1.1, 5e-6, 1e-4)` and `0.05 / iteration**0.3`.
`update_iteration` ignores fractional progress for this recipe. Preserving these
formulas gives LR 6.957944302072213e-6 and tau .0023684978179155515 at 26,001;
a denominator-dependent treatment requires a newly specified formula. No
alternative learner treatment or weights-only restart was selected.

Actual verified source `45940fe3587fe37851267d0c903c6030a3a64a92`, TrainingRun
`c2b8c6e731ee4126a2c2d18514dea4d1`, regime
`9a3a164cc499e63d6d3940596de469244fd368de2bfe7f1a92c32ce2a8204796`:

- raw SHA256 `3a3c65cbbc90231d9f96c5619b9bbc1b8ea88ac4711e1b1752fe2e99e33cb0da`
- EMA SHA256 `5c02212099606ca6b9199f5e3c8b4fe6511403f65c067997a2d1d469ed576681`
- optimizer SHA256 `381862476197c70879b652c6615159069d1d89f0961642670809633534dc9663`
- run JSON SHA256 `d4cc1d7b40ad042632607b4596cc6f34133ca5f448055faef78fb57fbd15234d`

Downloaded hash-verified artifacts are retained on Mini under
`~/.local/state/manabot/etu103-recovery-v3-science/continuation-inspection`.
Adam has 61 populated states, all at optimizer step 208,000. EMA metadata binds
iteration 26,000 and rate .999. Both policy metadata receipts agree with the run.
The completed record contains 26,000 diagnostics, 13,312,000 learner transitions,
3,328,000 exposures, 27,395,007 native decisions, 145,796 games and
15,865.934648 active seconds. Recovery artifact is null: no collector/RNG snapshot.
Optimizer-preserving restart on fresh game streams is feasible in principle;
exact CUDA process recovery is not established.

At observation 1791462373, the independent Mini controller was fresh, job0 was
finalizing at 26k on its existing pod, and jobs1–5 remained queued. Cohort phase
was uncertain due to the stale worker heartbeat. A 526,403,838-byte run JSON
explains substantial transfer work; completion/cleanup remained unverified.
No live job, source, controller credential or queue was changed.

Live L4 quote was $0.49/hour. Existing inclusive reservation is $48.867918369190;
admitted jobs plus prior/shared allowances are $20.367918369190, not settled cost.
Extrapolating observed rate gives 12.54358 additional active hours for 74k steps,
so a single admitted lease cannot fit. Two prospective 11.95h/$6.20 segments would
raise the reservation to $61.267918369190 before any extra reserves. This is not
price/allocation/credential admission. Segment design must allow evaluation,
large final exports, shared cohort deadline and restricted prefix authorization.

Remaining implementation: verified learning-state import/export and absolute
counters; explicit schedules after the definition is resolved; segmented
continuation; immutable queue interposition after job1 preserving jobs2–5;
controller/source/access admission, tests, landing and live queue verification.
PR5 delivery reconciled to merge 2a4fd419; rotated empty PR6 branch
`jack/keep-experiment-cohorts-running-and-optimizer-continuation`.

Check: verified live artifact hashes/contents and source formulas; no training,
rental, learner edit or continuation queue admission occurred.
