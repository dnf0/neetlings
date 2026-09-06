"""3Sum.

Curriculum exercise module within the Two Pointers chapter.
Evaluates sorting combined with two-pointer inward scanning to find unique triplets.

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Examples:
    1. Input: nums = [-1,0,1,2,-1,-4]
       Output: [[-1,-1,2],[-1,0,1]]
       Explanation:
       nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
       nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
       nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
       The distinct triplets are [-1,0,1] and [-1,-1,2].
       Notice that the order of the output and the order of the triplets does not matter.
    2. Input: nums = [0,1,1]
       Output: []
       Explanation: The only possible triplet does not sum up to 0.
    3. Input: nums = [0,0,0]
       Output: [[0,0,0]]
       Explanation: The only possible triplet sums up to 0.

Constraints:
    - 3 <= nums.length <= 3000
    - -10^5 <= nums[i] <= 10^5

Target:
    - Time Complexity: O(n^2)
    - Space Complexity: O(1) auxiliary (excluding output space)
"""

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """Find all unique triplets summing to zero.

        Args:
            nums: List of integers.

        Returns:
            List of unique triplets [a, b, c] such that a + b + c == 0.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": ([-1, 0, 1, 2, -1, -4],),
        "expected": [[-1, -1, 2], [-1, 0, 1]],
        "name": "standard_example",
    },
    {
        "input": ([0, 1, 1],),
        "expected": [],
        "name": "no_triplets",
    },
    {
        "input": ([0, 0, 0],),
        "expected": [[0, 0, 0]],
        "name": "all_zeros",
    },
    {
        "input": ([0, 0, 0, 0],),
        "expected": [[0, 0, 0]],
        "name": "multiple_zeros",
    },
    {
        "input": ([-1, -1, -1, 2, 2],),
        "expected": [[-1, -1, 2]],
        "name": "duplicate_numbers",
    },
    {
        "input": ([-2, 0, 1, 1, 2],),
        "expected": [[-2, 0, 2], [-2, 1, 1]],
        "name": "negative_numbers",
    },
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sorted([sorted(t) for t in sol.threeSum(*case["input"])]) == sorted(
            [sorted(t) for t in case["expected"]]
        )
