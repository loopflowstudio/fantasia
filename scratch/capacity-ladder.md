# ETU-102 narrow implementation plan — completed locally

Jack Heart requested independent capacity software delivery and authorized publication
and landing on 2026-10-05. Audit at be6260d9 found PRs 222/223 already supplied
AgentSpec width/head/depth validation, baseline-preserving layers, with_capacity
and the three model_capacity.regimes examples. They remain configuration owners.

Implemented versioned derived identity, component/total/trainable counts, run and
checkpoint receipts, strict present-receipt admission with unchanged historical
admission, real-observation legal-mask/reload tests and bounded calibration tooling.
Delete — do not maintain: none; no replacement schema or helper was introduced.

The one capacity attempt at 90c55627 completed in 212.56 seconds, six admitted raw
exports and 40 replayed games. Counts: 138434 / 188418 / 712706. High host load
precludes scaling claims. Earlier default-calibration timeout remains archived;
per-game allowance increased to 30 seconds without increasing total cap. Initial
native-extension absence and a test-import failure were repaired. All conclusions
and limits now live in docs/training-calibration.md and wave/intelligence/MEMORY.md.

Check: focused/gate suites passed (101 distinct checks, one optional notebook skip),
including the two affected reruns; lint/format and diff checks passed. Native build
completed; no Rust source changed, debug matrix remains CI-owned.

Remaining: publish and request landing/Task completion; verified merge depends on CI.
No scientific study, paid compute or ETU-91 modification occurred.
