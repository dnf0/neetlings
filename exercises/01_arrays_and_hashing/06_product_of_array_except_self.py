"""Product of Array Except Self.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates prefix and postfix accumulator patterns without using division.

Given an integer array nums, return an array answer such that answer[i] is equal
to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Examples:
    1. Input: nums = [1,2,3,4]
       Output: [24,12,8,6]
    2. Input: nums = [-1,1,0,-3,3]
       Output: [0,0,9,0,0]

Constraints:
    - 2 <= nums.length <= 10^5
    - -30 <= nums[i] <= 30
    - The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1) auxiliary space (output array does not count toward space)
"""

HINTS = [
    "If division were allowed, we could compute the total product and divide by nums[i]. Without division, how can we compute the product of all elements to the left and all elements to the right of each position?",
    "Prefix and postfix (suffix) products. For any element at index i, its answer is (product of elements before index i) * (product of elements after index i).",
    "Instead of allocating separate prefix and postfix arrays (which would use O(n) auxiliary space), store the prefix products directly in the output array during a left-to-right pass, then multiply by a running postfix accumulator during a right-to-left pass. Watch out for zeros and negative numbers.",
    "Initialize `res = [1] * len(nums)`. In the first loop, maintain prefix product `prefix = 1` and set `res[i] = prefix`, then `prefix *= nums[i]`. In the second loop going backwards, maintain `postfix = 1` and multiply `res[i] *= postfix`, then `postfix *= nums[i]`. Return `res`.",
]


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        """Compute an array where answer[i] is the product of all elements except nums[i].

        Args:
            nums: List of integers.

        Returns:
            List of integers where each index contains the product of all other elements.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {"input": ([1, 2, 3, 4],), "expected": [24, 12, 8, 6], "name": "standard_positive"},
    {"input": ([-1, 1, 0, -3, 3],), "expected": [0, 0, 9, 0, 0], "name": "single_zero_with_negatives"},
    {"input": ([0, 0],), "expected": [0, 0], "name": "multiple_zeros_boundary"},
    {"input": ([2, 3],), "expected": [3, 2], "name": "boundary_minimum_length_two"},
    {"input": ([-1, -2, -3, -4],), "expected": [-24, -12, -8, -6], "name": "all_negative_numbers"},
    {"input": ([0, 4, 0],), "expected": [0, 0, 0], "name": "multiple_zeros_separated"},
    {"input": ([5, 0, 2],), "expected": [0, 10, 0], "name": "single_zero_in_middle"},
    {"input": ([1, -1],), "expected": [-1, 1], "name": "two_elements_mixed_signs"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.productExceptSelf(*case["input"]) == case["expected"]
