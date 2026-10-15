"""Bounded search for choice aliasing in native authored games.

Collect replayable legal states, group actions by public descriptors (never
instance IDs), and fit a few shared policies to opposite artificial preferences.
Structural violations and finite-budget fit misses are reported separately.
This experiment driver measures capacity, not strategy or held-out strength.
"""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import random
import subprocess
import time
from typing import Literal

import torch

from manabot.env import ObservationSpace
from manabot.infra.hypers import AgentSpec
from manabot.model import Agent
from manabot.verify.action_cases import encode, reorder_objects, reorder_offers
import managym

PACK = "ur-lessons-vs-gw-allies"
KEYWORDS = (
    "flying",
    "reach",
    "haste",
    "flash",
    "vigilance",
    "trample",
    "first_strike",
    "double_strike",
    "deathtouch",
    "lifelink",
    "defender",
    "menace",
    "hexproof",
)
Arm = Literal["generic", "semantic", "generic_no_attention"]
ARMS: tuple[Arm, ...] = ("generic", "semantic", "generic_no_attention")


@dataclass
class Case:
    name: str
    seed: int
    swapped: bool
    trace: list[int]
    digest: str
    family: int
    groups: tuple[list[int], list[int]]
    signatures: list[str]
    raw_json: str
    obs: dict[str, torch.Tensor]
    successors: tuple[str, str]

    def receipt(self) -> dict[str, object]:
        return {key: value for key, value in asdict(self).items() if key != "obs"}


def _keywords(value: managym.Keywords) -> list[bool]:
    return [bool(getattr(value, key)) for key in KEYWORDS]


def _signatures(raw: managym.Observation) -> list[str]:
    """Conservative observable classes; equal copies share probability mass.

    The descriptor is independent of the tensor encoder. Equal descriptors do
    not prove full game-theoretic equivalence; relational distinctions outside
    this descriptor are explicitly outside the search's coverage.
    """
    objects: dict[int, list[object]] = {
        raw.agent.id: ["player", "self"],
        raw.opponent.id: ["player", "opponent"],
    }
    for role, cards, permanents in (
        ("self", raw.agent_cards, raw.agent_permanents),
        ("opponent", raw.opponent_cards, raw.opponent_permanents),
    ):
        for card in cards:
            objects[card.id] = [
                "card",
                role,
                card.registry_key,
                int(card.zone),
                card.power,
                card.toughness,
                card.is_token,
                card.is_ally,
                card.is_lesson,
                card.ward_cost,
                card.kicker_cost,
                _keywords(card.keywords),
            ]
        for permanent in permanents:
            objects[permanent.id] = [
                "permanent",
                role,
                permanent.registry_key,
                permanent.tapped,
                permanent.damage,
                permanent.is_summoning_sick,
                permanent.plus1_counters,
                permanent.cant_be_blocked_this_turn,
                permanent.power,
                permanent.toughness,
                permanent.is_animated,
                permanent.has_exile_link,
                _keywords(permanent.keywords),
            ]
    for card in raw.agent_sideboard:
        objects[card.candidate_id] = ["outside", "self", card.registry_key]
    # Unknown references are errors, not labels derived from arbitrary IDs.
    return [
        json.dumps(
            [
                int(action.action_type),
                action.declared,
                action.mode_index,
                action.ability_index,
                [objects[index] for index in action.focus],
            ],
            separators=(",", ":"),
        )
        for action in raw.action_space.actions
    ]


def _write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def _collect(
    out: Path, round_index: int, deadline: float
) -> tuple[list[Case], Counter[str], list[dict[str, object]]]:
    rng = random.Random(50_000 + round_index)
    buckets: dict[int, list[Case]] = defaultdict(list)
    counts: Counter[str] = Counter()
    findings: list[dict[str, object]] = []
    # Eight whole-game prefixes per round; both seats are visited naturally.
    for game in range(8):
        seed = 50_000 + round_index * 8 + game
        swapped = bool(game % 2)
        configs = [
            managym.authored_deck_setup(PACK, key)
            for key in ("ur_lessons", "gw_allies")
        ]
        if swapped:
            configs.reverse()
        env = managym.Env(seed=seed, skip_trivial=False)
        raw, _ = env.reset(configs)
        trace: list[int] = []
        for step in range(1200):
            if time.perf_counter() >= deadline:
                break
            actions = raw.action_space.actions
            if not actions or raw.game_over:
                counts["terminal_games"] += 1
                break
            family = int(raw.action_space.action_space_type)
            counts[f"visited_family_{family}"] += 1
            if len(actions) > 1:
                try:
                    signatures = _signatures(raw)
                    groups: dict[str, list[int]] = defaultdict(list)
                    for index, signature in enumerate(signatures):
                        groups[signature].append(index)
                    if len(groups) > 1:
                        obs = encode(env, raw)
                        assert int(obs["actions_valid"].sum()) == len(actions), (
                            "legal mask count"
                        )
                        for index, action in enumerate(actions):
                            assert (
                                obs["action_focus"][0, index, : len(action.focus)] >= 0
                            ).all(), "unresolved focus"
                        # Reverse native offers before running both encoders.
                        space, original = raw.action_space, actions
                        space.actions = original[::-1]
                        raw.action_space = space
                        try:
                            reversed_obs = encode(env, raw)
                        finally:
                            space.actions = original
                            raw.action_space = space
                        expected = reorder_offers(
                            obs, torch.arange(len(actions) - 1, -1, -1)
                        )
                        for key in obs:
                            torch.testing.assert_close(
                                reversed_obs[key], expected[key], rtol=0, atol=0
                            )
                        counts[f"audited_family_{family}"] += 1
                        keys = sorted(groups)
                        selected = (groups[keys[0]], groups[keys[-1]])
                        # Reservoir sampling within each family avoids priority dominance.
                        seen = counts[f"audited_family_{family}"]
                        slot = rng.randrange(seen)
                        if len(buckets[family]) < 6 or slot < 6:
                            root = env.state_digest()
                            left, right = env.clone_env(), env.clone_env()
                            left.step(selected[0][0])
                            right.step(selected[1][0])
                            assert env.state_digest() == root, "clone mutated root"
                            case = Case(
                                f"{seed}-{step}",
                                seed,
                                swapped,
                                trace.copy(),
                                root,
                                family,
                                selected,
                                signatures,
                                raw.toJSON(),
                                obs,
                                (left.state_digest(), right.state_digest()),
                            )
                            if len(buckets[family]) < 6:
                                buckets[family].append(case)
                            else:
                                buckets[family][slot] = case
                except Exception as error:
                    finding = {
                        "stage": "native_audit",
                        "seed": seed,
                        "swapped": swapped,
                        "trace": trace.copy(),
                        "family": family,
                        "error": f"{type(error).__name__}: {error}",
                        "raw": raw.toJSON(),
                    }
                    findings.append(finding)
                    # Keep the first 20 detailed errors per round; count every occurrence.
                    counts["native_errors"] += 1
                    if len(findings) > 20:
                        findings.pop()
            # Encourage spell/combat exposure without using an expert or hidden state.
            weights = [4 if int(a.action_type) in {0, 1, 6} else 1 for a in actions]
            index = rng.choices(range(len(actions)), weights=weights, k=1)[0]
            trace.append(index)
            try:
                raw, _, done, truncated, _ = env.step(index)
            except Exception as error:
                findings.append(
                    {
                        "stage": "native_step",
                        "seed": seed,
                        "swapped": swapped,
                        "trace": trace.copy(),
                        "error": f"{type(error).__name__}: {error}",
                    }
                )
                break
            if done or truncated:
                counts["terminal_games"] += int(done)
                break
        else:
            counts["step_capped_games"] += 1
    # Round-robin families so rare decision types get shared-fit slots.
    cases = [
        bucket[index]
        for index in range(6)
        for _, bucket in sorted(buckets.items())
        if index < len(bucket)
    ][:32]
    out.mkdir(parents=True, exist_ok=True)
    _write_json(out / "cases.json", [case.receipt() for case in cases])
    _write_json(out / "native-findings.json", findings)
    torch.save({case.name: case.obs for case in cases}, out / "observations.pt")
    return cases, counts, findings


def _spec(arm: Arm) -> AgentSpec:
    return AgentSpec(
        hidden_dim=32,
        num_attention_heads=2,
        attention_feedforward_dim=64,
        attention_on=arm != "generic_no_attention",
        semantic_pack=PACK if arm == "semantic" else None,
    )


def _fit(
    out: Path, cases: list[Case], arm: Arm, preference: int, seed: int, deadline: float
) -> dict[str, object]:
    started = time.perf_counter()
    torch.manual_seed(seed)
    spec = _spec(arm)
    agent = Agent(ObservationSpace(), spec)
    batch = {key: torch.cat([case.obs[key] for case in cases]) for key in cases[0].obs}
    selected = torch.zeros_like(batch["actions_valid"], dtype=torch.bool)
    pair = selected.clone()
    for row, case in enumerate(cases):
        selected[row, case.groups[preference]] = True
        pair[row, case.groups[0] + case.groups[1]] = True
    optimizer = torch.optim.Adam(agent.parameters(), lr=0.003)
    with torch.no_grad():
        initial, _ = agent(batch)
    completed_updates = 0
    for _ in range(240):
        if time.perf_counter() >= deadline:
            return {
                "arm": arm,
                "preference": preference,
                "seed": seed,
                "status": "budget_exhausted",
                "updates": completed_updates,
            }
        logits, _ = agent(batch)
        # Conditional group likelihood isolates whether this pair is separable;
        # other legal actions remain in the forward pass but are not negatives.
        normalizer = logits.masked_fill(~pair, -torch.inf).logsumexp(-1)
        chosen = logits.masked_fill(~selected, -torch.inf).logsumexp(-1)
        loss = (normalizer - chosen).mean()
        if not torch.isfinite(loss):
            raise ValueError("nonfinite loss")
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        completed_updates += 1
    agent.eval()
    path = out / f"{arm}-{preference}.pt"
    torch.save(
        {"state_dict": agent.state_dict(), "spec": spec.model_dump(), "seed": seed},
        path,
    )
    restored = Agent(ObservationSpace(), spec)
    restored.load_state_dict(torch.load(path, weights_only=True)["state_dict"])
    restored.eval()
    scores: list[dict[str, object]] = []
    with torch.no_grad():
        logits, values = agent(batch)
        reloaded, restored_values = restored(batch)
        reload_error = max(
            float((logits - reloaded).abs().max()),
            float((values - restored_values).abs().max()),
        )
        for row, case in enumerate(cases):
            obs = case.obs
            single, value = restored(obs)
            p = single.softmax(-1)
            group = case.groups[preference]
            union = case.groups[0] + case.groups[1]
            probability = float(p[0, group].sum() / p[0, union].sum())
            initial_row = initial[row].softmax(-1)
            before = float(initial_row[group].sum() / initial_row[union].sum())
            count = int(obs["actions_valid"].sum())
            order = torch.randperm(
                count, generator=torch.Generator().manual_seed(seed + row)
            )
            shuffled, _ = restored(reorder_offers(obs, order))
            objects, _ = restored(reorder_objects(obs))
            errors = {
                "batch": max(
                    float((single[0] - logits[row]).abs().max()),
                    float((value[0] - values[row]).abs()),
                ),
                "offer": float(
                    (shuffled.softmax(-1)[0, :count] - p[0, order]).abs().max()
                ),
                "object": float((objects.softmax(-1) - p).abs().max()),
                "padding_mass": float(p[obs["actions_valid"] == 0].sum()),
                "reload": reload_error,
            }
            scores.append(
                {
                    "case": case.name,
                    "family": case.family,
                    "initial": before,
                    "conditional_probability": probability,
                    "fit_passed": probability >= 0.95,
                    "errors": errors,
                    "invariants_passed": max(errors.values()) <= 1e-4,
                }
            )
    return {
        "arm": arm,
        "preference": preference,
        "seed": seed,
        "status": "completed",
        "updates": completed_updates,
        "seconds": time.perf_counter() - started,
        "checkpoint": path.name,
        "scores": scores,
    }


def run(out: Path, seconds: float) -> None:
    out.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    started = time.perf_counter()
    cpu_started = time.process_time()
    deadline = started + seconds
    rounds: list[dict[str, object]] = []
    result: dict[str, object] = {
        "protocol": "learnability-search-1",
        "source": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "world": managym.WORLD_VERSION,
        "torch": torch.__version__,
        "native_sha256": hashlib.sha256(
            Path(managym._managym.__file__).read_bytes()
        ).hexdigest(),
        "seconds_budget": seconds,
        "updates_per_fit": 240,
        "threshold": 0.95,
        "invariance_tolerance": 1e-4,
        "arms": ARMS,
        "rounds": rounds,
        "status": "running",
    }
    try:
        round_index = 0
        while time.perf_counter() < deadline:
            round_out = out / f"round-{round_index:03d}"
            cases, counts, findings = _collect(round_out, round_index, deadline)
            fits: list[dict[str, object]] = []
            record: dict[str, object] = {
                "round": round_index,
                "counts": dict(counts),
                "cases": len(cases),
                "native_findings": len(findings),
                "fits": fits,
            }
            rounds.append(record)
            _write_json(out / "result.json", result)
            # Rotate starting configuration to balance coverage at the deadline.
            arms = ARMS[round_index % len(ARMS) :] + ARMS[: round_index % len(ARMS)]
            for arm in arms:
                for preference in (0, 1):
                    if not cases or time.perf_counter() >= deadline:
                        break
                    try:
                        fit = _fit(
                            round_out,
                            cases,
                            arm,
                            preference,
                            1000 + round_index,
                            deadline,
                        )
                    except Exception as error:
                        fit = {
                            "arm": arm,
                            "preference": preference,
                            "status": "error",
                            "error": f"{type(error).__name__}: {error}",
                        }
                    fits.append(fit)
                    _write_json(out / "result.json", result)
                    score_rows = fit.get("scores", [])
                    assert isinstance(score_rows, list)
                    print(
                        json.dumps(
                            {
                                "round": round_index,
                                "cases": len(cases),
                                "arm": arm,
                                "preference": preference,
                                "status": fit["status"],
                                "fit_misses": sum(
                                    not s["fit_passed"] for s in score_rows
                                ),
                                "invariant_failures": sum(
                                    not s["invariants_passed"] for s in score_rows
                                ),
                                "elapsed": round(time.perf_counter() - started, 1),
                            }
                        ),
                        flush=True,
                    )
            round_index += 1
        result["status"] = "completed_budget"
    except BaseException as error:
        result["status"] = "error"
        result["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        result["wall_seconds"] = time.perf_counter() - started
        result["cpu_seconds"] = time.process_time() - cpu_started
        _write_json(out / "result.json", result)
        (out / "report.md").write_text(
            f"# Learnability exploration\n\nStatus: {result['status']}\n\n"
            f"Wall: {result['wall_seconds']:.1f}s; CPU: {result['cpu_seconds']:.1f}s.\n\n"
            "See result.json for per-case results; fit misses are candidates, not confirmed defects.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=1800)
    args = parser.parse_args()
    if not 0 < args.seconds <= 1800:
        parser.error("seconds must be in (0, 1800]")
    run(args.out, args.seconds)


if __name__ == "__main__":
    main()
