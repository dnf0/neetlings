"""Asset bundler compiling exercises, solutions, hints, and virtual runtime into JSON."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from neetlings import __version__
from neetlings.manifest import CATEGORIES, EXERCISE_RULES


def extract_hints_from_source(source: str) -> list[str]:
    """Parse HINTS = [...] list from Python source code using AST.

    Args:
        source: The Python source code string to parse.

    Returns:
        A list of hint strings, or an empty list if not found or invalid.
    """
    try:
        # Parse source code into an abstract syntax tree.
        tree = ast.parse(source)
    except SyntaxError:
        # Gracefully fall back on invalid syntax.
        return []

    # Traverse top-level nodes to find the assignment targeting HINTS.
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "HINTS":
                    # Extract string elements from list literal assignment.
                    if isinstance(node.value, ast.List):
                        hints: list[str] = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                hints.append(elt.value)
                        return hints
    return []


def strip_hints_from_source(source: str) -> str:
    """Remove HINTS = [...] block from Python source code using AST.

    Args:
        source: The Python source code string.

    Returns:
        The Python source code string without the HINTS block.
    """
    try:
        # Parse source code into an abstract syntax tree.
        tree = ast.parse(source)
    except SyntaxError:
        # Return unmodified source if syntax is invalid.
        return source

    hints_node = None
    # Traverse top-level nodes to locate the HINTS assignment statement.
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "HINTS":
                    hints_node = node
                    break
            if hints_node:
                break

    if hints_node is None:
        return source

    # Split lines, preserving line endings to maintain formatting.
    lines = source.splitlines(keepends=True)
    # Line numbers in AST nodes are 1-indexed.
    start_idx = hints_node.lineno - 1
    end_idx = hints_node.end_lineno if hints_node.end_lineno is not None else hints_node.lineno

    # Remove the contiguous block of lines matching the assignment.
    del lines[start_idx:end_idx]
    return "".join(lines)


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

                # Extract hints from solution, falling back to exercise code if not found or empty.
                hints = extract_hints_from_source(solution) if solution else []
                if not hints:
                    # Fallback to the exercise code's HINTS assignment if reference solution is absent.
                    hints = extract_hints_from_source(code)

                # Strip any leftover HINTS block from the student-facing template code.
                cleaned_code = strip_hints_from_source(code)

                # Look up specific banned actions or ops from EXERCISE_RULES manifest.
                rules = EXERCISE_RULES.get(ex_id, {})
                banned_calls = rules.get("banned_calls", [])
                banned_ops = rules.get("banned_ops", [])

                # Format programmatic identifier to a clean human-readable title.
                title = ex_id.replace("_", " ").title()
                exercises[ex_id] = {
                    "id": ex_id,
                    "categoryId": cat.id,
                    "title": title,
                    "code": cleaned_code,
                    "solution": solution,
                    "hints": hints,
                    "bannedCalls": banned_calls,
                    "bannedOps": banned_ops,
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
