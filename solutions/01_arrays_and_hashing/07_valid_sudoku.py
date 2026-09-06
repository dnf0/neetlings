"""Valid Sudoku.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates matrix traversal and duplicate detection using hash sets.

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated
according to the following rules:
1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

Note:
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.
- Only the filled cells need to be validated according to the mentioned rules.

Examples:
    1. Input: board =
       [["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]]
       Output: true

    2. Input: board =
       [["8","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]]
       Output: false
       Explanation: Same as Example 1, except with the top-left cell changed to 8.
       Since there is already an 8 in the top-left 3x3 sub-box, it is invalid.

Constraints:
    - board.length == 9
    - board[i].length == 9
    - board[i][j] is a digit '1'-'9' or '.'.

Target:
    - Time Complexity: O(1) across the fixed 9x9 board (81 cells)
    - Space Complexity: O(1) auxiliary space (fixed-size hash sets)
"""

from collections import defaultdict

HINTS = [
    "A Sudoku board is valid if no digit '1'-'9' repeats within any individual row, column, or 3x3 sub-box. Blank cells ('.') are ignored.",
    "Hash sets or boolean lookup tables. Maintain tracking collections for each of the 9 rows, 9 columns, and 9 sub-boxes during a single traversal of the 9x9 grid.",
    "Map cell coordinates (r, c) to their corresponding 3x3 sub-box index or coordinate tuple using integer division: `(r // 3, c // 3)`. Ensure only non-period characters are evaluated.",
    "Initialize row sets, col sets, and box sets (e.g. `boxes = collections.defaultdict(set)` or 2D array). For each row r from 0..8 and col c from 0..8, fetch `val = board[r][c]`. If `val == '.'`, continue. If `val` is in `rows[r]`, `cols[c]`, or `boxes[(r // 3, c // 3)]`, return False; otherwise add `val` to all three sets. Return True if no conflicts arise.",
]


class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        """Validate if a 9x9 Sudoku board conforms to Sudoku rules.

        Checks each row, column, and 3x3 sub-box for duplicate digits
        in O(1) time and O(1) space across the fixed 81-cell board.

        Args:
            board: 9x9 grid of characters representing the Sudoku board.

        Returns:
            True if board satisfies row, column, and 3x3 sub-box constraints, False otherwise.
        """
        # Fixed tracking collections for 9 rows, 9 columns, and 9 sub-boxes.
        # Sub-boxes are indexed by coordinate tuples (r // 3, c // 3).
        rows: list[set[str]] = [set() for _ in range(9)]
        cols: list[set[str]] = [set() for _ in range(9)]
        boxes: dict[tuple[int, int], set[str]] = defaultdict(set)

        # Single-pass scan over all 81 cells in the fixed 9x9 grid.
        for r in range(9):
            for c in range(9):
                val = board[r][c]

                # Period represents an empty cell, which does not violate constraints.
                if val == ".":
                    continue

                # Box coordinate mapping: (r // 3, c // 3) groups 3x3 sub-grids.
                box_key = (r // 3, c // 3)

                # Check for duplicates across current row, column, and sub-box.
                # Returning immediately upon detection provides early exit.
                if val in rows[r] or val in cols[c] or val in boxes[box_key]:
                    return False

                # Register the digit in respective tracking sets.
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_key].add(val)

        return True


VALID_PARTIAL_BOARD = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

VALID_COMPLETE_BOARD = [
    ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
    ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
    ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
]

ROW_DUPLICATE_BOARD = [
    ["8", "3", ".", ".", "8", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

COL_DUPLICATE_BOARD = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["5", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

BOX_DUPLICATE_BOARD = [
    ["5", "3", "6", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

EMPTY_BOARD = [["." for _ in range(9)] for _ in range(9)]

TEST_CASES = [
    {"input": (VALID_PARTIAL_BOARD,), "expected": True, "name": "valid_partial_board"},
    {"input": (VALID_COMPLETE_BOARD,), "expected": True, "name": "valid_complete_board"},
    {"input": (ROW_DUPLICATE_BOARD,), "expected": False, "name": "row_duplicate"},
    {"input": (COL_DUPLICATE_BOARD,), "expected": False, "name": "col_duplicate"},
    {"input": (BOX_DUPLICATE_BOARD,), "expected": False, "name": "box_duplicate"},
    {"input": (EMPTY_BOARD,), "expected": True, "name": "all_dots_empty_board"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.isValidSudoku(*case["input"]) == case["expected"]
