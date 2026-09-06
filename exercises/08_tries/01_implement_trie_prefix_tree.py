"""Implement Trie (Prefix Tree).

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and
retrieve keys in a dataset of strings. There are various applications of this data structure,
such as autocomplete and spellchecker.

Implement the Trie class wrapped within Solution:
    - solve(self, operations: list[str], arguments: list[list[Any]]) -> list[Any]
      Executes a series of trie operations and returns the results list.

Examples:
    1. Input:
       operations = ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
       arguments = [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
       Output:
       [None, None, True, False, True, None, True]

Constraints:
    - 1 <= word.length, prefix.length <= 2000
    - word and prefix consist only of lowercase English letters.
    - At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.

Target:
    - Time Complexity:
        - Insert: O(m) where m is key length
        - Search: O(m)
        - StartsWith: O(m)
    - Space Complexity: O(total number of nodes * 26)
"""

from typing import Any


class Solution:
    def solve(self, operations: list[str], arguments: list[list[Any]]) -> list[Any]:
        # TODO: Implement your solution here
        raise NotImplementedError

TEST_CASES = [
    {
        "input": (
            ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
            [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
        ),
        "expected": [None, None, True, False, True, None, True],
        "name": "example1",
    }
]

def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        assert sol.solve(*case["input"]) == case["expected"]
