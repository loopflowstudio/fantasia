"""Producer-only closed-evidence manifest writer, invoked after the training CLI."""

from pathlib import Path
import sys

from .bundle import make_bundle


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    (root.parent / "bundle.json").write_text(
        make_bundle(root).model_dump_json(indent=2)
    )


if __name__ == "__main__":
    main()
