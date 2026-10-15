"""Bounded regime execution; VerifyStore owns state, manifests are exports."""

from collections.abc import Mapping
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import asdict
import json
import os
from pathlib import Path
import platform
import socket
import time
from typing import TYPE_CHECKING
import uuid

import numpy as np
import psutil
import torch

from manabot.arena.models import canonical_sha256, file_sha256
from manabot.belief.sampling_data import (
    collect_frozen_policy,
    read_dataset,
    save_dataset,
)
from manabot.belief.sampling_fit import (
    fit_belief_sampler,
    load_belief_sampler,
    save_belief_sampler,
)
from manabot.env import Match, ObservationSpace, Reward
from manabot.infra import Experiment
from manabot.infra.hypers import ExperimentHypers, RewardHypers, TrainHypers
from manabot.model.agent import Agent
from manabot.model.architecture import architecture_identity
from manabot.model.policy_distribution import NumericalError
from manabot.model.world import validate_agent_setup
from manabot.remote.plan import Allocation
from manabot.sim.distill import generate_selfplay_shard, load_shards, save_bc_checkpoint
from manabot.sim.flat_mc import load_checkpoint_agent
from manabot.sim.net_opponent import NetOpponentTrainer, SeatRoutedCollector
from manabot.sim.search_supervised import (
    SearchSupervisedEpochStats,
    train_search_supervised,
)
from manabot.sim.teacher1_evidence import runtime_fingerprints, source_bundle_sha256
import managym

from .admission import admit_policy
from .clock import boot_identity, watchdog_seconds
from .compound import CompoundStatistics, collect_game, optimize_games, replay_game
from .incidents import save_incident
from .learning_state import admit_learning_state, validate_adam
from .models import (
    ArtifactReference,
    CheckpointCadence,
    CollectBelief,
    CollectLocalUpdate,
    CollectSearch,
    CollectSelection,
    FixedValidationCohort,
    ImportPolicy,
    MonitoringCheckpoint,
    NumericalFailure,
    StageRecord,
    TrainBelief,
    TrainCompound,
    TrainingRegime,
    TrainingRun,
    TrainSelfPlay,
    TrainSupervised,
)
from .objectives import update_ema, update_iteration
from .recovery import (
    TrainingPaused,
    UpdateSnapshot,
    attempt_lock,
    load_update,
    restore_learning,
    save_update,
    settle_orphan,
)
from .selection_analysis import analyze_selection, write_selection_report
from .selection_data import SelectionDataset, collect_selection_game
from .source_bundle import source_commit

if TYPE_CHECKING:
    from manabot.verify.store import VerifyStore


# Longest a run.json export may lag the store while a stage is making progress.
PROGRESS_EXPORT_SECONDS = 30.0
# Largest share of a stage's wall time that progress exports may consume.
PROGRESS_EXPORT_SHARE = 0.02


def atomic_json(path: str | Path, value: object) -> None:
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    os.replace(temporary, path)


def export_training_run(
    run_id: str, store: "VerifyStore", out: str | Path
) -> TrainingRun:
    run = store.training_run(run_id)
    atomic_json(Path(out) / "run.json", run.model_dump(mode="json"))
    return run


def validate_regime(
    regime: TrainingRegime | Mapping[str, object], *, require_current_world: bool = True
) -> TrainingRegime:
    """Validate a recipe; execution additionally requires the native world.

    Offline authoring can resolve historical recipes without relabeling them.
    Every execution entry point retains the current-world check by default.
    """
    regime = TrainingRegime.model_validate(
        regime.model_dump() if isinstance(regime, TrainingRegime) else regime
    )
    if require_current_world and regime.world != managym.WORLD_VERSION:
        raise ValueError("regime world differs from native runtime")
    if regime.world not in {"w2", "w3", "w4", "w5", managym.WORLD_VERSION}:
