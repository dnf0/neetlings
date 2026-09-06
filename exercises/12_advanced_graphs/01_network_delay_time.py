"""Network Delay Time.

You are given a network of n nodes, labeled from 1 to n. You are also given times,
a list of directed travel times as directed edges times[i] = (ui, vi, wi), where ui is the
source node, vi is the target node, and wi is the time it takes for a signal to travel from
source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes
to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.

Examples:
    1. Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
       Output: 2
    2. Input: times = [[1,2,1]], n = 2, k = 1
       Output: 1
    3. Input: times = [[1,2,1]], n = 2, k = 2
       Output: -1

Constraints:
    - 1 <= k <= n <= 100
    - 1 <= times.length <= 6000
    - times[i].length == 3
    - 1 <= ui, vi <= n
    - ui != vi
    - 0 <= wi <= 100
    - All the pairs (ui, vi) are unique. (i.e., no multiple edges)

Target:
    - Time Complexity: O(E log V) where E is length of times, V is n
    - Space Complexity: O(V + E)
"""

class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), "expected": 2, "name": "example1"},
    {"input": ([[1, 2, 1]], 2, 1), "expected": 1, "name": "example2"},
    {"input": ([[1, 2, 1]], 2, 2), "expected": -1, "name": "example3"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.networkDelayTime(*case["input"]) == case["expected"]
