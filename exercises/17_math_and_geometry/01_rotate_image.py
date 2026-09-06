"""Rotate Image.

You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly.
DO NOT allocate another 2D matrix and do the rotation.

Examples:
    1. Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
       Output: [[7,4,1],[8,5,2],[9,6,3]]
    2. Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,2,15],[15,14,12,16]]
       Output: [[15,13,2,5],[14,3,4,1],[12,2,8,9],[16,15,10,11]]

Constraints:
    - n == matrix.length == matrix[i].length
    - 1 <= n <= 20
    - -1000 <= matrix[i][j] <= 1000

Target:
    - Time Complexity: O(n^2)
    - Space Complexity: O(1)
"""

class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": ([[1, 2, 3], [4, 5, 6], [7, 8, 9]],),
        "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        "name": "example1",
    },
    {
        "input": ([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 2, 15], [15, 14, 12, 16]],),
        "expected": [[15, 13, 2, 5], [14, 3, 4, 1], [12, 2, 8, 9], [16, 15, 10, 11]],
        "name": "example2",
    },
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        matrix = [row[:] for row in case["input"][0]]
        sol.rotate(matrix)
        assert matrix == case["expected"]
