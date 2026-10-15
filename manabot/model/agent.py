"""
agent.py
Shared viewer-observation encoder, legal-action policy and scalar or WDL critic.

Agent.forward preserves the serving policy/value interface. Training uses
forward_distribution when it needs loss/draw/win logits rather than their mean.
"""

from typing import Dict, Literal, Optional, Tuple

import torch
import torch.nn as nn

# Local imports
from manabot.env import ObservationSpace
from manabot.env.observation import PERMANENT_DEFINITION_INDEX
from manabot.infra import AgentSpec
from manabot.infra.log import getLogger
from manabot.model.compound import CompoundDecoder, CompoundOutput
from manabot.model.recent_events import RecentEventEncoder
from manabot.sim.structured_policy import RaggedOfferBatch
import managym


class Agent(nn.Module):
    """
    Agent that:
      1. Encodes game objects with typed embeddings.
      2. Uses an attention mechanism to allow information exchange.
      3. Augments action representations with focus object information.
      4. Computes policy logits and a value estimate.

    Debug logging uses explicit category tags to help diagnose issues,
    such as why the model appears to always select the default action.
    """

    def __init__(self, observation_space: ObservationSpace, hypers: AgentSpec) -> None:
        super().__init__()
        self.observation_space = observation_space
        self.hypers = hypers
        # Scalar heads need the checkpoint's training-target declaration. WDL
        # means and compound prefix critics have architectural signed units.
        self.value_semantic: Literal["signed_outcome", "win_logit"] | None = (
            "signed_outcome"
            if hypers.value_kind == "categorical_wdl" or hypers.compound_decisions
            else None
        )
        self.logger = getLogger(__name__)

        # Extract dimensions from the observation encoder.
        enc = observation_space.encoder
        if hypers.recent_events and (
            hypers.semantic_pack is None or enc.hypers.policy_history_version != 1
        ):
            raise ValueError(
                "recent events require semantic_pack and policy_history_version=1"
            )
        if not hypers.recent_events and enc.hypers.policy_history_version != 0:
            raise ValueError(
                "history observation contract requires recent_events Agent"
            )
        player_dim = enc.player_dim
        card_dim = enc.card_dim
        # Definition IDs are categorical joins, never numeric permanent features.
        perm_dim = enc.permanent_dim - 1
        action_dim = enc.action_dim
