"""Project private local-update targets into the existing advice schema.

This is a projection seam, not a live advisor registration. The endpoint still
requires its ordinary historical-root and exact artifact admission. Signed Q is
identified by method; it is not silently called a win probability.
"""

from collections.abc import Sequence

import numpy as np

from etude.advice import (
    AdvisorOfferEvidence,
    AdvisorScenarioEvidence,
    AvailableQuantity,
    BeliefNormalizationReceipt,
    UnavailableQuantity,
)
from manabot.sim.local_update import LocalUpdateReceipt


def local_update_scenario(
    receipt: LocalUpdateReceipt,
    belief: BeliefNormalizationReceipt,
    *,
    labels: Sequence[str],
) -> AdvisorScenarioEvidence:
    """Keep offers and mixing; exclude sampled hands, seeds and branch tapes."""
    if (
        belief.normalized_belief_sha256 != receipt.belief_digest
        or belief.space_identity != receipt.world_identity
        or belief.belief_model_id != receipt.belief_model
        or len(labels) != len(receipt.offer_ids)
    ):
        raise ValueError("advice belief or offers differ from the local update")
    unavailable = UnavailableQuantity(
        status="unavailable", reason="insufficient_world_coverage"
    )
    values = np.asarray([v if v is not None else 0.0 for v in receipt.values])
    return AdvisorScenarioEvidence(
        scenario_id=belief.scenario_id,
        belief=belief,
        condition_mass=receipt.condition_mass,
        support=belief.positive_support,
        sampled_worlds=max(receipt.allocation_counts),
        actions=[
            AdvisorOfferEvidence(
                offer_id=offer,
                label=labels[index],
                probability=receipt.target[index],
                visits=receipt.allocation_counts[index],
                q=unavailable
                if receipt.values[index] is None
                else AvailableQuantity(
                    status="available",
                    value=float(values[index]),
                    method="signed_frozen_policy_rollout_value/v1",
                ),
                robustness=unavailable,
                uncertainty=unavailable,
            )
            for index, offer in enumerate(receipt.offer_ids)
        ],
        root_value=AvailableQuantity(
            status="available",
            value=float(values @ receipt.target),
            method="signed_local_policy_value/v1",
        ),
        root_uncertainty=unavailable,
        simulations=len(receipt.rollouts),
        cap_hits=0,
        tree_nodes=0,
    )
