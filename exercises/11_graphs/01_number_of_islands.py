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

class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError

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
