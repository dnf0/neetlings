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
