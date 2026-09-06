"""Tests for ASCII diagnostic visualizers."""

from neetlings.models import ListNode, TreeNode
from neetlings.visualizers import format_grid, format_list_diff, format_tree_diff, render_ascii_tree


def test_render_ascii_tree() -> None:
    root = TreeNode.from_level_order([4, 2, 7, 1, 3])
    diagram = render_ascii_tree(root)
    assert "4" in diagram
    assert "2" in diagram
    assert "7" in diagram


def test_format_tree_diff() -> None:
    expected = TreeNode.from_level_order([4, 7, 2])
    actual = TreeNode.from_level_order([4, 2, 7])
    diff = format_tree_diff(expected, actual)
    assert "--- Expected Tree ---" in diff
    assert "--- Actual Tree ---" in diff


def test_format_list_diff() -> None:
    exp = ListNode.from_list([1, 2, 3])
    act = ListNode.from_list([1, 3, 2])
    diff = format_list_diff(exp, act)
    assert "Expected List:" in diff
    assert "Actual List:" in diff


def test_format_grid() -> None:
    grid = [[1, 0], [0, 1]]
    output = format_grid(grid)
    assert "0" in output
    assert "1" in output
