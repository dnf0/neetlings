"""Tests for ASCII diagnostic visualizers."""

from neetlings.models import ListNode, TreeNode
from neetlings.visualizers import (
    format_grid,
    format_list_diff,
    format_rainwater_diff,
    format_tree_diff,
    render_ascii_elevation,
    render_ascii_tree,
)


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


def test_render_ascii_elevation_empty() -> None:
    """Verifies that an empty heights list returns the designated empty profile placeholder."""
    # Empty terrain profile must return deterministic fallback string.
    assert render_ascii_elevation([]) == "(empty profile)"


def test_render_ascii_elevation_simple() -> None:
    """Verifies rendering of simple elevation profile with aligned levels, baseline, and indices."""
    # Render three increasing elevation bars with no water layers.
    diagram = render_ascii_elevation([1, 2, 3])
    lines = diagram.split("\n")
    # Verify exact level contents, ground bars, airspace, baseline, and index row.
    assert lines[0] == " 3 |     #"
    assert lines[1] == " 2 |   # #"
    assert lines[2] == " 1 | # # #"
    assert lines[3] == "   +-------"
    assert lines[4] == "     0 1 2"


def test_render_ascii_elevation_with_water() -> None:
    """Verifies rendering of trapped water symbols in valleys between solid bars."""
    # Render a V-valley containing trapped water in the middle column.
    diagram = render_ascii_elevation([3, 0, 3], water=[0, 3, 0])
    lines = diagram.split("\n")
    # Verify water symbols `~` fill the valley at all levels up to max height.
    assert lines[0] == " 3 | # ~ #"
    assert lines[1] == " 2 | # ~ #"
    assert lines[2] == " 1 | # ~ #"
    assert lines[3] == "   +-------"
    assert lines[4] == "     0 1 2"


def test_render_ascii_elevation_flat_zero() -> None:
    """Verifies that flat terrain with zero elevation produces only baseline and indices."""
    # Zero elevation has no positive level rows to display.
    diagram = render_ascii_elevation([0, 0, 0])
    lines = diagram.split("\n")
    assert len(lines) == 2
    assert lines[0] == "   +-------"
    assert lines[1] == "     0 1 2"


def test_render_ascii_elevation_modulo_indices() -> None:
    """Verifies modulo-10 column indices for profiles longer than 10 columns."""
    # Twelve columns verify that columns 10 and 11 wrap to 0 and 1.
    diagram = render_ascii_elevation([1] * 12)
    lines = diagram.split("\n")
    assert lines[-1] == "     " + " ".join(str(i % 10) for i in range(12))


def test_format_rainwater_diff_standard() -> None:
    """Verifies format_rainwater_diff computes optimal water and includes expected/actual numbers."""
    # Standard rainwater profile with mismatch between expected and actual units.
    diff = format_rainwater_diff([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], expected=6, actual=5)
    # Check output components.
    assert "Expected Trapped Water: 6" in diff
    assert "Actual Trapped Water:   5" in diff
    assert "#" in diff
    assert "~" in diff
    assert "   +-" in diff


def test_format_rainwater_diff_empty() -> None:
    """Verifies format_rainwater_diff with empty elevation list."""
    # Empty profile diagnostic diff should cleanly show empty profile fallback.
    diff = format_rainwater_diff([], expected=0, actual=0)
    assert "Expected Trapped Water: 0" in diff
    assert "Actual Trapped Water:   0" in diff
    assert "(empty profile)" in diff

