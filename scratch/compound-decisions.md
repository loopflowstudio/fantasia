# ETU-94 implementation

2026-10-04, Jack Heart authorized bounded implementation and landing; scientific
scoring remains unfunded. ETU-91 is untouched.

Demo: a one-threaded `manabot train --regime` compound self-play stage trains
complete games, exports an ordinary world-bound Agent checkpoint, and the
ordinary checkpoint player executes its sampled declarations through canonical
Commands. Focused tests compare exact native atomic/sequential states, enumerate
small joint distributions, check gradients, and reload the policy.

Native `structured_offers` is incomplete at priority; canonical DecisionFrame is
currently action-aligned. Preserve that ABI. Extend the native structured bridge
with a complete legal projection and a read-only lowering of one submission to
canonical revision-bound Commands on an exact clone. Reuse its existing lowerer.
Do not infer grouping from consecutive equal actors. Only native atomic attacker
and single-target cast offers group; blockers/payments remain separate authority
observations until managym supplies an atomic representation.

The Agent owns an optional autoregressive ragged decoder; fixed candidate order
and cardinality masks give one unique encoding of each unordered selection.
Teacher-forced joint log probability sums normalized conditional log probabilities.
A prefix recurrent state conditions later choices; no engine stepping or new
observation occurs inside decoding. Completed games are the collection/update
boundary, with per-seat credit, terminal rewards, no optimizer step inside a
compound command, and explicit outcome versus bootstrapped estimators.
Sequential/grouped optimization share the same decoder and native Commands;
sequential treats decoder factors as credit steps, grouped sums them. Report
both factor and underlying engine counts plus elapsed latency and complete games.

Ataraxos primary paper (Nature s41586-026-11036-y, methods/Extended Data Fig. 1)
uses a decoder-only setup policy with prefix outcome values and Monte Carlo
returns. This implementation uses a small recurrent decoder and scalar values;
comparison of outcome/bootstrapped credit is a treatment, not transferred evidence.

Existing GameSession uses action-aligned semantic Commands and records explicit
choices separately from automatic passes; Trace carries private canonical replay.
Serving lowers a sampled native compound to that existing stream. No new session,
identity authority, or claim of crash-durable training/resume is introduced.

No deletion targets: additive policy capability. No expensive scoring or extra
paid compute; scientific multi-seed comparison needs a separate frozen budget.

Implementation reconciliation: native lowering preserves the existing canonical
ABI; default Agent serialization omits the new disabled field so old recipes do
not gain a new identity. Full-game collection stores rejected partial evidence
on failure. Sequential/grouped arms share the recurrent decoder and differ in
credit units; all factors, including forced factors, count in sequential traces.
Gamma=1 is fixed in recipes. Complete blockers/payments remain separate native
observations, and scientific comparison is explicitly unallocated. No child
Intelligence memories exist in this checkout.

Focused check: `OMP_NUM_THREADS=1 uv run pytest` over compound/structured/regime/
objective/study checks passed after the registration fixture compatibility fix;
new incomplete-attempt check passed; debug compound lowering passed all 64
attacker subsets. Two four-arm, one-threaded workflow smokes completed (268/224 s), each with 56 exact-replayed arena games and unchanged offline reports.

Sync check (2026-10-04): merged main locally; compound reload, categorical values, belief dependencies and all three belief reload variants passed after rebuilding the stale native extension.
