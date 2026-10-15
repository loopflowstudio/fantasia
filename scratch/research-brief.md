Requested by Jack Heart on 2026-10-14 from Understanding Strategic Learning in Manabot, published in PR287. Source: https://github.com/loopflowstudio/fantasia/blob/68eba6104e3049b0feb73e8d243e8a686eb1abf6/manabot/LEARNING_RESEARCH_GUIDE.md

This is a scoped research follow-up, not approval of the guide's proposed mechanisms. Verify current code and retained evidence before drawing conclusions; source-check paper-specific claims. Distinguish implemented instruments, measured benefits, hypotheses and unknowns. Preserve frozen experiment identities and all negative/inconclusive evidence. Existing experiments and their checkouts must not be interrupted or modified. Use existing research, arena and reporting instruments rather than a second runner.

The first deliverable is a decision-bearing research report and a prospective bounded protocol. Use available code, saved artifacts, and small local correctness or profiling probes with explicit limits recorded before execution. No paid resources or new training campaign is authorized by capture or the initial analysis launch. Record source/world/schema/checkpoint identities, actual cost, uncertainty and failures; propose additional empirical work separately. Questions may remain open with explicit missing evidence. Keep plans and analysis in topic-named scratch notes until accepted for durable publication.

Problem and outcome
Search can overrule a useful learned policy using noisy or biased values. Determine how the current planner turns evidence into an action distribution, and define an isolated comparison with a single KL-only or full magnetic mirror-descent update.

Acceptance
- Inspect actual flat/PUCT/compound-policy search and MTG-95/99/100 evidence. Trace raw-policy, prior, value, belief and continuation identities; locate one narrow root-selection boundary without introducing another world or planner stack.
- Source-check the one-step closed form against the stated objective and paper. Distinguish trust KL to the raw trained policy from magnetic KL to a fixed reference; make no network-weight update at inference.
- Define raw policy, current selection, KL-only and full MMD controls sharing exactly the same sampled worlds, rollouts, evaluator and realized compute. Specify value units, step size, masking, zero support and numerical behavior.
- Demonstrate or specify small correctness probes for the root update and information boundary, and a prospective held-out comparison with belief-error sensitivity, policy KL and cases where extra search becomes more confidently wrong.

Boundary
This is the focused root-update follow-up to MTG-99, not a new MCTS architecture, belief-model rewrite or training campaign. Preserve MTG-107's model-interface review and existing compound policy meaning. Initial execution delivers analysis, concrete test cases and a protocol; broader implementation or scored cohorts require subsequent selection.
