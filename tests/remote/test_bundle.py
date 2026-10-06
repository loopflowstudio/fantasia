"""Relocation preserves evidence and rejects unsafe or corrupt paths."""

from pathlib import Path

import pytest

from manabot.remote.bundle import Bundle, BundleFile, make_bundle
from manabot.remote.plan import digest


def test_relocated_bytes_and_corruption(tmp_path: Path) -> None:
    producer = tmp_path / "producer"
    producer.mkdir()
    artifact = producer / "policy.pt"
    artifact.write_bytes(b"immutable")
    manifest = make_bundle(producer)
    destination = tmp_path / "returned"
    producer.rename(destination)
    assert manifest.resolve(destination, str(artifact)).read_bytes() == b"immutable"
    (destination / "policy.pt").write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="digest"):
        manifest.verify(destination)


def test_traversal_and_symlink_rejected(tmp_path: Path) -> None:
    artifact = tmp_path / "private"
    artifact.write_bytes(b"x")
    root = tmp_path / "bundle"
    root.mkdir()
    for relative in ("../private", str(artifact), "link"):
        (root / "link").unlink(missing_ok=True)
        (root / "link").symlink_to(artifact)
        bundle = Bundle(
            files=(
                BundleFile(
                    producer_path="/original",
                    relative_path=relative,
                    size=1,
                    sha256=digest(b"x"),
                ),
            )
        )
        with pytest.raises(ValueError):
            bundle.verify(root)
