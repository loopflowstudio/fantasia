#!/usr/bin/env bash
# First-contact shakedown for a rented Linux GPU pod: build Etude from a clean
# clone the way CI does, then prove the GPU is visible and a CPU training smoke
# runs. Every step logs its wall time so setup cost is known before real runs.
set -euo pipefail

REF="${1:-main}"
WORK="${WORK:-/workspace}"
step() { echo; echo "=== $1 ($(date -u +%H:%M:%S)) ==="; }

step "host"
nproc; free -g | sed -n 2p; df -h "$WORK" | tail -1
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv

step "toolchains"
command -v cargo >/dev/null || curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

step "clone $REF"
cd "$WORK"
[ -d etude ] || git clone https://github.com/loopflowstudio/etude.git
cd etude && git fetch origin && git checkout "$REF" && git rev-parse HEAD

step "python environment"
time uv sync --python 3.12 --extra dev --extra play

step "managym extension"
time uv run --python 3.12 --extra play maturin develop --release \
  --features python --manifest-path managym/Cargo.toml

step "torch sees the GPU"
uv run python -c "
import torch
print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))
x = torch.randn(4096, 4096, device='cuda'); print((x @ x).sum().item())"

step "focused tests"
uv run --extra dev pytest tests/training tests/sim/test_net_opponent.py -q -x

echo; echo "shakedown complete"
