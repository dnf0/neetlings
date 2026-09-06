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

import heapq
from collections import defaultdict

HINTS = [
    "This is a shortest path problem in a weighted directed graph. We can use Dijkstra's Algorithm.",
    "Build an adjacency list mapping each source node to a list of its neighbors and edge weights: adj[u].append((v, w)).",
    "Use a min-heap to keep track of nodes to visit: (time, node), initialized with (0, k).",
    "Maintain a visited set. If the number of visited nodes equals n after processing, return the max time. If heap is empty and we haven't visited all nodes, return -1.",
]


class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))

        min_heap = [(0, k)]
        visited = set()
        t = 0

        while min_heap:
            w1, n1 = heapq.heappop(min_heap)
            if n1 in visited:
                continue
            visited.add(n1)
            t = max(t, w1)

            for n2, w2 in adj[n1]:
                if n2 not in visited:
                    heapq.heappush(min_heap, (w1 + w2, n2))

        return t if len(visited) == n else -1


TEST_CASES = [
    {"input": ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), "expected": 2, "name": "example1"},
    {"input": ([[1, 2, 1]], 2, 1), "expected": 1, "name": "example2"},
    {"input": ([[1, 2, 1]], 2, 2), "expected": -1, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.networkDelayTime(*case["input"]) == case["expected"]
