"""Two Sum.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates complement-lookup patterns using hash maps.

Given an array of integers nums and an integer target, return indices of the two
numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not
use the same element twice. You can return the answer in any order.

Examples:
    1. Input: nums = [2,7,11,15], target = 9
       Output: [0,1]
       Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
    2. Input: nums = [3,2,4], target = 6
       Output: [1,2]
    3. Input: nums = [3,3], target = 6
       Output: [0,1]

Constraints:
    - 2 <= nums.length <= 10^4
    - -10^9 <= nums[i] <= 10^9
    - -10^9 <= target <= 10^9
    - Only one valid answer exists.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

HINTS = [
    "A brute-force pair comparison takes O(n^2) time. Can we find the complementary value in O(1) time?",
    "For each number x, the value needed to reach target is exactly `target - x`. A hash map can record previously seen numbers and their indices.",
    "Inspect each element and check if its complement is already in the hash map before adding the current element. This ensures you never use the same element twice.",
    "Initialize an empty dictionary `seen = {}`. Loop through `enumerate(nums)`. If `target - num` in `seen`, return `[seen[target - num], idx]`. Otherwise, store `seen[num] = idx`.",
]


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """Find indices of two numbers that sum up to target.

        Args:
            nums: List of integers.
            target: Target sum.

        Returns:
            List containing the two 0-based indices.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {"input": ([2, 7, 11, 15], 9), "expected": [0, 1], "name": "basic_positive"},
    {"input": ([3, 2, 4], 6), "expected": [1, 2], "name": "unsorted_indices"},
    {"input": ([3, 3], 6), "expected": [0, 1], "name": "duplicate_elements"},
    {"input": ([-1, -2, -3, -4, -5], -8), "expected": [2, 4], "name": "negative_numbers"},
    {"input": ([0, 4, 3, 0], 0), "expected": [0, 3], "name": "zeros"},
    {"input": ([-3, 4, 3, 90], 0), "expected": [0, 2], "name": "mixed_signs"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.twoSum(*case["input"]) == case["expected"]
