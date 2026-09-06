"""Trapping Rain Water.

Curriculum solution module within the Two Pointers chapter.
Evaluates inward two-pointer convergence with running elevation bounds
to compute trapped rainwater in O(n) time and strictly O(1) auxiliary space.

Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.

Examples:
    1. Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
       Output: 6
       Explanation: The elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].
       In this case, 6 units of rain water are trapped.
    2. Input: height = [4,2,0,3,2,5]
       Output: 9
       Explanation: 9 units of rain water are trapped between elevation bars.

Constraints:
    - n == height.length
    - 0 <= n <= 2 * 10^4
    - 0 <= height[i] <= 10^5

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1) auxiliary
"""

HINTS = [
    "The water trapped directly above any bar at index `i` is determined by `min(max_left, max_right) - height[i]`, where `max_left` is the tallest bar to the left and `max_right` is the tallest bar to the right (if this value is positive).",
    "While computing prefix and suffix maximum arrays solves this in O(n) time, it requires O(n) extra space. Can two pointers converging from both ends track running maximums in O(1) space?",
    "If `left_max <= right_max`, we know for certain that the water level at the `left` pointer is bottlenecked by `left_max`, regardless of what lies between `left` and `right`. Therefore, we can safely compute trapped water at `left` and advance `left`.",
    "Initialize `left = 0`, `right = len(height) - 1`, `left_max = height[left]`, `right_max = height[right]`, `total = 0`. While `left < right`: if `left_max <= right_max`, increment `left`, update `left_max = max(left_max, height[left])`, and add `left_max - height[left]` to `total`. Otherwise, decrement `right`, update `right_max = max(right_max, height[right])`, and add `right_max - height[right]` to `total`. Return `total`.",
]


class Solution:
    def trap(self, height: list[int]) -> int:
        """Calculate total amount of rainwater trapped between elevation bars.

        Uses two-pointer inward convergence with running left_max and right_max trackers.
        Because water trapped at bar i is min(left_max, right_max) - height[i], whichever
        side has the smaller maximum is the bottleneck, allowing water accumulation at that
        pointer without needing the full opposite profile.
        Achieves O(n) time and strictly O(1) auxiliary space.

        Args:
            height: List of non-negative integers representing elevation map.

        Returns:
            Total units of trapped rainwater.
        """
        # Guard clause: terrain with fewer than 3 bars cannot form a container to hold water.
        # Fallback to 0 is physically correct because at least two boundary walls and one floor are required.
        if len(height) < 3:
            return 0

        # Initialize pointers at both extremes and track running boundary peaks.
        # O(1) scalar variables replace O(n) prefix/suffix maximum memory arrays.
        left = 0
        right = len(height) - 1
        left_max = height[left]
        right_max = height[right]
        total_water = 0

        # Inward convergence: move the pointer with the smaller boundary maximum.
        # The smaller maximum is guaranteed to be the limiting factor for water height at that position,
        # regardless of any taller bars that might exist further inward.
        while left < right:
            if left_max <= right_max:
                left += 1
                # Update running maximum elevation seen from the left.
                if height[left] > left_max:
                    left_max = height[left]
                # Water trapped above bar is the difference between peak wall height and bar elevation.
                else:
                    total_water += left_max - height[left]
            else:
                right -= 1
                # Update running maximum elevation seen from the right.
                if height[right] > right_max:
                    right_max = height[right]
                # Water trapped above bar is the difference between peak wall height and bar elevation.
                else:
                    total_water += right_max - height[right]

        return total_water


TEST_CASES = [
    {
        "input": ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],),
        "expected": 6,
        "name": "standard_leetcode",
    },
    {
        "input": ([0, 0, 0],),
        "expected": 0,
        "name": "flat_terrain",
    },
    {
        "input": ([5, 4, 3, 2, 1],),
        "expected": 0,
        "name": "strictly_descending",
    },
    {
        "input": ([1, 2, 3, 4, 5],),
        "expected": 0,
        "name": "strictly_ascending",
    },
    {
        "input": ([3, 0, 3],),
        "expected": 3,
        "name": "v_valley",
    },
    {
        "input": ([],),
        "expected": 0,
        "name": "empty",
    },
    {
        "input": ([5],),
        "expected": 0,
        "name": "single_element",
    },
    {
        "input": ([4, 2, 0, 3, 2, 5],),
        "expected": 9,
        "name": "multiple_basins",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.trap(*case["input"]) == case["expected"]
