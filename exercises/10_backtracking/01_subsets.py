"""Subsets.

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

Examples:
    1. Input: nums = [1,2,3]
       Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    2. Input: nums = [0]
       Output: [[],[0]]

Constraints:
    - 1 <= nums.length <= 10
    - -10 <= nums[i] <= 10
    - All the numbers of nums are unique.

Target:
    - Time Complexity: O(n * 2^n)
    - Space Complexity: O(n) (recursion stack)
"""

class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": ([1, 2, 3],),
        "expected": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]],
        "name": "example1",
    },
    {"input": ([0],), "expected": [[], [0]], "name": "example2"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        actual = sol.subsets(*case["input"])
        expected = case["expected"]
        assert sorted(sorted(x) for x in actual) == sorted(sorted(x) for x in expected)
        # Verify that all subsets are unique
        serialized_actual = [tuple(sorted(x)) for x in actual]
        assert len(serialized_actual) == len(set(serialized_actual))
