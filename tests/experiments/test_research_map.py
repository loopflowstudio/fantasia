"""Offline checks protect the research map's evidence boundaries, not its verdicts."""

import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from scripts import check_research_map as audit


@pytest.fixture
def snapshot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path
    mapping = root / "research" / "manabot"
    mapping.mkdir(parents=True)
    report = root / "experiments" / "probe.md"
    report.parent.mkdir()
    report.write_text("# Probe\nRetained result.\n")
    revision = "a" * 40
    manifest = {
        "repository": "fantasia",
        "snapshot": revision,
        "sources": [
            {
                "path": "experiments/probe.md",
                "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
                "role": "report",
            }
        ],
    }
    (mapping / "sources.json").write_text(json.dumps(manifest))
    (mapping / "questions.md").write_text("| Area | `question@1` | — | Why? |\n")
    (mapping / "experiments.md").write_text(
        "# Register\n\n## probe\n`fantasia:report:probe`\n"
        "[Source](../../experiments/probe.md)\n"
        "- `question@1` — Tests the question directly.\n"
    )

    def read_git(*args: str) -> bytes:
        if args[0] == "ls-tree":
            return b"experiments/probe.md\n"
        if args == ("show", f"{revision}:experiments/probe.md"):
            return report.read_bytes()
        raise subprocess.CalledProcessError(128, ["git", *args])

    monkeypatch.setattr(audit, "MAP", mapping)
    monkeypatch.setattr(audit, "_git", read_git)
    return mapping


def test_valid_snapshot(snapshot: Path) -> None:
    assert audit.check() == []


def test_changed_pinned_bytes_fail(snapshot: Path) -> None:
    path = snapshot / "sources.json"
    path.write_text(path.read_text().replace('"sha256": "', '"sha256": "bad'))
    assert any("changed source digest" in error for error in audit.check())


def test_unknown_question_fails(snapshot: Path) -> None:
    path = snapshot / "experiments.md"
    path.write_text(path.read_text().replace("question@1", "absent@1"))
    assert "invalid question attachment: absent@1" in audit.check()


def test_omitted_report_fails(snapshot: Path) -> None:
    (snapshot / "sources.json").write_text(
        json.dumps({"repository": "fantasia", "snapshot": "a" * 40, "sources": []})
    )
    assert "unmapped snapshot report: experiments/probe.md" in audit.check()


def test_missing_pending_branch_is_not_a_result_or_failure(
    snapshot: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = snapshot / "sources.json"
    manifest = json.loads(path.read_text())
    manifest["sources"].append(
        {
            "revision": "b" * 40,
            "path": "experiments/unpublished.md",
            "sha256": "c" * 64,
            "role": "pending-branch-report",
        }
    )
    path.write_text(json.dumps(manifest))
    assert audit.check() == []
    assert "Pending branch source unavailable locally" in capsys.readouterr().out


def test_broken_anchor_fails(snapshot: Path) -> None:
    (snapshot / "README.md").write_text("[Read](experiments.md#missing)\n")
    assert "broken anchor in README.md: experiments.md#missing" in audit.check()


def test_unavailable_required_revision_fails(snapshot: Path) -> None:
    path = snapshot / "sources.json"
    manifest = json.loads(path.read_text())
    manifest["sources"][0]["revision"] = "b" * 40
    path.write_text(json.dumps(manifest))
    assert f"unavailable git source: experiments/probe.md@{'b' * 40}" in audit.check()


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("repository", "etude", "source manifest repository must be fantasia"),
        ("snapshot", "main", "invalid snapshot revision"),
    ],
)
def test_invalid_manifest_identity_fails(
    snapshot: Path, field: str, value: str, error: str
) -> None:
    path = snapshot / "sources.json"
    manifest = json.loads(path.read_text())
    manifest[field] = value
    path.write_text(json.dumps(manifest))
    assert error in audit.check()
