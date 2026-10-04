"""Offline analysis of retained training and arena evidence."""

import json
from pathlib import Path

from .execution import atomic_json


def report(out):
    from nbclient import NotebookClient
    import nbformat

    out = Path(out).resolve()
    study = json.loads((out / "study.json").read_text())
    rows = study["measurements"]
    lines = [
        f"# {study['study']} — {study['profile']}",
        "",
        f"Status: {study['status']}. {study['limits']}",
        "",
        "Playing score is measured against the named opponent. Cost curves use the fixed random anchor; paired-recipe matches are listed separately. The smoke has one training seed and one deal block: cross-seed uncertainty is unavailable. These points prove execution, not learning-speed superiority.",
        "",
        "| Recipe | Cutoff | Opponent | Training seconds | Decisions | Complete games | Score |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        score = "unavailable" if row["score"] is None else f"{row['score']:.3f}"
        lines.append(
            f"| {row['regime']} | {row['cutoff']} | {row['opponent']} | {row['training_seconds']:.2f} | {row['decisions']} | {row['games']} | {score} |"
        )
    if not rows:
        lines += ["", "No completed measurements."]
    if study.get("error"):
        lines += ["", study["error"]]
    lines += [
        "",
        "Evaluation seconds: "
        + str(sum(c["evaluation_seconds"] for c in study["comparisons"])),
        "",
        "Not run: independent-seed inference, confirmatory scoring, S1–S5 current-world rebinding, human play, raw/EMA arena comparison, compound actions, belief-guided search, update distillation, belief sampling and exploiters. See the experiment protocols before funding those runs.",
        "",
        "Traces and per-game failures:",
    ]
    lines += [
        f"- [{c['a']} / {c['b']} cutoff {c['cutoff']}]({c['trace']['path']}) — exact replay {c['replay']['passed']}"
        for c in study["comparisons"]
    ]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    atomic_json(out / "metrics.json", rows)
    notebook = nbformat.read(
        Path(__file__).resolve().parents[2]
        / "experiments/study/training-regimes.ipynb",
        as_version=4,
    )
    notebook.cells.insert(
        0, nbformat.v4.new_code_cell(f"study_path = {str(out / 'study.json')!r}")
    )
    NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(out)}},
    ).execute()
    nbformat.write(notebook, out / "analysis.ipynb")
