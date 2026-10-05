"""The value factorial freezes one learning rule and independent output heads."""

from pydantic import TypeAdapter

from experiments.runners.run_value_models import smoke_plan
from experiments.runners.training_protocol import ResolvedStudy
from manabot.arena.models import PlayerRegistration
from manabot.training.models import TrainingRegime, TrainSelfPlay


def test_value_factorial_protocol() -> None:
    plan = smoke_plan()
    assert ResolvedStudy.model_validate_json(plan.model_dump_json()) == plan
    assert len(set(plan.protocol.regime_digests)) == 8
    recipes = [TrainingRegime.model_validate(row) for row in plan.recipes]
    assert {
        (r.agent.value_aggregation, r.agent.attention_layers, r.agent.value_kind)
        for r in recipes
    } == {
        (aggregation, depth, kind)
        for aggregation, depth in (
            ("historical_mean", 1),
            ("masked_mean", 1),
            ("value_token", 1),
            ("value_token", 2),
        )
        for kind in ("scalar", "categorical_wdl")
    }
    for recipe in recipes:
        assert recipe.agent.hidden_dim == 64
        assert recipe.agent.num_attention_heads == 4
        assert recipe.wall_seconds == 60
        for stage in recipe.stages:
            assert isinstance(stage, TrainSelfPlay)
            assert stage.learning.gradient == "ataraxos_move"
            assert stage.streams * stage.transitions * stage.updates == 256
            player_id = TypeAdapter(
                PlayerRegistration.model_fields["player_id"].rebuild_annotation()
            )
            for variant in ("raw", "ema"):
                player_id.validate_python(f"{recipe.id}-1061-{stage.id}-{variant}")
