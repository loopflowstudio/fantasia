"""Positive-control engine outcomes and real collector boundary checks."""

import numpy as np
import torch

from experiments.runners.current_baseline import declaration
from manabot.env import Match, ObservationSpace, Reward
from manabot.env.target_practice import resolve_target, target_root
from manabot.infra.hypers import RewardHypers
from manabot.model.agent import Agent
from manabot.sim.net_opponent import SeatRoutedCollector, transition_gae


def test_targets_reverse_with_seat_and_resolve_in_engine() -> None:
    regime = declaration().resolve().cases[0].regime
    space = ObservationSpace(regime.observation)
    for seed in (118, 119):
        for seat in (0, 1):
            for action in (0, 1):
                env = target_root(Match(regime.match), space, seed, seat)
                assert resolve_target(env, action) == 1 - action


def test_real_collector_terminal_rewards_and_advantages() -> None:
    torch.set_num_threads(1)
    regime = declaration().resolve().cases[0].regime
    space = ObservationSpace(regime.observation)
    agent = Agent(space, regime.agent)
    collector = SeatRoutedCollector(space, Match(regime.match), Reward(RewardHypers()),
        num_envs=4, seed=118, root="lethal-target-v1")
    batch = collector.collect(agent, 4)
    assert batch.dones.all()
    expected = np.where(1 - batch.actions == np.arange(4) % 2, 1, -1)
    np.testing.assert_array_equal(batch.rewards, expected)
    advantages, returns = transition_gae(torch.tensor(batch.rewards),
        torch.zeros_like(torch.tensor(batch.values)), torch.tensor(batch.dones),
        torch.full((4,), 100.0), 1.0, 0.5)
    torch.testing.assert_close(advantages, torch.tensor(batch.rewards))
    torch.testing.assert_close(returns, torch.tensor(batch.rewards))
    assert np.all(batch.probabilities[:, :, 2:] == 0)
