"""Trapping Rain Water.

Curriculum exercise module within the Two Pointers chapter.
Evaluates inward two-pointer convergence with running elevation bounds
to compute trapped rainwater in O(n) time and strictly O(1) auxiliary space.

Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

Examples:
    1. Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
       Output: 6
       Explanation: The elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].
       In this case, 6 units of rain water are trapped.
    2. Input: height = [4,2,0,3,2,5]
       Output: 9
       Explanation: 9 units of rain water are trapped between elevation bars.

Constraints:
    - n == height.length
    - 0 <= n <= 2 * 10^4
    - 0 <= height[i] <= 10^5

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1) auxiliary
"""

class Solution:
    def trap(self, height: list[int]) -> int:
        """Calculate total amount of rainwater trapped between elevation bars.

        Args:
            height: List of non-negative integers representing elevation map.

        Returns:
            Total units of trapped rainwater.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],),
        "expected": 6,
        "name": "standard_leetcode",
    },
    {
        "input": ([0, 0, 0],),
        "expected": 0,
        "name": "flat_terrain",
    },
    {
        "input": ([5, 4, 3, 2, 1],),
        "expected": 0,
        "name": "strictly_descending",
    },
    {
        "input": ([1, 2, 3, 4, 5],),
        "expected": 0,
        "name": "strictly_ascending",
    },
    {
        "input": ([3, 0, 3],),
        "expected": 3,
        "name": "v_valley",
    },
    {
        "input": ([],),
        "expected": 0,
        "name": "empty",
    },
    {
        "input": ([5],),
        "expected": 0,
        "name": "single_element",
    },
    {
        "input": ([4, 2, 0, 3, 2, 5],),
        "expected": 9,
        "name": "multiple_basins",
    },
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.trap(*case["input"]) == case["expected"]
