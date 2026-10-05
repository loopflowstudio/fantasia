# ETU-104 assumptions and boundaries

2026-10-05. Jack Heart approved implementation and landing. ETU-106 PR #222
at a371af46 is integrated through lf sync; its review dependency is resolved.
The capacity examples use delivered width/depth fields. Feedforward width and
normalization remain model-owned; no additional architecture or allocation is
inferred from ETU-102. History, transfer tooling and ETU-91 remain out of scope.

The Python AgentHypers symbol is replaced by AgentSpec throughout executable
consumers. Serialized agent_hypers dictionaries and checkpoint fields retain
their existing meanings; no compatibility alias or metadata rewrite is needed.
