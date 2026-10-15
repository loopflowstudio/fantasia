# Broader learnability search — 2026-10-15

## Frozen first-run question

Does a 30-minute CPU exploration expose action information loss or pipeline
invariance failures beyond the fixed PR suite? Jack Heart authorized this
prototype and a roughly 30-minute isolated remote run, with spending below $5.
This public repository uses a standard GitHub-hosted Ubuntu runner: no purchased
compute, credentials, laptop training, mini jobs, or scheduled nightly enabled
by this prototype. The existing short diagnostic's schedule is a separate
pending cadence decision.

Prediction, before execution: at least six distinct native decision families
will be audited, at least 100 distinct states will enter completed shared fits,
and at least 90% of per-case conditional fit scores will exceed 0.95. Predict
zero confirmed encoder/reordering/reload defects. Failure to fit is an
investigation candidate, not proof of missing information or a CI failure.

The runner generates eight seeded authored-game prefixes per round (up to 1,200
native steps each), swaps the two deck assignments, and samples up to six states
per decision family. At most 32 states enter a round's shared models. Native
versus scalar encoding and reversed-native-offer parity are audited before
sampling. Exact game seed, deck assignment, action prefix, state digest, raw
observation and encoded tensors are retained for every selected state.

Public action descriptors include verb, declaration, mode/ability selectors,
focus roles, definition, visible permanent attributes and keywords. Instance IDs
are excluded. Equal descriptor copies share mass; lexicographic first/last
classes define opposite artificial preferences in two separate shared fits.
The loss measures probability conditional on those two classes, not the chance
of selecting that action among every legal offer. No strategic label or
held-out generalization claim is made.

Three width-32 configurations: generic with attention, semantic with attention,
and generic without attention. Each uses paired initialization seed 1000+round,
240 Adam updates at .003, and P>=.95. Frozen-policy assertions check batching,
offer/object ordering, legal masks and state-dict reload at tolerance 1e-4.
The structural assertions inspect ordinary policy probabilities; reload is a
diagnostic weights round trip, not a world-bound playable checkpoint claim.

Cost/stopping: one standard CPU runner, one Torch thread, 1,800-second total
search budget checked in generation and each update; external 1,830-second
process watchdog, 40-minute job limit including setup. Save each completed fit;
record a final incomplete fit explicitly. No retries to obtain passing results.
Errors remain in artifacts. Separate native audit violations from optimization
misses. This is exploration, not a blocking PR gate or strength campaign.

Strongest confounds: public descriptors may omit relational distinctions; random
play may never visit rare decisions; small shared models and arbitrary ordering
labels may fail from optimization/capacity rather than aliasing. Diagnosis must
replay exact failures, check information flow, and distinguish those explanations.
An unchanged source rerun is not independent evidence of a repaired defect.

Execution entry point:

```sh
uv run experiments/runners/learnability_search.py --out .runs/learnability-search --seconds 1800
```

The temporary branch-only push trigger requires `[learnability-search]` in the
commit message. Normal PR updates do not launch another 30-minute experiment.

## Instrument correction, while first run continues

Run 38782530929 at source 6c445836 started the 30-minute search. The live log
shows completed generic/semantic fits, but immediate configuration errors for
the attention-disabled arm. Inspection reproduced the validator rejection:
`attention_feedforward_dim=64` is forbidden when attention is disabled. This is
a prototype configuration error, not a learned-policy defect. The initial run
and its errors are retained and continue to supply the other two arms.

Correct the attention-disabled setting to `None` and launch a separate
300-second supplemental run for that arm alone. Its first rounds reuse the
same generation/model seeds and fixed update budgets, permitting matched-case
comparison. It runs concurrently on a second standard GitHub runner ($0),
without extending the primary 30-minute run or changing its inputs. No rerun
of successful arms or thresholds is selected. The branch push trigger for this
revision selects only the supplemental arm; manual dispatch retains explicit
budget/configuration inputs. Both run receipts will remain in the final report.
