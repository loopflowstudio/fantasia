"""Throwaway probe: forward and train-step rates for a generic transformer encoder
at several sizes, as a stand-in until manabot can build deep models."""
import sys, time, torch, torch.nn as nn
dev = sys.argv[1]
def bench(depth, width, ff, tokens, batch, amp):
    layer = nn.TransformerEncoderLayer(width, 8 if width >= 256 else 4, ff, batch_first=True, norm_first=True)
    m = nn.Sequential(nn.TransformerEncoder(layer, depth), nn.Linear(width, 1)).to(dev)
    n = sum(p.numel() for p in m.parameters())
    opt = torch.optim.Adam(m.parameters(), 1e-4)
    x = torch.randn(batch, tokens, width, device=dev)
    def run(train):
        def step():
            with torch.autocast(dev, dtype=torch.bfloat16, enabled=amp):
                loss = m(x).float().mean()
            if train:
                opt.zero_grad(); loss.backward(); opt.step()
        with torch.set_grad_enabled(train):
            step()
            if dev == "cuda": torch.cuda.synchronize()
            t = time.perf_counter(); k = 0
            while time.perf_counter() - t < 2: step(); k += 1
            if dev == "cuda": torch.cuda.synchronize()
            return k * batch / (time.perf_counter() - t)
    try:
        f = run(False); tr = run(True)
        mem = torch.cuda.max_memory_allocated() / 2**30 if dev == "cuda" else 0
        print(f"{depth}x{width} ff{ff} tok{tokens} b{batch} amp{int(amp)} params={n/1e6:.1f}M fwd={f:,.0f}/s train={tr:,.0f}/s peakGB={mem:.1f}", flush=True)
    except RuntimeError as e:
        print(f"{depth}x{width} tok{tokens} b{batch} FAILED {str(e)[:60]}", flush=True)
    if dev == "cuda": torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
for depth, width, ff in [(4, 256, 1024), (8, 384, 1536)]:
    for tokens in (64, 256):
        for batch, amp in ((256, False), (1536, False), (1536, True)):
            if dev == "cpu" and (batch > 256 or amp): continue
            bench(depth, width, ff, tokens, batch, amp)
