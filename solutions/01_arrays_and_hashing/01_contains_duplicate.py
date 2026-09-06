"""Contains Duplicate.

Given an integer array nums, return true if any value appears at least twice in the array,
and return false if every element is distinct.

Examples:
    1. Input: nums = [1,2,3,1]
       Output: true
    2. Input: nums = [1,2,3,4]
       Output: false

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^9 <= nums[i] <= 10^9

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

HINTS = [
    "A hash set can keep track of elements we have already seen.",
    "As we iterate through the list, check if the current element is in the set.",
    "If it is in the set, we found a duplicate, so return True.",
    "Otherwise, add the element to the set and continue. If the loop finishes, return False.",
]


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "example1"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "example2"},
    {"input": ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), "expected": True, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.containsDuplicate(*case["input"]) == case["expected"]
