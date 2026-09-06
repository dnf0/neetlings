"""Verify that all written reference solutions pass 100% of test cases."""

import importlib.util
from pathlib import Path


def test_all_reference_solutions() -> None:
    solutions_dir = Path("solutions")
    sol_files = sorted(solutions_dir.rglob("*.py"))
    assert len(sol_files) >= 26, f"Expected at least 26 solutions, found {len(sol_files)}"
    for sol_file in sol_files:
        spec = importlib.util.spec_from_file_location(sol_file.stem, sol_file)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "test_solution"), f"{sol_file} missing test_solution()"
        mod.test_solution()
