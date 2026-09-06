"""Reverse Linked List.

Given the head of a singly linked list, reverse the list, and return the reversed list.

Examples:
    1. Input: head = [1,2,3,4,5]
       Output: [5,4,3,2,1]
    2. Input: head = [1,2]
       Output: [2,1]

Constraints:
    - The number of nodes in the list is the range [0, 5000].
    - -5000 <= Node.val <= 5000

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

from neetlings.models import ListNode


class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": (ListNode.from_list([1, 2, 3, 4, 5]),),
        "expected": ListNode.from_list([5, 4, 3, 2, 1]),
        "name": "example1",
    },
    {
        "input": (ListNode.from_list([1, 2]),),
        "expected": ListNode.from_list([2, 1]),
        "name": "example2",
    },
    {
        "input": (ListNode.from_list([]),),
        "expected": None,
        "name": "example3",
    },
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.reverseList(*case["input"]) == case["expected"]
