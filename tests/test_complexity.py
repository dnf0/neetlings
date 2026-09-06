"""Tests for AST complexity and banned syntax verification."""

import pytest

from neetlings.complexity import StepCounter, StepLimitExceeded, check_banned_syntax


def test_check_banned_syntax_finds_sort() -> None:
    user_code = """
def sort_colors(nums):
    nums.sort()
"""
    violations = check_banned_syntax(user_code, banned_calls=["sort"])
    assert len(violations) == 1
    assert "Disallowed call: sort" in violations[0]


def test_check_banned_syntax_clean() -> None:
    user_code = """
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen: return True
        seen.add(x)
    return False
"""
    assert check_banned_syntax(user_code, banned_calls=["sort"]) == []


def test_step_counter() -> None:
    counter = StepCounter(max_steps=100)
    with counter:
        for _ in range(10):
            counter.step()
    assert counter.total_steps == 10


def test_step_counter_exceeds_limit() -> None:
    counter = StepCounter(max_steps=5)
    with pytest.raises(StepLimitExceeded):
        with counter:
            for _ in range(10):
                counter.step()


def test_check_banned_syntax_flags_division_operators() -> None:
    """Verify that division and floor division operators are detected when banned."""
    # Source snippet utilizing true division and floor division in a loop.
    user_code_div = """
def product_except_self(nums):
    total = 1
    for x in nums:
        total = total * x
    return [total / x for x in nums]
"""
    # Check that true division is flagged when banned.
    violations_div = check_banned_syntax(user_code_div, banned_ops=["/", "//"])
    assert len(violations_div) == 1
    assert "Disallowed operator: /" in violations_div[0]

    # Source snippet utilizing floor division operator.
    user_code_floordiv = """
def product_except_self(nums):
    total = 1
    for x in nums:
        total = total * x
    return [total // x for x in nums]
"""
    # Check that floor division is flagged when banned.
    violations_floordiv = check_banned_syntax(user_code_floordiv, banned_ops=["/", "//"])
    assert len(violations_floordiv) == 1
    assert "Disallowed operator: //" in violations_floordiv[0]

    # Source snippet using only multiplication and addition without division.
    clean_code = """
def product_except_self(nums):
    res = [1] * len(nums)
    prefix = 1
    for i in range(len(nums)):
        res[i] = prefix
        prefix *= nums[i]
    return res
"""
    # Verify that clean code produces zero violations.
    assert check_banned_syntax(clean_code, banned_ops=["/", "//"]) == []


def test_check_banned_syntax_flags_array_banned_calls() -> None:
    """Verify that banned builtins and methods like sort and sorted are detected."""
    # Source snippet using the .sort() list method.
    code_sort_method = """
def top_k_frequent(nums, k):
    nums.sort()
    return nums[:k]
"""
    # Detect in-place sort method call.
    violations_method = check_banned_syntax(code_sort_method, banned_calls=["sort", "sorted"])
    assert len(violations_method) == 1
    assert "Disallowed call: sort" in violations_method[0]

    # Source snippet calling the sorted() built-in function.
    code_sorted_builtin = """
def longest_consecutive(nums):
    s = sorted(nums)
    return len(s)
"""
    # Detect sorted built-in call.
    violations_builtin = check_banned_syntax(code_sorted_builtin, banned_calls=["sort", "sorted"])
    assert len(violations_builtin) == 1
    assert "Disallowed call: sorted" in violations_builtin[0]

