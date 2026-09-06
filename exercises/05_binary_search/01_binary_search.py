"""Binary Search.

Given an array of integers nums which is sorted in ascending order, and an integer target,
write a function to search target in nums. If target exists, then return its index.
Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Examples:
    1. Input: nums = [-1,0,3,5,9,12], target = 9
       Output: 4
       Explanation: 9 exists in nums and its index is 4.
    2. Input: nums = [-1,0,3,5,9,12], target = 2
       Output: -1
       Explanation: 2 does not exist in nums so return -1.

Constraints:
    - 1 <= nums.length <= 10^4
    - -10^4 < nums[i], target < 10^4
    - All the integers in nums are unique.
    - nums is sorted in ascending order.

Target:
    - Time Complexity: O(log n)
    - Space Complexity: O(1)
"""

HINTS = [
    "Maintain two pointers: l (left) starting at 0 and r (right) starting at len(nums) - 1.",
    "While l <= r, calculate the middle index m = l + (r - l) // 2.",
    "Compare nums[m] with the target. If they are equal, return m.",
    "If nums[m] < target, search the right half by setting l = m + 1. If nums[m] > target, search the left half by setting r = m - 1. If not found after loop, return -1.",
]


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {"input": ([-1, 0, 3, 5, 9, 12], 9), "expected": 4, "name": "example1"},
    {"input": ([-1, 0, 3, 5, 9, 12], 2), "expected": -1, "name": "example2"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.search(*case["input"]) == case["expected"]
