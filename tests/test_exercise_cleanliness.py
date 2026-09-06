"""Tests verifying that exercise files are clean of spoiler hints and syntactically valid."""

import ast
from pathlib import Path

from neetlings.manifest import EXERCISE_RULES


def test_no_hints_in_exercise_files() -> None:
    exercises_dir = Path("exercises")
    ex_files = sorted(exercises_dir.rglob("*.py"))
    assert len(ex_files) >= 30, f"Expected at least 30 exercise files, found {len(ex_files)}"

    for ex_file in ex_files:
        content = ex_file.read_text(encoding="utf-8")
        assert "HINTS = [" not in content, f"Spoiler hints found in {ex_file}"
        # Ensure file parses as valid Python
        ast.parse(content, filename=str(ex_file))


def test_exercise_rules_manifest() -> None:
    assert isinstance(EXERCISE_RULES, dict)
    assert "06_product_of_array_except_self" in EXERCISE_RULES
    assert EXERCISE_RULES["06_product_of_array_except_self"].get("banned_ops") == ["/", "//"]
    assert "02_two_sum_ii_input_array_is_sorted" in EXERCISE_RULES
    assert EXERCISE_RULES["02_two_sum_ii_input_array_is_sorted"].get("banned_calls") == [
        "dict",
        "defaultdict",
    ]
