"""Valid Parentheses.

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

Examples:
    1. Input: s = "()"
       Output: true
    2. Input: s = "()[]{}"
       Output: true
    3. Input: s = "(]"
       Output: false

Constraints:
    - 1 <= s.length <= 10^4
    - s consists of parentheses only '()[]{}'.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

HINTS = [
    "A stack is perfect for this LIFO (Last-In-First-Out) problem.",
    "Use a dictionary to map closing brackets to their corresponding opening brackets: {')': '(', '}': '{', ']': '['}.",
    "Iterate through the string; push opening brackets onto the stack.",
    "For closing brackets, check if the stack is non-empty and the top of the stack matches the expected opening bracket. If so, pop it; otherwise, return False. Finally, return True if the stack is empty.",
]


class Solution:
    def isValid(self, s: str) -> bool:
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {"input": ("()",), "expected": True, "name": "example1"},
    {"input": ("()[]{}",), "expected": True, "name": "example2"},
    {"input": ("(]",), "expected": False, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.isValid(*case["input"]) == case["expected"]
