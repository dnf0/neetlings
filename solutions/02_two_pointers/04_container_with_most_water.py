"""Container With Most Water.

Curriculum solution module within the Two Pointers chapter.
Evaluates inward two-pointer boundary convergence to maximize bounded rectangular area in O(n) time and O(1) auxiliary space.

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Examples:
    1. Input: height = [1,8,6,2,5,4,8,3,7]
       Output: 49
       Explanation: The vertical lines are represented by array [1,8,6,2,5,4,8,3,7].
       The max area of water the container can contain is 49 (width = 8 - 1 = 7, height = min(8, 7) = 7).
    2. Input: height = [1,1]
       Output: 1
       Explanation: The container formed between indices 0 and 1 has width 1 and height 1, area = 1 * 1 = 1.

Constraints:
    - n == height.length
    - 2 <= n <= 10^5
    - 0 <= height[i] <= 10^4

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

HINTS = [
    "The area between two lines at index `i` and `j` (where `i < j`) is determined by the shorter line: `min(height[i], height[j]) * (j - i)`. How can we search for the maximum area efficiently without testing all pairs in O(n^2)?",
    "Start with the widest possible container by placing two pointers at the outer boundaries: `left = 0` and `right = len(height) - 1`. The width is maximized here.",
    "To find a potentially larger area as width decreases, which pointer should move inward? Moving the taller line cannot increase the area because the height is bounded by the shorter line, and width is smaller. Moving the shorter line is the only way that might yield a taller boundary.",
    "Initialize `left = 0`, `right = len(height) - 1`, and `max_water = 0`. In each iteration while `left < right`: calculate `current_area = min(height[left], height[right]) * (right - left)`, update `max_water = max(max_water, current_area)`. If `height[left] < height[right]`, increment `left`; otherwise, decrement `right`. Return `max_water`.",
]


class Solution:
    def maxArea(self, height: list[int]) -> int:
        """Calculate the maximum area of water a container can store.

        Uses two pointers starting at the outermost lines and converging inward.
        At each step, calculates the rectangular area bounded by the shorter line,
        updates the maximum observed area, and advances the pointer at the shorter
        line because keeping the shorter line cannot yield a larger area with smaller width.
        Operates in O(n) time and O(1) auxiliary space.

        Args:
            height: List of non-negative integers representing vertical line heights.

        Returns:
            The maximum area of water that can be contained.
        """
        # Initialize two pointers at outer boundaries to evaluate maximum width first.
        # Starting with the widest span allows us to prune suboptimal configurations.
        left = 0
        right = len(height) - 1
        max_water = 0

        # Inward convergence loop: evaluate the widest remaining container at each step.
        # As the width (right - left) decreases monotonically, only finding a taller boundary
        # can potentially compensate for the reduced width.
        while left < right:
            width = right - left

            # Determine the limiting height of the container walls.
            # Water level is constrained by the shorter vertical boundary.
            if height[left] < height[right]:
                current_area = height[left] * width
                # Move the left pointer inward since the current left wall has been fully
                # evaluated against all possible opposing walls at this or smaller widths.
                left += 1
            else:
                current_area = height[right] * width
                # Move the right pointer inward since the current right wall has been fully
                # evaluated against all possible opposing walls at this or smaller widths.
                right -= 1

            # Track the maximum water volume observed across all evaluated container pairs.
            if current_area > max_water:
                max_water = current_area

        return max_water


TEST_CASES = [
    {
        "input": ([1, 8, 6, 2, 5, 4, 8, 3, 7],),
        "expected": 49,
        "name": "normal_example",
    },
    {
        "input": ([1, 1],),
        "expected": 1,
        "name": "two_elements",
    },
    {
        "input": ([1, 2, 3, 4, 5, 6, 7, 8],),
        "expected": 16,
        "name": "staircase",
    },
    {
        "input": ([5, 5, 5, 5, 5],),
        "expected": 20,
        "name": "identical_heights",
    },
    {
        "input": ([1, 10000, 10000, 1],),
        "expected": 10000,
        "name": "large_variations",
    },
    {
        "input": ([4, 3, 2, 1, 4],),
        "expected": 16,
        "name": "symmetric_high_ends",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.maxArea(*case["input"]) == case["expected"]
