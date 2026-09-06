"""Valid Palindrome.

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters
and removing all non-alphanumeric characters, it reads the same forward and backward.
Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Examples:
    1. Input: s = "A man, a plan, a canal: Panama"
       Output: true
       Explanation: "amanaplanacanalpanama" is a palindrome.
    2. Input: s = "race a car"
       Output: false
       Explanation: "raceacar" is not a palindrome.

Constraints:
    - 1 <= s.length <= 2 * 10^5
    - s consists only of printable ASCII characters.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

HINTS = [
    "Pointers can start at both ends of the string and move towards the center.",
    "Ignore non-alphanumeric characters. You can use .isalnum() in Python.",
    "Compare the characters at the two pointers while ignoring case using .lower().",
    "If they don't match, return False. Otherwise, move the pointers closer. If they meet, return True.",
]


class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


TEST_CASES = [
    {"input": ("A man, a plan, a canal: Panama",), "expected": True, "name": "example1"},
    {"input": ("race a car",), "expected": False, "name": "example2"},
    {"input": (" ",), "expected": True, "name": "example3"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.isPalindrome(*case["input"]) == case["expected"]
