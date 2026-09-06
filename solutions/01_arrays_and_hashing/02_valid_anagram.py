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

HINTS = [
    "An anagram must contain the exact same characters with identical frequencies. If lengths differ, can they be anagrams?",
    "Use character frequency counting. Since characters are lowercase English letters, a fixed 26-element array or dictionary tracks counts.",
    "Check if len(s) != len(t) as a guard clause. Increment frequencies for characters in s and decrement for characters in t.",
    "Initialize a 26-element integer list. If lengths differ, return False. In one pass, update counts for s and t. Return True only if all counts are zero.",
]


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """Determine if string t is an anagram of string s.

        Uses a fixed 26-element integer table to count character frequencies
        in O(n) time and O(1) auxiliary space without sorting or collections.Counter.

        Args:
            s: Source string of lowercase English letters.
            t: Candidate string to verify as an anagram.

        Returns:
            True if t is an anagram of s, False otherwise.
        """
        # Guard clause: Anagrams must have identical character lengths.
        # Returning early avoids unnecessary allocations and passes.
        if len(s) != len(t):
            return False

        # Fixed 26-slot array representing ASCII offsets from 'a'.
        # Because alphabet size is constant (26 letters), space complexity is strictly O(1).
        counts = [0] * 26
        offset = ord("a")

        # Simultaneously increment frequencies for s and decrement for t.
        # This achieves a single-pass dual-string scan.
        for char_s, char_t in zip(s, t):
            counts[ord(char_s) - offset] += 1
            counts[ord(char_t) - offset] -= 1

        # Check if every character offset returned to zero balance.
        # Non-zero balance proves a surplus or deficit in letter frequencies.
        for count in counts:
            if count != 0:
                return False

        return True


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
