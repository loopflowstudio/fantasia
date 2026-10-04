# ETU-97 — bounded frozen-policy attacks

2026-10-04. Jack Heart authorized implementation and landing, with only small
bounded real-game proof. Scientific comparisons remain open; ETU-91 is untouched.

Demo: a frozen JSON attack plan drives independent TrainingRuns against admitted
checkpoint bytes, retains increasing update-budget checkpoints, and evaluates
initial and trained attackers on untouched four-leg arena deals. Saved reports
show attack curves, paired improvement and training-seed uncertainty, costs,
behavior counts, failures and scenario support. No rating is imported.

Reuse TrainingRegime/TrainingRun and VerifyStore, the repaired learner-only
NetOpponentTrainer, ordinary checkpoint admission and INT-6 Command replay.
Add explicit frozen-opponent recipe input rather than a competing trainer.
The update ladder declares cumulative learner work and reports actual elapsed
cost; it does not claim equal wall time. Retain all rungs, including failures.
Freeze source/runtime, targets, anchors, seeds, cost caps and predictions before
execution. Final deals must be disjoint from producer and native collector seed
ranges. Scientific launches require separate allocation; no long run here.

Risks resolved: arena already executes four deck/seat legs and replays semantic
Commands; it is separate from GameSession's human attempt store. Automatic passes
are not human decision rows. runtime_fingerprints must receive selected_match,
not its Interactive default. Historical scenarios use custom cards and cannot
silently admit selected semantic checkpoints. Validate their premises separately
and explicitly report current selected-setup incompatibility.

Acceptance: focused recipe/admission and analysis tests; real exploitable toy
positive control; bounded current-world scenario probes; one selected-world
four-leg attack smoke with policy-free replay. A negative attack never certifies
Nash equilibrium. No demo acceptance or ETU-85 completion claim.

Additive scope; no deletion targets. Historical population treatment remains
explicitly deferred pending a measured overfitting finding and its own budget.

Root continuation: the two frozen-opponent contract/runtime tests pass. All five
historical scenario reference/contrast pairs resolve as intended; selected-match
scoring is explicitly unsupported, with a passing regression test. The proposed
positive control initially referenced absent Grizzly Bears (no training ran).
Using supported Gray Ogre with a 16-card deck gave before=after=.5 after 16,384
learner transitions, 624 games and 7.10 seconds; this failed sensitivity. A
40-card toy deck is now under test to allow combat before decking. These are
fixture-development attempts, not held-out scientific evidence or seed selection.

The 40-card fixture with initial pass bias 3 gave .96875 to 1.0 in 7.36 seconds, failing the improvement threshold because its baseline was already strong. Next fixture uses pass bias 5 with unchanged seeds and training budget.

Bias 5 gave .515625 to .5 in 8.11 seconds; only four spells were cast during training, so the fixture did not supply enough successful exploration. Testing intermediate bias 4, without changing the held-out seeds or assertion.

Bias 4 gave .59375 to .640625 in 8.26 seconds, below the unchanged sensitivity
threshold. The positive-control remains failing and must not be claimed as
proof of attack learning. Next diagnose learning dynamics or allocate a larger
bounded update ladder within the existing 110-second test deadline; do not relax
the expected improvement or select a favorable seed. No PR published yet.

With the same bias-4 fixture, seeds and assertions, a 64-update ladder passed:
65,536 learner transitions, 1,086 training games, 114,271 environment microsteps,
25.275 seconds. Fresh evaluation was .59375 before and 1.0 after (64 games each).
This is a development positive control, not scientific target-policy evidence.
The independent-seed attack-plan runner, paired arena/replay reports and bounded
selected-world end-to-end smoke remain to implement before ETU-97 acceptance.

Added AttackPlan/AttackTarget with explicit byte identities, declared producer and
independent attacker seeds, strictly increasing cumulative updates, separate final
deals and full-cohort budget admission. Eight plan tests pass, including seed
namespace leakage rejection and continued-optimizer stage construction. This is
plan validation only; execution and arena/report integration remain unfinished.

Implemented attack_execution plus `uv run -m experiments.runners.run_attack_plan`
CLI: fresh frozen plan, target/seed TrainingRuns, initial and every retained raw
checkpoint, four-leg arena cells, exact replay admission, seed-bootstrap paired
endpoint reporting, per-cell traces/registrations and retained failed manifest.
Nine plan/scenario checks pass. Full 24-game, two-attacker-seed smoke is running;
first fixture attempt rejected missing semantic_pack before training, now fixed.
Review failure accounting, timer cleanup and full CLI evidence before delivery.

Selected-world smoke completed: 24/24 games replayed across two attacker seeds
and baseline/two update rungs, total45.680 seconds. Scores stayed .5 for seed301
and .75 for seed401 at this workflow-only budget; no learning claim. Added
scenario evidence to each attack manifest and run_paths before execution so
failed training remains visible. Failure-injection test passes and proves timer
handler restoration. Final docs, full focused check, latest-main sync and CLI
proof remain before publication.
