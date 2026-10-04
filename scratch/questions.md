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


## Implementation choices (2026-10-04)

Jack Heart split delivery into regime/run infrastructure (ETU-89), RL
correctness/treatments (ETU-90), and study/arena/report (ETU-91). Three dedicated
workers now own these Tasks in separate stacked checkouts; the boundaries are
in worker-handoff.md. ETU-91 must integrate ETU-90 before final acceptance. Preserve their separate
acceptance evidence. The smoke uses one fixed random anchor and one four-leg
block per checkpoint, alongside paired recipe comparisons; the expensive
three-anchor scientific cohort remains proposed. CPU only is certified.

ETU-75 owns ordinary checkpoint world/setup validation. Reuse ordinary checkpoint
writers/loaders and sync its landed contract before delivery; do not introduce a
parallel checkpoint compatibility format. Live same-run continuation is supported;
external resume requires additional explicit artifact/cost admission and is not
silently inferred from a model checkpoint.
