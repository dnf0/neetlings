"""In-memory code evaluation engine for browser Pyodide and local execution."""

from __future__ import annotations

import io
import sys
import threading
import time
import traceback
from typing import Any

from neetlings.complexity import check_banned_syntax
from neetlings.models import Interval, ListNode, TreeNode
from neetlings.visualizers import format_list_diff, format_tree_diff


def are_equal(actual: Any, expected: Any) -> bool:
    """Type-aware recursive equality check for ListNode, TreeNode, Interval, and containers."""
    if isinstance(actual, ListNode) and isinstance(expected, ListNode):
        return actual.to_list() == expected.to_list()
    if isinstance(actual, TreeNode) and isinstance(expected, TreeNode):
        return actual.to_level_order() == expected.to_level_order()
    if isinstance(actual, Interval) and isinstance(expected, Interval):
        return actual.start == expected.start and actual.end == expected.end
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        return all(are_equal(a, e) for a, e in zip(actual, expected))
    if isinstance(actual, dict) and isinstance(expected, dict):
        if len(actual) != len(expected):
            return False
        return all(k in expected and are_equal(actual[k], expected[k]) for k in actual)
    return actual == expected


def run_with_timeout(func: Any, args: tuple[Any, ...], timeout: float = 2.0) -> Any:
    """Run a function with a timeout. Fall back to direct execution if threading is unavailable."""
    res_list: list[Any] = []
    exc_list: list[Exception] = []

    def target() -> None:
        try:
            res_list.append(func(*args))
        except Exception as e:
            exc_list.append(e)

    try:
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            raise TimeoutError(f"Execution timed out after {timeout} seconds")
        if exc_list:
            raise exc_list[0]
        return res_list[0]
    except (RuntimeError, NotImplementedError):
        # Fallback for environments where threading is not fully supported (like some WASM runtimes)
        return func(*args)


def evaluate_code(
    code_str: str,
    test_cases: list[dict[str, Any]],
    method_name: str,
    banned_calls: list[str] | None = None,
    banned_ops: list[str] | None = None,
) -> dict[str, Any]:
    """Execute user-supplied Python code in an isolated scope against test cases.

    Args:
        code_str: The student or reference Python source code string.
        test_cases: List of dictionaries containing test inputs, expected outputs, and names.
        method_name: The name of the solution method on class Solution to invoke.
        banned_calls: Disallowed functions or methods flagged via AST checking.
        banned_ops: Disallowed operator representations (e.g., ['/', '//']) flagged via AST checking.

    Returns:
        Structured evaluation result dictionary containing execution status, pass counts,
        duration, stdout logs, error details, case records, and diagnostic diffs.
    """
    # 1. Check for banned AST calls and prohibited operators.
    violations = check_banned_syntax(code_str, banned_calls=banned_calls, banned_ops=banned_ops)
    if violations:
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(test_cases),
            "durationMs": 0.0,
            "stdout": "",
            "error": "Security / Complexity Rule Violation:\n" + "\n".join(violations),
            "cases": [],
            "diagnosticDiff": None,
        }

    # 2. Redirect stdout
    stdout_buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buf

    try:
        # 3. Compile and execute definitions
        scope: dict[str, Any] = {
            "ListNode": ListNode,
            "TreeNode": TreeNode,
            "Interval": Interval,
        }

        start_time = time.perf_counter()
        try:
            exec(code_str, scope)
        except Exception:
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(test_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": f"Compilation/Import Error:\n{traceback.format_exc()}",
                "cases": [],
                "diagnosticDiff": None,
            }

        if "Solution" not in scope:
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(test_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": "Error: class Solution was not defined.",
                "cases": [],
                "diagnosticDiff": None,
            }

        sol_instance = scope["Solution"]()
        if not hasattr(sol_instance, method_name):
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(test_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": f"Error: Solution has no method '{method_name}'.",
                "cases": [],
                "diagnosticDiff": None,
            }

        fn = getattr(sol_instance, method_name)

        # 4. Evaluate each test case
        cases_result: list[dict[str, Any]] = []
        all_passed = True
        diagnostic_diff: str | None = None

        for case in test_cases:
            c_name = case.get("name", "case")
            args = case["input"]
            expected = case["expected"]

            case_start = time.perf_counter()
            try:
                actual = run_with_timeout(fn, args, timeout=2.0)
                case_duration = (time.perf_counter() - case_start) * 1000.0

                # Compare results
                passed = are_equal(actual, expected)
                if not passed:
                    all_passed = False
                    # Check if visualizer diff applies
                    if isinstance(expected, TreeNode) or isinstance(actual, TreeNode):
                        diagnostic_diff = format_tree_diff(
                            expected if isinstance(expected, TreeNode) else None,
                            actual if isinstance(actual, TreeNode) else None,
                        )
                    elif isinstance(expected, ListNode) or isinstance(actual, ListNode):
                        diagnostic_diff = format_list_diff(
                            expected if isinstance(expected, ListNode) else None,
                            actual if isinstance(actual, ListNode) else None,
                        )

                cases_result.append(
                    {
                        "name": c_name,
                        "status": "PASSED" if passed else "FAILED",
                        "durationMs": round(case_duration, 2),
                        "expected": str(expected),
                        "actual": str(actual),
                    }
                )
                if not passed:
                    break
            except Exception:
                all_passed = False
                cases_result.append(
                    {
                        "name": c_name,
                        "status": "ERROR",
                        "durationMs": 0.0,
                        "error": traceback.format_exc(),
                    }
                )
                break

        total_duration = (time.perf_counter() - start_time) * 1000.0

        return {
            "status": "PASSED" if all_passed else "FAILED",
            "passedCount": sum(1 for c in cases_result if c.get("status") == "PASSED"),
            "totalCount": len(test_cases),
            "durationMs": round(total_duration, 2),
            "stdout": stdout_buf.getvalue(),
            "error": None,
            "cases": cases_result,
            "diagnosticDiff": diagnostic_diff,
        }

    finally:
        sys.stdout = old_stdout
