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
    test_cases: list[dict[str, Any]] | None = None,
    method_name: str = "solution",
    banned_calls: list[str] | None = None,
    banned_ops: list[str] | None = None,
    canonical_code: str | None = None,
) -> dict[str, Any]:
    """Execute user-supplied Python code in an isolated scope against test cases.

    Args:
        code_str: The student or reference Python source code string.
        test_cases: List of dictionaries containing test inputs, expected outputs, and names.
        method_name: The name of the solution method on class Solution to invoke.
        banned_calls: Disallowed functions or methods flagged via AST checking.
        banned_ops: Disallowed operator representations (e.g., ['/', '//']) flagged via AST checking.
        canonical_code: Optional reference/canonical code to extract test cases from.

    Returns:
        Structured evaluation result dictionary containing execution status, pass counts,
        duration, stdout logs, error details, case records, and diagnostic diffs.
    """
    # Initialize list of test cases resolved from inputs or canonical source.
    resolved_cases = list(test_cases) if test_cases else []

    # If no test cases are passed directly, try to extract them from canonical code.
    if not resolved_cases and canonical_code:
        # Prepare a clean scope for executing canonical code.
        canonical_scope: dict[str, Any] = {
            "ListNode": ListNode,
            "TreeNode": TreeNode,
            "Interval": Interval,
        }
        # Run canonical code to safely extract global TEST_CASES variable.
        try:
            exec(canonical_code, canonical_scope)
            if "TEST_CASES" in canonical_scope and isinstance(canonical_scope["TEST_CASES"], list):
                resolved_cases = canonical_scope["TEST_CASES"]
        except Exception:
            pass

    # 1. Check for banned AST calls and prohibited operators.
    violations = check_banned_syntax(code_str, banned_calls=banned_calls, banned_ops=banned_ops)
    if violations:
        # Halt execution and return security rules error with resolved counts.
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(resolved_cases),
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

        # Track execution performance starting from compilation phase.
        start_time = time.perf_counter()
        try:
            exec(code_str, scope)
        except Exception:
            # Trap compile/run-time errors when preparing user code.
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(resolved_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": f"Compilation/Import Error:\n{traceback.format_exc()}",
                "cases": [],
                "diagnosticDiff": None,
            }

        # Check if test cases can be resolved from the user-defined scope.
        if not resolved_cases and "TEST_CASES" in scope and isinstance(scope["TEST_CASES"], list):
            resolved_cases = scope["TEST_CASES"]

        # If no test cases are found anywhere, abort with structured ERROR code status.
        if not resolved_cases:
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": 0,
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": "Error: No test cases found to evaluate code.",
                "cases": [],
                "diagnosticDiff": None,
            }

        # Verify class Solution exists within the user scope.
        if "Solution" not in scope:
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(resolved_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": "Error: class Solution was not defined.",
                "cases": [],
                "diagnosticDiff": None,
            }

        # Instantiate solution object dynamically.
        sol_instance = scope["Solution"]()
        if not hasattr(sol_instance, method_name):
            # Abort if expected method name is missing on the Solution instance.
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": len(resolved_cases),
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": f"Error: Solution has no method '{method_name}'.",
                "cases": [],
                "diagnosticDiff": None,
            }

        # Extract executable reference method on the solution object.
        fn = getattr(sol_instance, method_name)

        # 4. Evaluate each test case
        cases_result: list[dict[str, Any]] = []
        all_passed = True
        diagnostic_diff: str | None = None

        # Execute test cases in sequential loop.
        for case in resolved_cases:
            c_name = case.get("name", "case")
            args = case["input"]
            expected = case["expected"]

            # Run execution with strict timeout mechanism.
            case_start = time.perf_counter()
            try:
                actual = run_with_timeout(fn, args, timeout=2.0)
                case_duration = (time.perf_counter() - case_start) * 1000.0

                # Compare actual output to target expected structure.
                passed = are_equal(actual, expected)
                if not passed:
                    all_passed = False
                    # Format structural diagnostic diff representation if mismatched.
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

                # Record individual test case result data.
                cases_result.append(
                    {
                        "name": c_name,
                        "status": "PASSED" if passed else "FAILED",
                        "durationMs": round(case_duration, 2),
                        "expected": str(expected),
                        "actual": str(actual),
                    }
                )
                # Fail fast and stop processing subsequent tests.
                if not passed:
                    break
            except Exception:
                # Capture unhandled exception and mark test status as FAILED.
                all_passed = False
                cases_result.append(
                    {
                        "name": c_name,
                        "status": "FAILED",
                        "durationMs": 0.0,
                        "expected": str(expected),
                        "actual": None,
                        "error": traceback.format_exc(),
                    }
                )
                break

        # Calculate final aggregated run execution duration.
        total_duration = (time.perf_counter() - start_time) * 1000.0

        # Compile final outcome and structure response data.
        return {
            "status": "PASSED" if all_passed and len(resolved_cases) > 0 else "FAILED",
            "passedCount": sum(1 for c in cases_result if c.get("status") == "PASSED"),
            "totalCount": len(resolved_cases),
            "durationMs": round(total_duration, 2),
            "stdout": stdout_buf.getvalue(),
            "error": None,
            "cases": cases_result,
            "diagnosticDiff": diagnostic_diff,
        }

    finally:
        # Reset original stdout stream cleanly.
        sys.stdout = old_stdout

