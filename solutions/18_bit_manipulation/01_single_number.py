"""Single Number.

Given a non-empty array of integers nums, every element appears twice except for one.
Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

Examples:
    1. Input: nums = [2,2,1]
       Output: 1
    2. Input: nums = [4,1,2,1,2]
       Output: 4
    3. Input: nums = [1]
       Output: 1

Constraints:
    - 1 <= nums.length <= 3 * 10^4
    - -3 * 10^4 <= nums[i] <= 3 * 10^4
    - Each element in the array appears twice except for one element which appears only once.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""


HINTS = [
    "We can solve this with constant extra space using bitwise XOR operator (^).",
    "XORing a number with itself yields 0: a ^ a = 0.",
    "XORing a number with 0 yields the number itself: a ^ 0 = a.",
    "Since XOR is associative and commutative, XORing all elements together will cancel out the duplicates and leave the single number.",
]


class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        res = 0
        for num in nums:
            res ^= num
        return res


TEST_CASES = [
    {"input": ([2, 2, 1],), "expected": 1, "name": "example1"},
    {"input": ([4, 1, 2, 1, 2],), "expected": 4, "name": "example2"},
    {"input": ([1],), "expected": 1, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.singleNumber(*case["input"]) == case["expected"]
