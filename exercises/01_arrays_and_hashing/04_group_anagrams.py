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

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        """Group anagrams together from the input list of strings.

        Args:
            strs: List of strings consisting of lowercase English letters.

        Returns:
            List of grouped anagrams (each group is a list of strings).

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

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
