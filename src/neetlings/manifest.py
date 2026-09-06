"""Curriculum manifest definitions for NeetCode 150 categories."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChapterInfo:
    """Represents metadata for a single learning chapter/category.

    Attributes:
        number: The chronological chapter number (1-indexed).
        id: The programmatic identifier of the category.
        title: The display title of the category.
        description: A brief summary of topic areas covered.
    """
    number: int
    id: str
    title: str
    description: str


# All 18 NeetCode 150 curriculum categories mapped chronologically.
# Each entry specifies its folder index/ID, display title, and high-level description.
CATEGORIES: list[ChapterInfo] = [
    ChapterInfo(1, "arrays_and_hashing", "Arrays & Hashing", "Hash maps, sets, frequency arrays"),
    ChapterInfo(2, "two_pointers", "Two Pointers", "Converging indices, sorted search"),
    ChapterInfo(3, "sliding_window", "Sliding Window", "Subarrays, dynamic & fixed window"),
    ChapterInfo(4, "stack", "Stack", "LIFO, monotonic stacks, parentheses"),
    ChapterInfo(5, "binary_search", "Binary Search", "Search space division, rotated arrays"),
    ChapterInfo(6, "linked_list", "Linked List", "Fast & slow pointers, reversals"),
    ChapterInfo(7, "trees", "Trees", "DFS, BFS, BST invariants"),
    ChapterInfo(8, "tries", "Tries", "Prefix trees, word search"),
    ChapterInfo(9, "heap_priority_queue", "Heap / Priority Queue", "Min/Max heaps, top-k"),
    ChapterInfo(10, "backtracking", "Backtracking", "State exploration, pruning"),
    ChapterInfo(11, "graphs", "Graphs", "BFS, DFS, cycle detection, topological sort"),
    ChapterInfo(12, "advanced_graphs", "Advanced Graphs", "Dijkstra, Prim, Kruskal"),
    ChapterInfo(13, "1d_dynamic_programming", "1-D Dynamic Programming", "Subproblems, tabulation"),
    ChapterInfo(14, "2d_dynamic_programming", "2-D Dynamic Programming", "Grids, knapsack, LCS"),
    ChapterInfo(15, "greedy", "Greedy", "Local optimal choices"),
    ChapterInfo(16, "intervals", "Intervals", "Merging, scheduling, non-overlapping"),
    ChapterInfo(17, "math_and_geometry", "Math & Geometry", "Matrix rotations, spiral traversal"),
    ChapterInfo(18, "bit_manipulation", "Bit Manipulation", "Bitwise logic, XOR properties"),
]
