"""Invert Binary Tree.

Given the root of a binary tree, invert the tree, and return its root.

Examples:
    1. Input: root = [4,2,7,1,3,6,9]
       Output: [4,7,2,9,6,3,1]
    2. Input: root = [2,1,3]
       Output: [2,3,1]

Constraints:
    - The number of nodes in the tree is in the range [0, 100].
    - -100 <= Node.val <= 100

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(h) where h is height of tree (recursion stack)
"""

from neetlings.models import TreeNode

HINTS = [
    "Think about how to solve this recursively. For any given node, we want to swap its left and right children.",
    "Invert the left subtree and right subtree recursively.",
    "Swap the left and right pointers of the current node.",
    "Base case: if the root is None, return None. Finally, return root.",
]


class Solution:
    def invertTree(self, root: TreeNode | None) -> TreeNode | None:
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {
        "input": (TreeNode.from_level_order([4, 2, 7, 1, 3, 6, 9]),),
        "expected": TreeNode.from_level_order([4, 7, 2, 9, 6, 3, 1]),
        "name": "example1",
    },
    {
        "input": (TreeNode.from_level_order([2, 1, 3]),),
        "expected": TreeNode.from_level_order([2, 3, 1]),
        "name": "example2",
    },
    {
        "input": (TreeNode.from_level_order([]),),
        "expected": None,
        "name": "example3",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.invertTree(*case["input"]) == case["expected"]
