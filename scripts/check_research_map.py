"""Check the authored research snapshot without loading manabot or running work.

Markdown owns questions, attachments and draft interpretations. The JSON manifest
only pins evidence bytes. This check verifies those joins and local navigation;
it does not reproduce private evidence or certify scientific conclusions.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "research" / "manabot"


def _git(*args: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.PIPE
    )


def _anchors(text: str) -> set[str]:
    """GitHub-style slugs for the ASCII headings used in this snapshot."""
    return {
        re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        for heading in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE)
    }


def check() -> list[str]:
    errors: list[str] = []
    manifest: object = json.loads((MAP / "sources.json").read_text())
    if not isinstance(manifest, dict):
        return ["source manifest must be an object"]
    snapshot = manifest.get("snapshot")
    sources = manifest.get("sources")
    if not isinstance(snapshot, str) or not isinstance(sources, list):
        return ["source manifest needs snapshot and sources"]
    pinned_reports: set[str] = set()
    identities: set[tuple[str, str]] = set()
    for source in sources:
        # JSON is untyped; narrow the fields once before using git or hashing.
        if not isinstance(source, dict) or not all(
            isinstance(source.get(key), str)
            for key in ("repository", "revision", "path", "sha256", "role")
        ):
            errors.append("malformed source entry")
            continue
        revision, path, digest = (
            str(source[key]) for key in ("revision", "path", "sha256")
        )
        if source["repository"] != "fantasia" or not re.fullmatch(
            r"[a-f0-9]{40}", revision
        ):
            errors.append(f"invalid repository/revision: {path}")
            continue
        identity = (revision, path)
        if identity in identities:
            errors.append(f"duplicate source: {path}@{revision}")
        identities.add(identity)
        try:
            data = _git("show", f"{revision}:{path}")
        except subprocess.CalledProcessError:
            if source["role"] == "pending-branch-report":
                print(f"Pending branch source unavailable locally: {path}@{revision}")
                continue
            errors.append(f"unavailable git source: {path}@{revision}")
            continue
        if hashlib.sha256(data).hexdigest() != digest:
            errors.append(f"changed source digest: {path}@{revision}")
        if revision == snapshot and source["role"] == "report":
            pinned_reports.add(path)
    report_paths = {
        path
        for path in _git("ls-tree", "--name-only", snapshot, "experiments/")
        .decode()
        .splitlines()
        if path.endswith(".md") and path != "experiments/README.md"
    }
    for path in sorted(report_paths - pinned_reports):
        errors.append(f"unmapped snapshot report: {path}")
    questions = (
        (MAP / "questions.md").read_text().split("## Complete attachment index")[0]
    )
    definitions = re.findall(r"\| `([a-z0-9-]+@1)` \|", questions)
    if len(set(definitions)) != len(definitions):
        errors.append("duplicate question identity")
    catalog = (MAP / "experiments.md").read_text()
    keys = re.findall(
        r"`fantasia:(?:report|collection):([a-z0-9.-]+)`",
        catalog.partition("\n## ")[2],
    )
    if len(set(keys)) != len(keys):
        errors.append("duplicate experiment key")
    for block in re.split(r"(?m)^#{2,3} ", catalog)[1:]:
        if not re.search(r"`fantasia:(?:report|collection):", block):
            continue
        attachments = re.findall(r"(?m)^- `([a-z0-9-]+@1)` — (.+)$", block)
        if not attachments:
            errors.append(
                f"experiment lacks relevance reasons: {block.splitlines()[0]}"
            )
        for question, reason in attachments:
            if question not in definitions or not reason.strip():
                errors.append(f"invalid question attachment: {question}")
    for path in sorted(pinned_reports):
        if f"../../{path})" not in catalog:
            errors.append(f"pinned report absent from register: {path}")
    for document in MAP.glob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
            if "://" in target:
                continue
            relative, _, anchor = unquote(target).partition("#")
            destination = document.parent / relative if relative else document
            if not destination.is_file():
                errors.append(f"broken link in {document.name}: {target}")
            elif anchor and destination.suffix == ".md":
                if anchor not in _anchors(destination.read_text()):
                    errors.append(f"broken anchor in {document.name}: {target}")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(errors))
        return 1
    print(
        "Research map: available source hashes, report coverage, question joins and links pass."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
