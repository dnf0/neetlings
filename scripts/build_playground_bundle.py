#!/usr/bin/env python3
"""CLI script to build neetlings playground bundle."""

import sys
from pathlib import Path

# Ensure that the src directory is in the import path for direct executions.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from neetlings.bundler import export_bundle


def main() -> None:
    """Run bundle generation and export it to the playground assets location."""
    # Define target playground JSON bundle path.
    dest = Path("docs/assets/playground/playground-bundle.json")

    # Export bundle to destination path.
    out = export_bundle(dest)
    print(f"✓ Built Neetlings WebAssembly Bundle at: {out}")


if __name__ == "__main__":
    main()
