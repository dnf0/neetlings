"""Valid Anagram.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates frequency counting and hash-based frequency comparison.

Given two strings s and t, return true if t is an anagram of s,
and return false otherwise.

Examples:
    1. Input: s = "anagram", t = "nagaram"
       Output: true
    2. Input: s = "rat", t = "car"
       Output: false

Constraints:
    - 1 <= s.length, t.length <= 5 * 10^4
    - s and t consist of lowercase English letters.

Target:
    - Time Complexity: O(n)
    - Space Complexity: O(1)
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """Determine if string t is an anagram of string s.

        Args:
            s: Source string of lowercase English letters.
            t: Candidate string to verify as an anagram.

        Returns:
            True if t is an anagram of s, False otherwise.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {"input": ("anagram", "nagaram"), "expected": True, "name": "standard_anagram"},
    {"input": ("rat", "car"), "expected": False, "name": "different_characters"},
    {"input": ("a", "a"), "expected": True, "name": "single_char_match"},
    {"input": ("a", "b"), "expected": False, "name": "single_char_mismatch"},
    {"input": ("ab", "a"), "expected": False, "name": "different_lengths"},
    {"input": ("aaabbb", "ababab"), "expected": True, "name": "repeated_chars_anagram"},
    {"input": ("aaabbb", "aabbbb"), "expected": False, "name": "same_chars_different_counts"},
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.isAnagram(*case["input"]) == case["expected"]
