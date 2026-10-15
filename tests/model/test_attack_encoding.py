"""Flat attack/decline choices remain distinguishable from encoder to learning."""

import numpy as np
import pytest
import torch

from manabot.env import ObservationSpace
from manabot.infra.hypers import AgentSpec
from manabot.model.agent import Agent
import managym


def _attack_root() -> tuple[managym.Env, managym.Observation]:
    env = managym.Env(seed=815, skip_trivial=False)
    raw, _ = env.reset(
        [
            managym.PlayerConfig("a", {"Gray Ogre": 40}),
            managym.PlayerConfig("b", {"Gray Ogre": 40}),
        ]
    )
    env.scenario_clear_hand(0)
    env.scenario_clear_hand(1)
    env.scenario_force_battlefield(0, "Gray Ogre", ready=True)
    raw = env.scenario_refresh()
    for _ in range(30):
        if (
            raw.action_space.action_space_type
            == managym.ActionSpaceEnum.DECLARE_ATTACKER
        ):
            return env, raw
        action = next(
            i
            for i, option in enumerate(raw.action_space.actions)
            if option.action_type == managym.ActionEnum.PRIORITY_PASS_PRIORITY
        )
        raw, _, _, _, _ = env.step(action)
    raise AssertionError("fixture did not reach an attacker declaration")


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("attack", [False, True])
def test_flat_policy_can_learn_either_declaration(native: bool, attack: bool) -> None:
    torch.set_num_threads(1)
    torch.manual_seed(815)
    env, raw = _attack_root()
    space = ObservationSpace()
    encoded = space.encode(raw)
    encoded_native = env.encode_observation(raw)
    for key in encoded:
        np.testing.assert_array_equal(encoded[key], encoded_native[key])
    options = raw.action_space.actions
    assert [option.declared for option in options] == [True, False]
    rows = encoded["actions"][:2]
    assert rows.shape == (2, 18)
    np.testing.assert_array_equal(rows[0, :16], rows[1, :16])
    np.testing.assert_array_equal(
        encoded["action_focus"][0], encoded["action_focus"][1]
    )
    np.testing.assert_array_equal(rows[:, 16], [1, -1])
    np.testing.assert_array_equal(rows[:, 17], [1, 1])
    np.testing.assert_array_equal(encoded["actions"][2:], 0)

    obs = {
        key: torch.as_tensor(value).unsqueeze(0)
        for key, value in (encoded_native if native else encoded).items()
    }
    agent = Agent(
        space, AgentSpec(hidden_dim=16, num_attention_heads=2, attention_on=False)
    )
    optimizer = torch.optim.Adam(agent.parameters(), lr=0.01)
    target = torch.tensor([0 if attack else 1])
    # This is a representability/gradient test on a real root, not game-strength
    # training. The old identical rows cannot fit either label above 50 percent.
    for _ in range(40):
        logits, _ = agent(obs)
        loss = torch.nn.functional.cross_entropy(logits, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        logits, _ = agent(obs)
    assert logits.softmax(-1)[0, target.item()] > 0.95
