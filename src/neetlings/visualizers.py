"""Visualizers for data structure differences, formatted ASCII trees, and elevation diagrams."""

from __future__ import annotations

from typing import Any

from neetlings.models import ListNode, TreeNode

__all__ = [
    "format_grid",
    "format_list_diff",
    "format_rainwater_diff",
    "format_tree_diff",
    "render_ascii_elevation",
    "render_ascii_tree",
]


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


def render_ascii_elevation(heights: list[int], water: list[int] | None = None) -> str:
    """Render an ASCII elevation profile with optional trapped rainwater layers.

    Args:
        heights: List of non-negative bar heights.
        water: Optional list of trapped water units per column.

    Returns:
        Multi-line string diagram representing elevation and water levels.
    """
    # Guard clause: empty terrain profile cannot be rendered into an elevation grid.
    # Fallback to "(empty profile)" gives deterministic and human-readable feedback.
    if not heights:
        return "(empty profile)"

    # Compute maximum elevation including any trapped water to determine grid height.
    max_level = max(h + (water[i] if water and i < len(water) else 0) for i, h in enumerate(heights))

    # Render elevation lines from highest level down to 1.
    lines: list[str] = []
    for level in range(max_level, 0, -1):
        chars: list[str] = []
        for col, h in enumerate(heights):
            # Ground bar elevation reaches or exceeds current level.
            if h >= level:
                chars.append("#")
            # Trapped water surface reaches or exceeds current level.
            elif water and col < len(water) and h + water[col] >= level:
                chars.append("~")
            # Airspace above terrain and water.
            else:
                chars.append(" ")
        lines.append(f"{level:2d} | " + " ".join(chars))

    # Render baseline separator aligned with vertical axis and column positions.
    lines.append("   +-" + "--" * len(heights))

    # Render column index row with modulo-10 digits to prevent multi-digit column misalignment.
    lines.append("     " + " ".join(str(i % 10) for i in range(len(heights))))

    return "\n".join(lines)


def format_rainwater_diff(heights: list[int], expected: int, actual: int) -> str:
    """Format diagnostic difference for rainwater trapping tests.

    Computes the optimal water profile across columns using prefix and suffix maximums,
    and returns a formatted string comparing expected vs actual trapped water along with
    an ASCII elevation diagram showing the trapped water layers.

    Args:
        heights: Elevation map represented as a list of integers.
        expected: Expected total units of trapped water.
        actual: Actual units returned by the candidate solution.

    Returns:
        Formatted diagnostic diff string with expected/actual counts and ASCII diagram.
    """
    n = len(heights)
    # Compute prefix and suffix maximum elevations to find water capacity per column.
    left_max = [0] * n
    right_max = [0] * n

    running_left = 0
    for i in range(n):
        running_left = max(running_left, heights[i])
        left_max[i] = running_left

    running_right = 0
    for i in range(n - 1, -1, -1):
        running_right = max(running_right, heights[i])
        right_max[i] = running_right

    # Water trapped above bar i is bounded by min(left_max, right_max) minus bar height.
    optimal_water = [max(0, min(left_max[i], right_max[i]) - heights[i]) for i in range(n)]

    # Render elevation diagram with optimal water profile.
    elevation = render_ascii_elevation(heights, optimal_water)

    return (
        f"Expected Trapped Water: {expected}\n"
        f"Actual Trapped Water:   {actual}\n\n"
        f"{elevation}\n"
    )

