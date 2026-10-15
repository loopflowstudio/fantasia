"""Strict identities and artifact schemas for the manabot skill arena."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from manabot.sim.search_branch import branch_backend


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
BASE_ANCHOR_IDS = (
    "random-v1",
    "scripted-greedy-v1",
    "flat-mc-4-v1",
    "flat-mc-16-v1",
    "flat-mc-64-v1",
)


class ArenaKey(StrictModel):
    world: Literal["w2", "w3", "w4", "w5", "w6"]
