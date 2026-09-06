"""Insert Interval.

You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi]
represent the start and the end of the ith interval and intervals is sorted in ascending order by starti.
You are also given an interval newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti
and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion.

Examples:
    1. Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
       Output: [[1,5],[6,9]]
    2. Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
       Output: [[1,2],[3,10],[12,16]]
       Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].

Constraints:
    - 0 <= intervals.length <= 10^4
    - intervals[i].length == 2
    - 0 <= starti <= endi <= 10^5
    - intervals is sorted by starti in ascending order.
    - newInterval.length == 2
    - 0 <= start <= end <= 10^5

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""


HINTS = [
    "The intervals are already sorted. We can iterate through and handle three cases relative to newInterval.",
    "If the current interval ends before newInterval starts, add the current interval to the result.",
    "If the current interval starts after newInterval ends, we can insert newInterval (if not done yet) and add all remaining intervals.",
    "If there is an overlap, merge them by updating newInterval = [min(start, newStart), max(end, newEnd)].",
]


class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {
        "input": ([[1, 3], [6, 9]], [2, 5]),
        "expected": [[1, 5], [6, 9]],
        "name": "example1",
    },
    {
        "input": ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
        "expected": [[1, 2], [3, 10], [12, 16]],
        "name": "example2",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.insert(*case["input"]) == case["expected"]
