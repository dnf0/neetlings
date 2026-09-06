"""Tests for Neetlings data structure models."""

from neetlings.models import Interval, ListNode, TreeNode


def test_list_node_roundtrip() -> None:
    head = ListNode.from_list([1, 2, 3])
    assert head is not None
    assert head.to_list() == [1, 2, 3]
    assert head.to_ascii() == "1 ➔ 2 ➔ 3 ➔ None"


def test_list_node_empty() -> None:
    assert ListNode.from_list([]) is None


def test_tree_node_roundtrip() -> None:
    root = TreeNode.from_level_order([4, 2, 7, 1, 3, 6, 9])
    assert root is not None
    assert root.val == 4
    assert root.left is not None and root.left.val == 2
    assert root.right is not None and root.right.val == 7
    assert root.to_level_order() == [4, 2, 7, 1, 3, 6, 9]


def test_interval_model() -> None:
    inv = Interval(start=1, end=3)
    assert inv.to_list() == [1, 3]
