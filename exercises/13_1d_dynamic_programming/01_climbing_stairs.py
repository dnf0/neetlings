"""Climbing Stairs.

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Examples:
    1. Input: n = 2
       Output: 2
       Explanation: There are two ways to climb to the top.
                    1. 1 step + 1 step
                    2. 2 steps
    2. Input: n = 3
       Output: 3
       Explanation: There are three ways to climb to the top.
                    1. 1 step + 1 step + 1 step
                    2. 1 step + 2 steps
                    3. 2 steps + 1 step

Constraints:
    - 1 <= n <= 45

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

class Solution:
    def climbStairs(self, n: int) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": (2,), "expected": 2, "name": "example1"},
    {"input": (3,), "expected": 3, "name": "example2"},
    {"input": (5,), "expected": 8, "name": "example3"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.climbStairs(*case["input"]) == case["expected"]
