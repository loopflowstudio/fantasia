# Open experiment decisions

2026-10-04. Jack Heart has established the regime/run names and the experiment
document + protocol + notebook/report structure. The following proposals have
not been accepted; they affect the expensive experiment, not the core model.

1. Does the laptop week cover both regimes and evaluation, or is it one week
   per regime? The draft uses 168 active laptop hours total. Confirm expected
   availability if the deadline is seven calendar days.
2. Does the first comparison stop at policy-only strength, or include the
   full RL -> frozen-policy belief learning -> search path? The draft proposes
   policy-only first and explicitly retains the latter as the next build.

Final budgets and scope remain draft, not accepted decisions. The implementation
must demonstrate both Ataraxos-inspired ablations and learning-speed comparison,
per Jack Heart's explicit scope. The proposed 15-hour ablation training screen
is a separate allocation unless the week is explicitly repartitioned.
Pilot coefficients,
sample counts and the proposed .55 prediction require a recorded experiment
freeze after complete-loop timing evidence. No current-world throughput or
effect-size claim exists for these recipes.

The additional review is incorporated with checked evidence limits. Named
horizon, reference, collection-KL, paper-filter and EMA contrasts are part of
the system's experimental uses, but only the five core arms are priced into
the proposed 15-hour training screen. Exploiter training and full belief/search
studies require explicit allocations. The accessible preprint appendix informs
new treatments; its exact settings are not asserted to match the inaccessible
final Nature supplement.

2026-10-04 active-goal update: Jack Heart explicitly requested landing the
required Tasks and then running the Ataraxos/MTG experiment. Actual experiment
execution is now authorized; the earlier implementation-only limitation is
superseded. Use 168 active laptop hours total as the conservative operational
ceiling inferred from the earlier one-week request, not an assertion that Jack
accepted every draft allocation. Include calibration, core ablations,
learning-speed training, evaluation and reserve within that ceiling. Freeze
feasible run/deal lists after measured integrated calibration and before
scientific scoring. A smoke or small pilot alone does not achieve this goal.
No paid hardware is authorized. Jack enabled prevention of automatic sleep on
power adapter; local pmset now reports AC sleep 0.

2026-10-04: ETU-95 found a concrete full-game exact-belief dependency: opponent
combat/target choices lack public likelihood identities, and materialization
cannot refresh some opponent prompts including discard. Preserve exactness by
marginalizing unobserved choices; never expose hidden choices as public data.
Rules status currently says no In Progress Project, so no separate Rules Task
was filed. Keep this within ETU-95's existing full-game acceptance; pursue a
serial follow-up after its active writer finishes. Do not call the bounded
local-update implementation a completed full-game exact-versus-prior comparison.
Native follow-up entry points: `possible_worlds.rs::MaterializeMode::RefreshOpponentCommitment`
currently refreshes only Priority/Learn; `agent/structured_offer.rs::PublicCommitment`
contains pass, cast, land, discard and Learn identities, not combat/targets.

- 2026-10-04 low-power sleep: 14:46:42–15:12:30 PDT, 1% battery; same campaign resumed on AC. Retained `.runs/ataraxos-20261004/sleep-20261004T144642-0700.json`: reserve 1,548 extra seconds; total charged+reserved+sleep 166.1656/168h. Reconcile this sidecar after supervisor commits its study charge, checking double counting. Do not mutate its in-memory ledger or frozen recipe.
