"""Container With Most Water.

Curriculum exercise module within the Two Pointers chapter.
Evaluates inward two-pointer boundary convergence to maximize bounded rectangular area in O(n) time and O(1) auxiliary space.

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Examples:
    1. Input: height = [1,8,6,2,5,4,8,3,7]
       Output: 49
       Explanation: The vertical lines are represented by array [1,8,6,2,5,4,8,3,7].
       The max area of water the container can contain is 49 (width = 8 - 1 = 7, height = min(8, 7) = 7).
    2. Input: height = [1,1]
       Output: 1
       Explanation: The container formed between indices 0 and 1 has width 1 and height 1, area = 1 * 1 = 1.

Constraints:
    - n == height.length
    - 2 <= n <= 10^5
    - 0 <= height[i] <= 10^4

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

class Solution:
    def maxArea(self, height: list[int]) -> int:
        """Calculate the maximum area of water a container can store.

        Args:
            height: List of non-negative integers representing vertical line heights.

        Returns:
            The maximum area of water that can be contained.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": ([1, 8, 6, 2, 5, 4, 8, 3, 7],),
        "expected": 49,
        "name": "normal_example",
    },
    {
        "input": ([1, 1],),
        "expected": 1,
        "name": "two_elements",
    },
    {
        "input": ([1, 2, 3, 4, 5, 6, 7, 8],),
        "expected": 16,
        "name": "staircase",
    },
    {
        "input": ([5, 5, 5, 5, 5],),
        "expected": 20,
        "name": "identical_heights",
    },
    {
        "input": ([1, 10000, 10000, 1],),
        "expected": 10000,
        "name": "large_variations",
    },
    {
        "input": ([4, 3, 2, 1, 4],),
        "expected": 16,
        "name": "symmetric_high_ends",
    },
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.maxArea(*case["input"]) == case["expected"]
