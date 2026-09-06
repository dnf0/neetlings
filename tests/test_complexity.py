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
