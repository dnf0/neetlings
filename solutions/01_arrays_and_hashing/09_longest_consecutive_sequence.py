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

HINTS = [
    "Sorting the array takes O(n log n), but we need O(n). How can we achieve O(1) lookups to check if consecutive numbers exist?",
    "Store all numbers in a hash set. Only start counting consecutive elements from the *beginning* of a sequence.",
    "A number is the beginning of a sequence if `num - 1` is not in the set. If `num - 1` exists, skip it—it will be counted from its true origin.",
    "Convert `nums` into a set `num_set = set(nums)`. For each `num` in `num_set`, if `num - 1 not in num_set`, traverse forward with a while loop checking `num + 1, num + 2, ...` and update `max_streak`. Handle empty input `[]` by returning 0.",
]


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        """Find the length of the longest consecutive elements sequence in O(n) time.

        Uses a hash set to achieve O(1) membership queries. Streak counting is strictly
        initiated at sequence origins (numbers where num - 1 is absent from the set),
        ensuring each consecutive number is visited at most twice for a total O(n) runtime.

        Args:
            nums: List of unsorted integers.

        Returns:
            The length of the longest consecutive elements sequence.
        """
        # Guard clause: an empty array contains zero sequence elements.
        # Short-circuits immediately to avoid allocating an empty hash set.
        if not nums:
            return 0

        # Construct hash set for O(1) average-time lookups.
        # Deduplication naturally ignores duplicate numbers in consecutive runs.
        num_set = set(nums)
        longest_streak = 0

        for num in num_set:
            # Check whether `num` is the first element of a consecutive sequence.
            # If `num - 1` exists, `num` is part of a streak and will be visited
            # when traversing from that streak's true lowest starting element.
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                # Expand forward along the consecutive chain while subsequent numbers exist.
                # Each number across all streaks is inspected at most once in this inner loop.
                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                # Track the maximum streak length discovered across all sequence components.
                if current_streak > longest_streak:
                    longest_streak = current_streak

        return longest_streak


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
