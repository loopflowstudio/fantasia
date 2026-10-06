# ETU-108 remaining work

Research and benchmark preparation now live in docs/distributed-rl.md and
experiments/runners/distributed_{benchmark,workloads}.py. The earlier claim of
missing value-token support was wrong: the fixed recipe selects historical mean;
the ordinary model already implements token aggregation and additional attention.

Mini remains unresolved after the prior single access attempt. Torch/native
workloads remain unexecuted without a local environment and priority-safe capacity.
No access retry, training, prototype acceptance or Task completion is part of this
delivery. Placement, lag and aggregate execution budget remain future decisions.
Delete the scratch-only copies; durable owners above are the sole maintained path.

Checks: six unittest supervisor fixtures, focused Ruff lint/format, Python 3.12 AST and diff whitespace passed; Torch/native workloads deferred.
