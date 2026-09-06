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

class Solution:
    def solve(self, k: int, nums: list[int], val_adds: list[int]) -> list[int]:
        # TODO: Implement your solution here
        raise NotImplementedError

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
