"""Number of Islands.

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

Examples:
    1. Input: grid = [
         ["1","1","1","1","0"],
         ["1","1","0","1","0"],
         ["1","1","0","0","0"],
         ["0","0","0","0","0"]
       ]
       Output: 1
    2. Input: grid = [
         ["1","1","0","0","0"],
         ["1","1","0","0","0"],
         ["0","0","1","0","0"],
         ["0","0","0","1","1"]
       ]
       Output: 3

Constraints:
    - m == grid.length
    - n == grid[i].length
    - 1 <= m, n <= 300
    - grid[i][j] is '0' or '1'.

Target:
    - Time Complexity: O(m * n)
    - Space Complexity: O(m * n)
"""


HINTS = [
    "Represent the grid as a graph where each '1' (land) is a node connected to adjacent land cells.",
    "Iterate through each cell in the grid. When we find '1', it triggers a DFS/BFS to visit the entire island.",
    "Increment the island count when a new island is found.",
    "During DFS/BFS, mark visited land cells as '0' to avoid double counting and infinite loops.",
]


class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        islands = 0

        def dfs(r: int, c: int) -> None:
            if r < 0 or c < 0 or r >= m or c >= n or grid[r][c] != "1":
                return
            grid[r][c] = "0"  # Mark as visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1":
                    dfs(r, c)
                    islands += 1

        return islands


TEST_CASES = [
    {
        "input": (
            [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ],
        ),
        "expected": 1,
        "name": "example1",
    },
    {
        "input": (
            [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ],
        ),
        "expected": 3,
        "name": "example2",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        grid_copy = [row[:] for row in case["input"][0]]
        assert sol.numIslands(grid_copy) == case["expected"]
