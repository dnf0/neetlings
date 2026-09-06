"""Curriculum manifest definitions for NeetCode 150 categories."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ChapterInfo:
    """Represents metadata for a single learning chapter/category.

    Attributes:
        number: The chronological chapter number (1-indexed).
        id: The programmatic identifier of the category.
        title: The display title of the category.
        description: A brief summary of topic areas covered.
        exercise_ids: The ordered list of exercise identifiers belonging to this category.
    """

    number: int
    id: str
    title: str
    description: str
    exercise_ids: list[str] = field(default_factory=list)


# All 18 NeetCode 150 curriculum categories mapped chronologically.
# Each entry specifies its folder index/ID, display title, and high-level description.
CATEGORIES: list[ChapterInfo] = [
    ChapterInfo(
        1,
        "arrays_and_hashing",
        "Arrays & Hashing",
        "Hash maps, sets, frequency arrays",
        exercise_ids=[
            "01_contains_duplicate",
            "02_valid_anagram",
            "03_two_sum",
            "04_group_anagrams",
            "05_top_k_frequent_elements",
            "06_product_of_array_except_self",
            "07_valid_sudoku",
            "08_encode_and_decode_strings",
            "09_longest_consecutive_sequence",
        ],
    ),
    ChapterInfo(
        2,
        "two_pointers",
        "Two Pointers",
        "Converging indices, sorted search",
        exercise_ids=[
            "01_valid_palindrome",
            "02_two_sum_ii_input_array_is_sorted",
            "03_3sum",
            "04_container_with_most_water",
            "05_trapping_rain_water",
        ],
    ),
    ChapterInfo(
        3,
        "sliding_window",
        "Sliding Window",
        "Subarrays, dynamic & fixed window",
        exercise_ids=["01_best_time_to_buy_and_sell_stock"],
    ),
    ChapterInfo(
        4,
        "stack",
        "Stack",
        "LIFO, monotonic stacks, parentheses",
        exercise_ids=["01_valid_parentheses"],
    ),
    ChapterInfo(
        5,
        "binary_search",
        "Binary Search",
        "Search space division, rotated arrays",
        exercise_ids=["01_binary_search"],
    ),
    ChapterInfo(
        6,
        "linked_list",
        "Linked List",
        "Fast & slow pointers, reversals",
        exercise_ids=["01_reverse_linked_list"],
    ),
    ChapterInfo(
        7,
        "trees",
        "Trees",
        "DFS, BFS, BST invariants",
        exercise_ids=["01_invert_binary_tree"],
    ),
    ChapterInfo(
        8,
        "tries",
        "Tries",
        "Prefix trees, word search",
        exercise_ids=["01_implement_trie_prefix_tree"],
    ),
    ChapterInfo(
        9,
        "heap_priority_queue",
        "Heap / Priority Queue",
        "Min/Max heaps, top-k",
        exercise_ids=["01_kth_largest_element_in_a_stream"],
    ),
    ChapterInfo(
        10,
        "backtracking",
        "Backtracking",
        "State exploration, pruning",
        exercise_ids=["01_subsets"],
    ),
    ChapterInfo(
        11,
        "graphs",
        "Graphs",
        "BFS, DFS, cycle detection, topological sort",
        exercise_ids=["01_number_of_islands"],
    ),
    ChapterInfo(
        12,
        "advanced_graphs",
        "Advanced Graphs",
        "Dijkstra, Prim, Kruskal",
        exercise_ids=["01_network_delay_time"],
    ),
    ChapterInfo(
        13,
        "1d_dynamic_programming",
        "1-D Dynamic Programming",
        "Subproblems, tabulation",
        exercise_ids=["01_climbing_stairs"],
    ),
    ChapterInfo(
        14,
        "2d_dynamic_programming",
        "2-D Dynamic Programming",
        "Grids, knapsack, LCS",
        exercise_ids=["01_unique_paths"],
    ),
    ChapterInfo(
        15,
        "greedy",
        "Greedy",
        "Local optimal choices",
        exercise_ids=["01_maximum_subarray"],
    ),
    ChapterInfo(
        16,
        "intervals",
        "Intervals",
        "Merging, scheduling, non-overlapping",
        exercise_ids=["01_insert_interval"],
    ),
    ChapterInfo(
        17,
        "math_and_geometry",
        "Math & Geometry",
        "Matrix rotations, spiral traversal",
        exercise_ids=["01_rotate_image"],
    ),
    ChapterInfo(
        18,
        "bit_manipulation",
        "Bit Manipulation",
        "Bitwise logic, XOR properties",
        exercise_ids=["01_single_number"],
    ),
]

# Alias for compatibility with chapter-oriented interfaces.
CHAPTERS: list[ChapterInfo] = CATEGORIES
