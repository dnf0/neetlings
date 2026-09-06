"""Longest Consecutive Sequence.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates hash set membership lookups and sequence boundary detection in linear time.

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Examples:
    1. Input: nums = [100,4,200,1,3,2]
       Output: 4
       Explanation: The longest consecutive elements sequence is [1, 2, 3, 4].
       Therefore its length is 4.
    2. Input: nums = [0,3,7,2,5,8,4,6,0,1]
       Output: 9

Constraints:
    - 0 <= nums.length <= 10^5
    - -10^9 <= nums[i] <= 10^9

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        """Find the length of the longest consecutive elements sequence.

        Args:
            nums: List of unsorted integers.

        Returns:
            The length of the longest consecutive elements sequence.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": ([100, 4, 200, 1, 3, 2],), "expected": 4, "name": "standard_unsorted"},
    {"input": ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), "expected": 9, "name": "longer_sequence_with_duplicate"},
    {"input": ([],), "expected": 0, "name": "empty_array"},
    {"input": ([1],), "expected": 1, "name": "single_element"},
    {"input": ([1, 2, 0, 1],), "expected": 3, "name": "duplicate_elements"},
    {"input": ([-5, -4, -3, -2, -1, 0, 1],), "expected": 7, "name": "negative_to_positive"},
    {"input": ([-2, -3, 10, 11, -1, 5, 6, 7, 8],), "expected": 4, "name": "multiple_components_with_negatives"},
    {"input": ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],), "expected": 7, "name": "mixed_sequence_with_gaps"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.longestConsecutive(*case["input"]) == case["expected"]
