"""Encode and Decode Strings.

Curriculum exercise module within the Arrays & Hashing chapter.
Evaluates delimiter escaping and length-prefixed serialization protocols.

Design an algorithm to encode a list of strings to a single string.
The encoded string is then decoded back to the original list of strings.

Please implement `encode` and `decode`.

Examples:
    1. Input: dummy_input = ["lint","code","love","you"]
       Output: ["lint","code","love","you"]
       Explanation:
       One possible encode method is: "4#lint4#code4#love3#you"
    2. Input: dummy_input = ["we", "say", ":", "yes"]
       Output: ["we", "say", ":", "yes"]
    3. Input: dummy_input = [""]
       Output: [""]
    4. Input: dummy_input = []
       Output: []

Constraints:
    - 0 <= strs.length <= 200
    - 0 <= strs[i].length <= 200
    - strs[i] contains any possible characters out of 256 valid ASCII characters.

Target:
    - Time Complexity: O(n) for both encode and decode, where n is total characters
    - Space Complexity: O(n) to store encoded string and decoded list
"""

HINTS = [
    "Standard single-character delimiters (e.g. commas or colons) fail when strings contain that delimiter. How can we record boundaries unambiguously without relying on escaping?",
    "Length-prefixed encoding (chunking). Prefix each string with its length followed by a separator (e.g., '<length>#<string>').",
    "During decoding, read characters until the '#' separator to parse the length integer L. Once L is parsed, take exactly the next L characters as the string payload, then advance past it.",
    "For `encode`, join chunks formed by `f'{len(s)}#{s}'`. For `decode`, maintain pointer `i = 0`. In a while loop, find delimiter `j = s.find('#', i)`, parse length `length = int(s[i:j])`, slice `s[j + 1 : j + 1 + length]`, and update `i = j + 1 + length`.",
]


class Solution:
    def encode(self, strs: list[str]) -> str:
        """Encode a list of strings into a single string.

        Args:
            strs: List of strings to encode.

        Returns:
            A single encoded string.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError

    def decode(self, s: str) -> list[str]:
        """Decode a single string back into a list of strings.

        Args:
            s: Encoded string produced by `encode`.

        Returns:
            Reconstructed list of original strings.

        Raises:
            NotImplementedError: Awaiting student implementation.
        """
        # TODO: Implement your solution here
        raise NotImplementedError


TEST_CASES = [
    {"input": (["lint", "code", "love", "you"],), "expected": ["lint", "code", "love", "you"], "name": "standard_strings"},
    {"input": (["we", "say", ":", "yes"],), "expected": ["we", "say", ":", "yes"], "name": "strings_with_colons"},
    {"input": ([""],), "expected": [""], "name": "single_empty_string"},
    {"input": ([],), "expected": [], "name": "empty_list"},
    {"input": (["#", "##", "4#test#"],), "expected": ["#", "##", "4#test#"], "name": "delimiters_inside_strings"},
    {"input": (["", "", ""],), "expected": ["", "", ""], "name": "multiple_empty_strings"},
    {"input": (["!@#$%^&*()_+{}[]:;\"'<>?,./~`"],), "expected": ["!@#$%^&*()_+{}[]:;\"'<>?,./~`"], "name": "special_characters"},
    {"input": (["12345678901", "a" * 50, "hello world!"],), "expected": ["12345678901", "a" * 50, "hello world!"], "name": "numbers_and_long_strings"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        encoded = sol.encode(*case["input"])
        decoded = sol.decode(encoded)
        assert decoded == case["expected"]
