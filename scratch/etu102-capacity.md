# Capacity compression

The merged AgentSpec/with_capacity path remains the sole model configuration
owner. No obsolete implementation needs deletion. Calibration shares its canonical
run lookup between probes and reporting; the resolved plan owns the probe deadline,
and probe receipts record the loop counts and collector batch size actually used.
Architecture hashes, model equations, checkpoint admission and the frozen ladder
are unchanged. ETU-91 and retained evidence remain untouched.

`uv run pytest tests/training/test_calibration.py tests/model/test_capacity.py -q` — 14 passed in 31.14 s; focused Ruff and diff checks passed. Broader acceptance remains with gate/CI; no capacity study was run.
