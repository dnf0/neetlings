"""Asset bundler compiling exercises, solutions, hints, and virtual runtime into JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neetlings import __version__
from neetlings.manifest import CATEGORIES


def generate_bundle(repo_root: Path | None = None) -> dict[str, Any]:
    """Compile curriculum and runtime into a single JSON-serializable dictionary.

    Args:
        repo_root: Optional custom path to the repository root directory. Defaults to CWD.

    Returns:
        A dict containing version, chapters list, exercises lookup, and virtual runtime files.
    """
    # Fallback to Current Working Directory if repo_root is unspecified.
    if repo_root is None:
        repo_root = Path.cwd()

    # Define paths for core source, exercises, and solutions.
    src_dir = repo_root / "src" / "neetlings"
    exercises_dir = repo_root / "exercises"
    solutions_dir = repo_root / "solutions"

    # Bundle target runtime modules to be dynamically loaded in the sandbox environment.
    runtime_modules: dict[str, str] = {}
    for filename in ["models.py", "visualizers.py", "complexity.py", "test_runner.py"]:
        path = src_dir / filename
        if path.exists():
            runtime_modules[filename] = path.read_text(encoding="utf-8")

    chapters: list[dict[str, Any]] = []
    exercises: dict[str, Any] = {}

    # Iterate through all 18 categories to scan directory-based learning exercises and solutions.
    for cat in CATEGORIES:
        ch_dir_name = f"{cat.number:02d}_{cat.id}"
        ex_dir = exercises_dir / ch_dir_name
        ex_ids: list[str] = []

        # If the chapter exercises folder exists, extract its individual python exercises.
        if ex_dir.exists():
            for ex_file in sorted(ex_dir.glob("*.py")):
                ex_id = ex_file.stem
                ex_ids.append(ex_id)
                sol_file = solutions_dir / ch_dir_name / ex_file.name

                code = ex_file.read_text(encoding="utf-8")
                solution = sol_file.read_text(encoding="utf-8") if sol_file.exists() else ""

                # Format programmatic identifier to a clean human-readable title.
                title = ex_id.replace("_", " ").title()
                exercises[ex_id] = {
                    "id": ex_id,
                    "categoryId": cat.id,
                    "title": title,
                    "code": code,
                    "solution": solution,
                }

        # Build chapter metadata structured dictionary.
        chapters.append(
            {
                "number": cat.number,
                "id": cat.id,
                "title": cat.title,
                "description": cat.description,
                "exerciseIds": ex_ids,
            }
        )

    # Return the aggregated playground payload dictionary.
    return {
        "version": __version__,
        "totalChapters": len(chapters),
        "totalExercises": len(exercises),
        "chapters": chapters,
        "exercises": exercises,
        "runtime_modules": runtime_modules,
    }


def export_bundle(dest_path: Path, repo_root: Path | None = None) -> Path:
    """Generate the curriculum bundle and write it to the specified destination path as JSON.

    Args:
        dest_path: The target path where the compiled playground JSON bundle is exported.
        repo_root: Optional custom path to the repository root directory.

    Returns:
        The verified absolute or relative path to the written JSON file.
    """
    # Compile the standard package bundle.
    bundle = generate_bundle(repo_root)

    # Ensure that any parent directories for the destination path exist.
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the formatted payload with 2-space indentation.
    dest_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    return dest_path
