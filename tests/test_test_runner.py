"""Tests for in-memory test runner."""

from neetlings.models import TreeNode
from neetlings.test_runner import evaluate_code


def test_evaluate_passing_code() -> None:
    code = """
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        lookup = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in lookup:
                return [lookup[diff], i]
            lookup[n] = i
        return []
"""
    test_cases = [
        {"input": ([2, 7, 11, 15], 9), "expected": [0, 1], "name": "basic"},
        {"input": ([3, 2, 4], 6), "expected": [1, 2], "name": "unsorted"},
    ]
    res = evaluate_code(code, test_cases, method_name="two_sum")
    assert res["status"] == "PASSED"
    assert res["passedCount"] == 2
    assert res["totalCount"] == 2
    assert res["error"] is None


def test_evaluate_failing_code() -> None:
    code = """
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        return []
"""
    test_cases = [{"input": ([2, 7, 11, 15], 9), "expected": [0, 1], "name": "basic"}]
    res = evaluate_code(code, test_cases, method_name="two_sum")
    assert res["status"] == "FAILED"
    assert res["passedCount"] == 0
    assert len(res["cases"]) == 1


def test_evaluate_banned_syntax_rejection() -> None:
    code = """
class Solution:
    def sort_colors(self, nums: list[int]) -> None:
        nums.sort()
"""
    test_cases = [{"input": ([2, 0, 2, 1, 1, 0],), "expected": None, "name": "basic"}]
    res = evaluate_code(code, test_cases, method_name="sort_colors", banned_calls=["sort"])
    assert res["status"] == "ERROR"
    assert "Disallowed call: sort" in (res["error"] or "")


def test_evaluate_banned_ops_rejection() -> None:
    """Verify that evaluate_code rejects code containing banned operators."""
    # Code snippet that uses division for product_except_self.
    code = """
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        total = 1
        for n in nums:
            total *= n
        return [total // n for n in nums]
"""
    test_cases = [{"input": ([1, 2, 3, 4],), "expected": [24, 12, 8, 6], "name": "basic"}]
    # Run code evaluation with banned floor division and true division.
    res = evaluate_code(code, test_cases, method_name="productExceptSelf", banned_ops=["/", "//"])
    assert res["status"] == "ERROR"
    assert "Disallowed operator: //" in (res["error"] or "")



def test_evaluate_tree_diagnostic_diff_on_failure() -> None:
    code = """
class Solution:
    def invert_tree(self, root):
        return root  # buggy: returns unmodified
"""
    root = TreeNode.from_level_order([4, 2, 7])
    expected = TreeNode.from_level_order([4, 7, 2])
    test_cases = [{"input": (root,), "expected": expected, "name": "invert"}]
    res = evaluate_code(code, test_cases, method_name="invert_tree")
    assert res["status"] == "FAILED"
    assert res["diagnosticDiff"] is not None
    assert "--- Expected Tree ---" in res["diagnosticDiff"]


def test_evaluate_failing_code_not_implemented() -> None:
    """Verify that code raising NotImplementedError returns FAILED status, not PASSED."""
    # Define a solution code block that raises NotImplementedError.
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        raise NotImplementedError
"""
    # Define matching canonical code with correct test cases.
    canonical_code = """
TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "example1"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "example2"},
]
"""
    # Evaluate the student code against the canonical test cases.
    res = evaluate_code(code, test_cases=None, method_name="containsDuplicate", canonical_code=canonical_code)

    # Perform assertions on the failure details and statuses.
    assert res["status"] == "FAILED"
    assert res["passedCount"] == 0
    assert res["totalCount"] == 2
    assert len(res["cases"]) == 1
    assert res["cases"][0]["status"] == "FAILED"
    assert "NotImplementedError" in (res["cases"][0].get("error") or "")


def test_evaluate_empty_test_cases_returns_error() -> None:
    """Verify that when no test cases exist anywhere, status is ERROR, never PASSED."""
    # Define a solution code block that returns a simple boolean.
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return False
"""
    # Evaluate the code with empty test cases.
    res = evaluate_code(code, test_cases=[], method_name="containsDuplicate")

    # Assert that the status is ERROR and an appropriate error message is given.
    assert res["status"] == "ERROR"
    assert res["passedCount"] == 0
    assert "No test cases found" in (res["error"] or "")


def test_evaluate_extracts_canonical_code_test_cases() -> None:
    """Verify that evaluate_code automatically extracts test cases from canonical_code."""
    # Define a correct solution code block.
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))
"""
    # Define matching canonical code with correct test cases.
    canonical_code = """
TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "example1"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "example2"},
]
"""
    # Evaluate code with None test cases to trigger auto extraction from canonical.
    res = evaluate_code(code, test_cases=None, method_name="containsDuplicate", canonical_code=canonical_code)

    # Assert that all extracted tests are evaluated and pass successfully.
    assert res["status"] == "PASSED"
    assert res["passedCount"] == 2
    assert res["totalCount"] == 2

