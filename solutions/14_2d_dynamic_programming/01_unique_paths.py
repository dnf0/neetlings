"""Unique Paths.

There is a robot on an m x n grid. The robot is initially located at the top-left corner
(i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]).
The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can
take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10^9.

Examples:
    1. Input: m = 3, n = 7
       Output: 28
    2. Input: m = 3, n = 2
       Output: 3
       Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
                    1. Right -> Down -> Down
                    2. Down -> Down -> Right
                    3. Down -> Right -> Down

Constraints:
    - 1 <= m, n <= 100

Target:
    - Time Complexity: O(m * n)
    - Space Complexity: O(n)
"""


HINTS = [
    "Let dp[r][c] be the number of unique paths to cell (r, c). We can reach it from the top (r-1, c) or left (r, c-1).",
    "The recurrence relation is: dp[r][c] = dp[r-1][c] + dp[r][c-1].",
    "Initialize a 1D row array of size n with 1s, since there is only 1 path to any cell in the first row.",
    "Iterate row by row (starting from second row) and update the column values: row[c] += row[c-1].",
]


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n
        for _ in range(m - 1):
            new_row = [1] * n
            for c in range(1, n):
                new_row[c] = new_row[c - 1] + row[c]
            row = new_row
        return row[-1]


TEST_CASES = [
    {"input": (3, 7), "expected": 28, "name": "example1"},
    {"input": (3, 2), "expected": 3, "name": "example2"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.uniquePaths(*case["input"]) == case["expected"]
