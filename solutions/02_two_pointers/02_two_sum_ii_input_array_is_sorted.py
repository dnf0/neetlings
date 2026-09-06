"""Two Sum II - Input Array Is Sorted.

Curriculum solution module within the Two Pointers chapter.
Evaluates two-pointer inward convergence on sorted arrays with O(1) auxiliary space.

Given a 1-indexed array of integers numbers that is already sorted in
non-decreasing order, find two numbers such that they add up to a specific
target number. Let these two numbers be numbers[index1] and numbers[index2]
where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an
integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not
use the same element twice. Your solution must use only constant extra space.

Examples:
    1. Input: numbers = [2,7,11,15], target = 9
       Output: [1,2]
       Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
    2. Input: numbers = [2,3,4], target = 6
       Output: [1,3]
       Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
    3. Input: numbers = [-1,0], target = -1
       Output: [1,2]
       Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

Constraints:
    - 2 <= numbers.length <= 3 * 10^4
    - -1000 <= numbers[i] <= 1000
    - numbers is sorted in non-decreasing order.
    - -1000 <= target <= 1000
    - The tests are generated such that there is exactly one solution.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

HINTS = [
    "The input array is already sorted in non-decreasing order. How can we leverage sorted order without extra space?",
    "Consider placing one pointer at the beginning (`left = 0`) and one at the end (`right = len(numbers) - 1`). Compute the sum of the elements at these pointers.",
    "If the current sum is smaller than `target`, moving `left` to the right increases the sum. If the sum is larger than `target`, moving `right` to the left decreases the sum.",
    "Loop `while left < right:`. Calculate `total = numbers[left] + numbers[right]`. If `total == target`, return `[left + 1, right + 1]` (remember 1-based indexing). If `total < target`, increment `left`. Otherwise, decrement `right`.",
]


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        """Find 1-indexed positions of two numbers summing to target.

        Uses two-pointer inward convergence on the pre-sorted array to locate
        the unique pair in O(n) time and O(1) auxiliary space.

        Args:
            numbers: 1-indexed list of integers sorted in non-decreasing order.
            target: Target sum.

        Returns:
            List containing the two 1-based indices [index1, index2].

        Raises:
            ValueError: If no pair sums to target (violating problem constraints).
        """
        # Initialize two pointers at opposite ends of the sorted array.
        # Starting at the extrema allows deterministic elimination of impossible values.
        left = 0
        right = len(numbers) - 1

        # Inward convergence loop searching for target sum.
        # Since exactly one solution is guaranteed, the pointers will meet the solution before crossing.
        while left < right:
            current_sum = numbers[left] + numbers[right]

            # Matching pair found: convert 0-based indices to 1-based indexing as required by problem.
            if current_sum == target:
                return [left + 1, right + 1]

            # Current sum is deficient: advance left pointer to larger value to increase sum.
            if current_sum < target:
                left += 1
            # Current sum is excessive: retreat right pointer to smaller value to decrease sum.
            else:
                right -= 1

        # Defensive guard clause triggered only if inputs violate the guarantee of exactly one solution.
        raise ValueError("No two sum solution exists for given target")


TEST_CASES = [
    {"input": ([2, 7, 11, 15], 9), "expected": [1, 2], "name": "normal"},
    {"input": ([2, 3, 4], 6), "expected": [1, 3], "name": "three_elements"},
    {"input": ([-1, 0], -1), "expected": [1, 2], "name": "single_pair"},
    {"input": ([-5, -3, -1, 0, 2, 4], -4), "expected": [2, 3], "name": "negative_numbers"},
    {"input": ([0, 0, 3, 4], 0), "expected": [1, 2], "name": "zeros"},
    {"input": ([-1000, -500, 2, 7, 1000], 0), "expected": [1, 5], "name": "large_differences"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.twoSum(*case["input"]) == case["expected"]
