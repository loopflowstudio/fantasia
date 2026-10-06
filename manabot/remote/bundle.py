"""Preserve producer bytes while resolving relocated artifacts beneath one bundle.

The manifest binds every file and its original absolute path. It is transport
metadata, not a rewritten TrainingRun or a portable recovery checkpoint.
"""

import json
from pathlib import Path, PurePosixPath
import sqlite3
import sys

from pydantic import Field, model_validator

from manabot.sim.flat_mc import load_checkpoint_agent
from manabot.training.models import TrainingRun

from .plan import Frozen, digest


class BundleFile(Frozen):
    producer_path: str
    relative_path: str
    size: int = Field(ge=0)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    def destination(self, root: Path) -> Path:
        """Validate before download as well as before reading returned bytes."""
        relative = PurePosixPath(self.relative_path)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or not relative.parts
            or relative.as_posix() != self.relative_path
            or any(
                c
                not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-/"
                for c in self.relative_path
            )
        ):
            raise ValueError("invalid bundle path")
        path = root
        if path.is_symlink():
            raise ValueError("bundle root is a symlink")
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise ValueError("bundle contains a symlink")
        return path

    def verify(self, root: Path) -> Path:
        path = self.destination(root)
        if not path.is_file() or path.stat().st_size != self.size:
            raise ValueError("bundle file missing or size differs")
        if digest(path.read_bytes()) != self.sha256:
            raise ValueError("bundle digest differs")
        return path


class Bundle(Frozen):
    files: tuple[BundleFile, ...]

    @model_validator(mode="after")
    def unique_paths(self) -> "Bundle":
        relative = [item.relative_path for item in self.files]
        producer = [item.producer_path for item in self.files]
        if len(relative) != len(set(relative)) or len(producer) != len(set(producer)):
            raise ValueError("duplicate bundle paths")
        return self

    def verify(self, root: Path) -> None:
        for item in self.files:
            item.verify(root)

    def resolve(self, root: Path, producer_path: str) -> Path:
        for item in self.files:
            if item.producer_path == producer_path:
                return item.verify(root)
        raise ValueError("producer artifact missing")


def make_bundle(root: Path) -> Bundle:
    """Called on the producer after the CLI closes SQLite and all output files."""
    files: list[BundleFile] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("producer contains a symlink")
        if path.is_file():
            files.append(
                BundleFile(
                    producer_path=str(path.absolute()),
                    relative_path=path.relative_to(root).as_posix(),
                    size=path.stat().st_size,
                    sha256=digest(path.read_bytes()),
                )
            )
    return Bundle(files=tuple(files))


def verify_training_bundle(root: Path, bundle: Bundle) -> list[Path]:
    """Check all declared outputs; admit raw/EMA policies through the ordinary loader."""
    bundle.verify(root)
    required = {"training.sqlite", "run/run.json"}
    if not required.issubset({item.relative_path for item in bundle.files}):
        raise ValueError("bundle lacks authoritative run records")
    run = TrainingRun.model_validate(json.loads((root / "run/run.json").read_text()))
    with sqlite3.connect(
        f"{(root / 'training.sqlite').absolute().as_uri()}?mode=ro", uri=True
    ) as database:
        row = database.execute(
            "SELECT payload FROM training_runs WHERE id=?", (run.id,)
        ).fetchone()
    if row is None or TrainingRun.model_validate_json(row[0]) != run:
        raise ValueError("TrainingRun export differs from authoritative database")
    if run.status != "completed":
        raise ValueError("returned training run did not complete")
    policies: list[Path] = []
    for stage in run.stages:
        for name, artifact in stage.artifacts.items():
            path = bundle.resolve(root, artifact["path"])
            if (
                path.stat().st_size != artifact["bytes"]
                or digest(path.read_bytes()) != artifact["sha256"]
            ):
                raise ValueError("artifact differs from TrainingRun")
            if name in ("raw", "ema"):
                load_checkpoint_agent(str(path))
                policies.append(path)
    if not policies:
        raise ValueError("returned run has no policy exports")
    return policies


def main() -> None:
    """Write the producer manifest after the training CLI closes its evidence."""
    root = Path(sys.argv[1]).resolve()
    (root.parent / "bundle.json").write_text(
        make_bundle(root).model_dump_json(indent=2)
    )


if __name__ == "__main__":
    main()
