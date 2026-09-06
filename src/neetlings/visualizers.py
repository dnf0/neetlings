"""Visualizers for data structure differences and formatted ASCII trees."""

from __future__ import annotations

from typing import Any

from neetlings.models import ListNode, TreeNode


def render_ascii_tree(root: TreeNode | None, prefix: str = "", is_left: bool = True) -> str:
    """Render a binary tree into a clean multi-line ASCII diagram."""
    if root is None:
        return ""
    lines: list[str] = []
    if root.right is not None:
        lines.append(render_ascii_tree(root.right, prefix + ("│   " if is_left else "    "), False))
    lines.append(prefix + ("└── " if is_left else "┌── ") + str(root.val))
    if root.left is not None:
        lines.append(render_ascii_tree(root.left, prefix + ("    " if is_left else "│   "), True))
    return "\n".join(line for line in lines if line)


def format_tree_diff(expected: TreeNode | None, actual: TreeNode | None) -> str:
    """Render side-by-side or stacked tree diagrams comparing expected and actual trees."""
    exp_tree = render_ascii_tree(expected) or "(Empty Tree)"
    act_tree = render_ascii_tree(actual) or "(Empty Tree)"
    return f"--- Expected Tree ---\n{exp_tree}\n\n--- Actual Tree ---\n{act_tree}\n"


def format_list_diff(expected: ListNode | None, actual: ListNode | None) -> str:
    """Render linked list comparison."""
    exp_str = expected.to_ascii() if expected else "None"
    act_str = actual.to_ascii() if actual else "None"
    return f"Expected List: {exp_str}\nActual List:   {act_str}\n"


def format_grid(grid: list[list[Any]]) -> str:
    """Render 2D matrix with coordinate row/column headers."""
    if not grid or not grid[0]:
        return "[]"
    header = "     " + " ".join(f"{c:3}" for c in range(len(grid[0])))
    sep = "    +" + "---" * len(grid[0])
    rows: list[str] = [header, sep]
    for r, row in enumerate(grid):
        row_str = " ".join(f"{str(v):3}" for v in row)
        rows.append(f"{r:2} | {row_str}")
    return "\n".join(rows)
