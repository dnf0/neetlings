"""Group Anagrams.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates frequency counting and hash table categorization using immutable keys.

Given an array of strings strs, group the anagrams together. You can return
the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters exactly once.

Examples:
    1. Input: strs = ["eat","tea","tan","ate","nat","bat"]
       Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
    2. Input: strs = [""]
       Output: [[""]]
    3. Input: strs = ["a"]
       Output: [["a"]]

Constraints:
    - 1 <= strs.length <= 10^4
    - 0 <= strs[i].length <= 100
    - strs[i] consists of lowercase English letters.

Target:
    - Time Complexity: O(m * n) where m is len(strs) and n is max string length
    - Space Complexity: O(m * n)
"""

from collections import defaultdict

HINTS = [
    "Two strings are anagrams if and only if their character counts are identical. How can we map each string to a common signature?",
    "Instead of sorting each string (which takes O(n log n)), we can use a frequency count of 26 lowercase English letters as a canonical key in a hash map.",
    "Python lists cannot be dictionary keys because they are mutable, but a tuple of counts is immutable and hashable. Handle empty strings and single characters gracefully.",
    "Initialize a defaultdict(list). For each string s, build a 26-element count list, convert it to tuple(count), and append s to the list at that key. Return list(ans.values()).",
]


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        """Group anagrams together from the input list of strings.

        Uses a 26-element character frequency tuple as the canonical hash key.
        Achieves optimal O(m * n) time and O(m * n) auxiliary space without
        per-word sorting (which would require O(m * n log n)).

        Args:
            strs: List of strings consisting of lowercase English letters.

        Returns:
            List of grouped anagrams (each group is a list of strings).
        """
        # Guard clause: Empty input produces an empty grouping list.
        # Although problem constraints specify len(strs) >= 1, this guards edge callers.
        if not strs:
            return []

        # Map each canonical 26-element character count tuple to its list of anagram words.
        # Using defaultdict eliminates explicit key-existence initialization checks.
        groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
        offset = ord("a")

        # Process each word by computing its 26-letter frequency distribution.
        # Converting the mutable count list into an immutable tuple allows hash table indexing.
        for s in strs:
            count = [0] * 26
            for char in s:
                count[ord(char) - offset] += 1
            groups[tuple(count)].append(s)

        return list(groups.values())


TEST_CASES = [
    {
        "input": (["eat", "tea", "tan", "ate", "nat", "bat"],),
        "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        "name": "standard_grouping",
    },
    {
        "input": ([""],),
        "expected": [[""]],
        "name": "single_empty_string",
    },
    {
        "input": (["a"],),
        "expected": [["a"]],
        "name": "single_character",
    },
    {
        "input": (["", ""],),
        "expected": [["", ""]],
        "name": "multiple_empty_strings",
    },
    {
        "input": (["bdddddddddd", "bbbbbbbbbbc"],),
        "expected": [["bdddddddddd"], ["bbbbbbbbbbc"]],
        "name": "different_character_counts",
    },
    {
        "input": (["cab", "tin", "pew", "duh", "may", "ill", "buy", "bar", "max", "doc"],),
        "expected": [
            ["cab"],
            ["tin"],
            ["pew"],
            ["duh"],
            ["may"],
            ["ill"],
            ["buy"],
            ["bar"],
            ["max"],
            ["doc"],
        ],
        "name": "all_distinct_anagram_groups",
    },
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sorted([sorted(g) for g in sol.groupAnagrams(*case["input"])]) == sorted(
            [sorted(g) for g in case["expected"]]
        )
