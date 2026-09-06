"""Top K Frequent Elements.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates frequency counting and non-comparison bucket sorting.

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Examples:
    1. Input: nums = [1,1,1,2,2,3], k = 2
       Output: [1,2]
    2. Input: nums = [1], k = 1
       Output: [1]

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - k is in the range [1, the number of unique elements in the array].
    - It is guaranteed that the answer is unique.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

HINTS = [
    "A standard sort on frequencies takes O(n log n), and a heap takes O(n log k). Can we achieve O(n) using the bounded nature of frequencies?",
    "Since an element can appear at most len(nums) times, we can use Bucket Sort where the bucket index represents the occurrence count.",
    "Multiple elements can share the same frequency, so each bucket should be a list. Empty frequencies will have empty lists. Scan buckets in descending order from len(nums) down to 1.",
    "Count frequencies into a dictionary. Allocate `buckets = [[] for _ in range(len(nums) + 1)]` and append each element to `buckets[frequency]`. Traverse buckets in reverse and accumulate elements until k items are collected.",
]


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        """Find the k most frequent elements in nums.

        Args:
            nums: List of integers.
            k: Number of most frequent elements to return.

        Returns:
            List of k most frequent elements.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {
        "input": ([1, 1, 1, 2, 2, 3], 2),
        "expected": [1, 2],
        "name": "standard_top_k",
    },
    {
        "input": ([1], 1),
        "expected": [1],
        "name": "single_element",
    },
    {
        "input": ([4, 1, -1, 2, -1, 2, 3], 2),
        "expected": [-1, 2],
        "name": "negative_numbers_and_ties",
    },
    {
        "input": ([1, 2], 2),
        "expected": [1, 2],
        "name": "k_equals_unique_elements",
    },
    {
        "input": ([7, 7, 7, 7, 8, 8, 8, 9, 9, 10], 3),
        "expected": [7, 8, 9],
        "name": "distinct_descending_frequencies",
    },
    {
        "input": ([-1, -1], 1),
        "expected": [-1],
        "name": "negative_duplicate",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert set(sol.topKFrequent(*case["input"])) == set(case["expected"])
