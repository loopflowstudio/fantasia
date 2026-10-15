"""Read retained screening evidence and calculate bounded categorical examples.

This is an offline analysis script, not a training/evaluation runner. Constructed
offer sets are arithmetic examples, never native states or checkpoint outputs.
"""

from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import math
from pathlib import Path
import signal
import sys
import time
from typing import Any


@dataclass(frozen=True)
class Probe:
    name: str
    families: tuple[str, ...]
    policy: tuple[float, ...]
    behavior: tuple[float, ...]


def entropy(probabilities: tuple[float, ...]) -> float:
    return -sum(p * math.log(p) for p in probabilities if p > 0)


def kl(policy: tuple[float, ...], target: tuple[float, ...]) -> float:
    assert len(policy) == len(target)
    return sum(p * math.log(p / q) for p, q in zip(policy, target) if p > 0)


def mass(families: tuple[str, ...], p: tuple[float, ...]) -> dict[str, float]:
    return {f: sum(v for k, v in zip(families, p) if k == f) for f in dict.fromkeys(families)}


def describe(probe: Probe) -> dict[str, object]:
    counts = Counter(probe.families)
    n = len(probe.families)
    uniform = (1 / n,) * n
    structured = tuple(1 / (len(counts) * counts[f]) for f in probe.families)
    for p in (probe.policy, probe.behavior, uniform, structured):
        assert len(p) == n and all(v > 0 for v in p)
        assert math.isclose(sum(p), 1)
    grouped = tuple(mass(probe.families, probe.policy).values())
    h = entropy(probe.policy)
    assert math.isclose(kl(probe.policy, uniform), math.log(n) - h, abs_tol=1e-12)
    return {
        "name": probe.name, "constructed_not_native": True,
        "families": probe.families, "policy": probe.policy, "behavior": probe.behavior,
        "encoded_uniform": uniform, "action_type_uniform": structured,
        "policy_family_mass": mass(probe.families, probe.policy),
        "uniform_family_mass": mass(probe.families, uniform),
        "structured_family_mass": mass(probe.families, structured),
        "entropy_nats": h, "family_entropy_nats": entropy(grouped),
        "within_family_entropy_nats": h - entropy(grouped),
        "kl_policy_behavior": kl(probe.policy, probe.behavior),
        "kl_behavior_policy": kl(probe.behavior, probe.policy),
        "kl_policy_uniform": kl(probe.policy, uniform),
        "kl_policy_structured": kl(probe.policy, structured),
    }


def main() -> None:
    signal.alarm(60)
    start = time.perf_counter()
    probes = [
        Probe("priority", ("cast",) * 4 + ("land", "pass"), (.1, .1, .1, .1, .1, .5), (1 / 6,) * 6),
        Probe("optional-target", ("target",) * 3 + ("decline",), (.2, .2, .2, .4), (.25,) * 4),
        Probe("waterbend", ("tap",) * 3 + ("pay",), (.2, .2, .2, .4), (.25,) * 4),
        Probe("attacker-aliased-features", ("declare-attacker",) * 2, (.5, .5), (.5, .5)),
        Probe("learn", ("lesson",) * 2 + ("discard",) * 3 + ("decline",), (.1, .1, .1, .1, .1, .5), (1 / 6,) * 6),
        Probe("forced-pass", ("pass",), (1.,), (1.,)),
        Probe("hypothetical-equivalent-encodings", ("same-semantic-choice",) * 4, (.25,) * 4, (.25,) * 4),
        Probe("unchanged-sampled-ratio", ("sampled", "unsampled-a", "unsampled-b"), (.2, .79, .01), (.2, .4, .4)),
    ]
    assert len(probes) <= 8
    path = Path("experiments/data/etu105/filter-scope-mini.json.gz")
    with gzip.open(path, "rb") as stream:
        raw = stream.read(64 * 1024 * 1024 + 1)
    assert len(raw) <= 64 * 1024 * 1024
    # Local JSON boundary: this frozen report's nested legacy schema is retained
    # verbatim; validate the containers needed for extraction, not a new schema.
    evidence: dict[str, Any] = json.loads(raw)
    assert isinstance(evidence, dict) and isinstance(evidence["runs"], list)
    identity_keys = (
        "world", "action_abi_sha256", "observation_abi_sha256", "matchup_sha256",
        "content_digest", "content_manifest_sha256", "content_schema_version",
        "engine_extension_sha256", "engine_source_sha256", "training_source_sha256",
        "source_commit", "torch", "architecture",
    )
    runs = []
    for run in evidence["runs"]:
        stages = run["stages"]
        assert isinstance(stages, list) and len(stages) == 2
        runs.append({
            "id": run["id"], "seed": run["seed"], "regime_digest": run["regime_digest"],
            "status": run["status"], "seconds": run["seconds"],
            "selected_artifact": run["selected_artifact"],
            "selected_artifact_exists_here": Path(run["selected_artifact"]["path"]).is_file(),
            "identities": {k: run["identities"].get(k) for k in identity_keys},
            "learning": run["regime"]["stages"][0]["learning"],
            "observation": run["regime"]["observation"],
            "agent": run["regime"]["agent"],
            "diagnostic_count": sum(len(s["diagnostics"]) for s in stages),
            "last_diagnostic": stages[-1]["diagnostics"][-1],
        })
    backups: list[dict[str, Any]] = json.loads(Path("experiments/data/etu105/local-backup.json").read_text())
    paths = [
        "scratch/regularization-probe.py", str(path),
        "experiments/data/etu105/analysis.json", "experiments/data/etu105/closeout.json",
        "manabot/training/ataraxos.py", "manabot/training/objectives.py",
        "manabot/training/references.py", "manabot/model/policy_distribution.py",
        "managym/src/agent/observation_encoder.rs", "managym/src/agent/observation.rs",
    ]
    output = {
        "scope": "offline evidence extraction and constructed distributions; no model execution",
        "python": sys.version.split()[0], "source_commit": "9576dc40ef486966246e20d9fdf58e5d741f1c40",
        "native_runtime": None, "new_checkpoint": None, "training_steps": 0,
        "paid_resource_spend": 0, "owned_host_dollar_cost": None,
        "file_sha256": {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths},
        "constructed_probes": [describe(p) for p in probes],
        "retained_runs": runs,
        "local_backup_receipt": {"entries": len(backups), "present_in_this_checkout": sum(Path(b["local"]).is_file() for b in backups)},
        "lr_upper_clamp_last_iteration": math.floor((.5 / 1e-4) ** (1 / 1.1)),
        "read_bytes_decompressed": len(raw), "elapsed_seconds": time.perf_counter() - start,
        "earlier_inspection_seconds": [.059551458922214806, .06024995900224894],
        "failures": [],
    }
    destination = Path("scratch/regularization-diagnostics.json")
    temporary = destination.with_suffix(".tmp")
    temporary.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    temporary.replace(destination)
    print(json.dumps({
        "elapsed_seconds": output["elapsed_seconds"], "backups": output["local_backup_receipt"],
        "lr_upper_clamp_last_iteration": output["lr_upper_clamp_last_iteration"],
        "identities": runs[0]["identities"],
        "endpoints": [{"seed": r["seed"], "scope": r["learning"]["filter_scope"], "checkpoint": r["selected_artifact"]["sha256"]} for r in runs],
        "diagnostics": [{k: p[k] for k in ("name", "entropy_nats", "kl_policy_behavior", "kl_behavior_policy", "kl_policy_uniform", "kl_policy_structured")} for p in output["constructed_probes"]],
    }, indent=2))


if __name__ == "__main__":
    main()
