"""Kth Largest Element in a Stream.

Design a class to find the kth largest element in a stream. Note that it is the kth
largest element in the sorted order, not the kth distinct element.

Implement the KthLargest class wrapped within Solution:
    - solve(self, k: int, nums: list[int], val_adds: list[int]) -> list[int]
      Initializes the stream with k and nums, then calls add(val) for each value in val_adds,
      returning the list of results.

Examples:
    1. Input: k = 3, nums = [4, 5, 8, 2], val_adds = [3, 5, 10, 9, 4]
       Output: [4, 5, 5, 8, 8]
       Explanation:
       - kth_largest = KthLargest(3, [4, 5, 8, 2])
       - add(3) -> returns 4 (stream: [2, 3, 4, 5, 8])
       - add(5) -> returns 5 (stream: [2, 3, 4, 5, 5, 8])
       - add(10) -> returns 5 (stream: [2, 3, 4, 5, 5, 8, 10])
       - add(9) -> returns 8 (stream: [2, 3, 4, 5, 5, 8, 9, 10])
       - add(4) -> returns 8 (stream: [2, 3, 4, 4, 5, 5, 8, 9, 10])

Constraints:
    - 1 <= k <= 10^4
    - 0 <= nums.length <= 10^4
    - -10^4 <= nums[i], val <= 10^4
    - At most 10^4 calls in total will be made to add.

Target:
    - Time Complexity:
        - Initialization: O(n log k)
        - Add: O(log k)
    - Space Complexity: O(k)
"""

import heapq

HINTS = [
    "A min-heap is ideal for maintaining the k largest elements in a stream.",
    "Initialize a min-heap with the starting elements. While its size exceeds k, pop the minimum elements.",
    "For each new value, push it onto the min-heap.",
    "If the size of the heap exceeds k, pop the minimum element. The Kth largest element is then at the top of the min-heap (heap[0]).",
]


class KthLargest:
    def __init__(self, k: int, nums: list[int]) -> None:
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]


class Solution:
    def solve(self, k: int, nums: list[int], val_adds: list[int]) -> list[int]:
        kth = KthLargest(k, nums)
        return [kth.add(v) for v in val_adds]


TEST_CASES = [
    {
        "input": (3, [4, 5, 8, 2], [3, 5, 10, 9, 4]),
        "expected": [4, 5, 5, 8, 8],
        "name": "example1",
    }
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.solve(*case["input"]) == case["expected"]
