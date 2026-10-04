"""Study evidence must preserve cost, cohort and artifact boundaries."""

import hashlib
import json

import pytest

from experiments.runners.training_protocol import EvaluationProtocol
from manabot.arena.models import canonical_sha256
from manabot.training.analysis import cost_comparison, verify_saved_inputs


def point(name, seconds, score):
    return dict(
        regime=name,
        seed=197,
        training_seconds=seconds,
        score=score,
        checkpoint={"path": f"{name}-{seconds}"},
        complete=True,
        opponent="random-smoke-anchor",
    )


def test_shared_cost_never_uses_future_checkpoint_or_backfills_collection():
    rows = [
        point("a", 10, 0.2),
        point("a", 20, 0.9),
        point("b", 5, 0.4),
        point("b", 15, 0.8),
    ]
    result = cost_comparison(rows)
    assert (result["start_seconds"], result["end_seconds"]) == (10, 15)
    assert [r["score"] for r in result["rows"]] == [0.2, 0.8]
    assert [r["mean_score"] for r in result["rows"]] == [0.2, 0.4]
    assert (
        cost_comparison([point("a", 20, 0.9), point("b", 5, 0.4)])["status"]
        == "unavailable"
    )


def test_shared_cost_integrates_only_observed_intervals():
    rows = [
        point("a", 2, 0.1),
        point("a", 8, 0.6),
        point("a", 14, 0.9),
        point("b", 5, 0.4),
        point("b", 12, 0.8),
    ]
    result = cost_comparison(rows)
    assert (result["start_seconds"], result["end_seconds"]) == (5, 12)
    assert result["rows"][0]["mean_score"] == pytest.approx((3 * 0.1 + 4 * 0.6) / 7)
    assert result["rows"][1]["mean_score"] == pytest.approx(0.4)


def test_failed_or_paired_measurements_cannot_enter_anchor_curve():
    bad = point("a", 1, 1)
    bad["complete"] = False
    paired = point("a", 2, 1)
    paired["opponent"] = "another-policy"
    assert cost_comparison([bad, paired])["status"] == "unavailable"


def test_raw_and_averaged_checkpoints_remain_separate_cost_curves():
    raw = [point("a", 10, 0.2), point("a", 20, 0.3)]
    averaged = [dict(row, variant="ema", score=0.8) for row in raw]
    result = cost_comparison(raw + averaged)
    assert {(r["variant"], r["score"]) for r in result["rows"]} == {
        ("raw", 0.3),
        ("ema", 0.8),
    }


def test_protocol_rejects_overlap_and_unbound_recipes():
    kwargs = dict(study="learning-speed", regime_digests=("a" * 64, "b" * 64))
    EvaluationProtocol(**kwargs)
    with pytest.raises(ValueError, match="disjoint"):
        EvaluationProtocol(**kwargs, anchor_deals=(910001,))
    with pytest.raises(ValueError, match="reserved"):
        EvaluationProtocol(**kwargs, paired_deals=(10197,))
    with pytest.raises(ValueError, match="every resolved"):
        EvaluationProtocol(study="ataraxos-ablations", regime_digests=("a" * 64,))


def test_offline_reporting_rejects_changed_checkpoint(tmp_path):
    checkpoint = tmp_path / "checkpoint"
    checkpoint.write_bytes(b"original")
    study = {
        "runs": [],
        "measurements": [
            {
                "checkpoint": {
                    "path": str(checkpoint),
                    "sha256": hashlib.sha256(b"original").hexdigest(),
                }
            }
        ],
    }
    verify_saved_inputs(tmp_path, study)
    checkpoint.write_bytes(b"changed")
    with pytest.raises(ValueError, match="checkpoint digest"):
        verify_saved_inputs(tmp_path, study)


def test_offline_reporting_rejects_changed_recipe(tmp_path):
    recipe = {"id": "frozen"}
    protocol = {"regime_digests": [canonical_sha256(recipe)]}
    (tmp_path / "protocol.json").write_text(json.dumps(protocol))
    (tmp_path / "recipes.json").write_text(json.dumps([recipe]))
    study = {
        "protocol_sha256": canonical_sha256(protocol),
        "runs": [],
        "measurements": [],
    }
    verify_saved_inputs(tmp_path, study)
    (tmp_path / "recipes.json").write_text('[{"id": "changed"}]')
    with pytest.raises(ValueError, match="recipe digest"):
        verify_saved_inputs(tmp_path, study)


def test_report_regeneration_preserves_metrics_without_training(tmp_path):
    pytest.importorskip("nbclient")
    from manabot.training.analysis import report

    study = dict(
        study="ataraxos-ablations",
        profile="smoke",
        status="failed",
        limits="Test fixture: no measured games",
        runs=[],
        comparisons=[
            dict(
                a="a",
                b="b",
                cutoff=0,
                evaluation_seconds=1,
                replay={"passed": False},
                trace=None,
                scheduled_games=4,
                rows=[
                    dict(
                        deal_seed=1,
                        leg=leg,
                        player_a_seat=0,
                        score_a=1,
                        failure=None,
                        terminated=True,
                        truncated=leg == 0,
                        replay_passed=leg != 1,
                    )
                    for leg in range(2)
                ],
            )
        ],
        measurements=[],
        error="Failure before training",
    )
    (tmp_path / "study.json").write_text(json.dumps(study))
    report(tmp_path)
    first = {
        name: (tmp_path / name).read_bytes()
        for name in ("metrics.json", "cost-comparison.json", "report.md")
    }
    report(tmp_path)
    assert first == {name: (tmp_path / name).read_bytes() for name in first}
    notebook = json.loads((tmp_path / "analysis.ipynb").read_text())
    assert all(
        c["execution_count"] is not None
        for c in notebook["cells"]
        if c["cell_type"] == "code"
    )
    rendered = first["report.md"].decode()
    assert "No completed measurements" in rendered
    assert "Unresolved-game bounds for A: [0.000, 1.000]" in rendered
    assert rendered.count("| unavailable | None |") == 2


def test_scientific_profile_requires_replicates_and_explicit_uncertainty():
    kwargs = dict(
        study="learning-speed",
        regime_digests=("a" * 64, "b" * 64),
        purpose="scientific",
        process_seconds=3600,
        cost_cutoffs_seconds=(600, 1200),
    )
    with pytest.raises(ValueError, match="three seeds"):
        EvaluationProtocol(**kwargs)
    protocol = EvaluationProtocol(
        **kwargs,
        training_seeds=(601, 1601, 2601),
        uncertainty="paired-seed-descriptive",
        anchors=("random", "scripted-greedy", "puct-64"),
        endpoint_paired_deals=(950001,),
        endpoint_anchor_deals=(960001,),
        endpoint_seed_pairs=tuple(
            (a, b) for a in (601, 1601, 2601) for b in (601, 1601, 2601)
        ),
    )
    assert len(protocol.training_seeds) == 3
    with pytest.raises(ValueError, match="900 seconds"):
        EvaluationProtocol(
            study="learning-speed",
            regime_digests=("a" * 64, "b" * 64),
            process_seconds=901,
        )


def test_cost_cutoffs_exclude_endpoint_and_future_weights():
    from manabot.training.analysis import cost_cutoffs

    rows = [
        point("a", 10, 0.2),
        point("a", 20, 0.9),
        point("b", 5, 0.3),
        point("b", 20, 0.4),
    ]
    rows.append(dict(point("a", 12, 1), phase="endpoint"))
    results = cost_cutoffs(rows, (1, 15, 25))
    assert results[0]["status"] == results[2]["status"] == "unavailable"
    assert [r["score"] for r in results[1]["rows"]] == [0.2, 0.3]


def test_uncertainty_clusters_training_seeds_and_four_leg_deals():
    from manabot.training.analysis import paired_uncertainty

    cells = [
        dict(
            a="a",
            b="b",
            cutoff=1,
            phase="endpoint",
            training_seed=a,
            b_training_seed=b,
            scheduled_games=8,
            replay={"passed": True},
            rows=[
                dict(
                    deal_seed=d,
                    score_a=a / 2,
                    failure=None,
                    terminated=True,
                    truncated=False,
                    replay_passed=True,
                )
                for d in (1000000, 1000001)
                for _ in range(4)
            ],
        )
        for a in range(3)
        for b in range(3)
    ]
    result = paired_uncertainty(cells)[0]
    assert result["status"] == "available"
    assert result["training_seeds"] == 3
    assert result["deal_blocks"] == 2
    assert result["score_a"] == 0.5
    assert "crossed" in result["method"]
    assert paired_uncertainty(cells[:3])[0]["status"] == "unavailable"
