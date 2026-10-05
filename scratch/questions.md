# ETU-104 unresolved review choices

2026-10-05. Jack Heart's framework review is pending. Recommendations are proposals:

- Prefer closed typed architecture specs and explicit builders over extending local
  switches indefinitely; choose the first coherent cutover scope.
- Start with bounded recent-event tokens. Persistent recurrence requires explicit
  per-viewer state, reset/cursor semantics and sequence training; defer that scope.
- Strict reload preserves function/world semantics; compatible transfer is a new
  run with explicit tensor mapping and initialization, never permissive loading.

Material working assumptions: no framework code before review; ETU-106's focused
value-token direction and independent capacity ladder may proceed. Existing
EvaluationProtocol gets a new versioned architecture-study discriminator later;
no frozen study is relabeled. The live ETU-106 Task was inspected, but its worker
was not launched or interrupted and no unpublished code was assumed to exist.

The later steer requests a separate human review-design Session. Human attendance
and approval remain unavailable here; artifact readiness is not that review.
