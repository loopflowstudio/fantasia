# ETU-126 continuation — 2026-10-08

Jack Heart authorized optimizer-preserving continuation of the first small run to
100,000 total updates after science job1, without interrupting live work or
replacing the remaining paired jobs. Jack Heart corrected the earlier assistant
wording on 2026-10-08: rates must behave as if 100k had been planned initially.
Keep the existing absolute-iteration Ataraxos formulas unchanged and resume at
26,001. No denominator or human schedule decision is outstanding. Preserve raw,
Adam, EMA and counters; reset collector/game/RNG streams explicitly.

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

Job0 subsequently completed: final manifest verified, seven evaluations, confirmed
provider absence, estimated charge $2.9223462572991847. Job1 is independently
running on Mini; jobs2–5 remain queued. No training was interrupted.

Live L4 quote was $0.49/hour. Existing inclusive reservation is $48.867918369190;
admitted jobs plus prior/shared allowances are $20.367918369190, not settled cost.
Extrapolating observed rate gives 12.54358 additional active hours for 74k steps,
so a single admitted lease cannot fit. Two prospective 11.95h/$6.20 segments would
raise the reservation to $61.267918369190 before any extra reserves. This is not
price/allocation/credential admission. Segment design must allow evaluation,
large final exports, shared cohort deadline and restricted prefix authorization.

Implementation now adds typed learner-state import with original wire-digest
admission, unchanged absolute schedules, fresh collector streams, preserved
Adam/EMA, inherited monitoring coordinates, and immutable queue interposition.
The controller binds only final manifests; workers fetch exact versioned inputs.
Remaining: finish gate, land software, admit two 37k segments with realistic
reserves, upgrade the existing Mini service in place and verify durable ordering.
No deletion targets; frozen six-job scientific definitions remain unchanged.

Check: isolated remote suite 158 passed/2 expected skips; updated initial admission
and service checks 30 passed/1 expected skip; explicit source-upgrade fixture passed.
