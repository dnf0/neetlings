"""Maximum Subarray.

Given an integer array nums, find the subarray with the largest sum, and return its sum.

Examples:
    1. Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
       Output: 6
       Explanation: The subarray [4,-1,2,1] has the largest sum 6.
    2. Input: nums = [1]
       Output: 1
       Explanation: The subarray [1] has the largest sum 1.
    3. Input: nums = [5,4,-1,7,8]
       Output: 23
       Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": ([-2, 1, -3, 4, -1, 2, 1, -5, 4],), "expected": 6, "name": "example1"},
    {"input": ([1],), "expected": 1, "name": "example2"},
    {"input": ([5, 4, -1, 7, 8],), "expected": 23, "name": "example3"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.maxSubArray(*case["input"]) == case["expected"]
