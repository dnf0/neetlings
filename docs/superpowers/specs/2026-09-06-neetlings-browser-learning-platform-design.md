# Neetlings: Full Browser WebAssembly Learning Platform for NeetCode 150

**Date:** 2026-09-06  
**Status:** Approved Design Spec  
**Target Platform:** 100% Client-Side WebAssembly (Pyodide) & Static GitHub Pages  
**Tech Stack:** Python 3.12, Pyodide v0.26+, Monaco Editor, uv, ruff, pyright, pytest  

---

## 1. Executive Summary

`neetlings` is an interactive, zero-install, zero-cost data structures and algorithms learning platform implementing the complete **NeetCode 150** curriculum. Built in alignment with the architecture established in `kubelings` and `raylings`, `neetlings` operates 100% client-side in the browser using **Pyodide WebAssembly (Python 3.12)** and **Monaco Editor** (VS Code in the browser).

### Key Differentiators Over Standard NeetCode
1. **Zero Backend Infrastructure & Zero Cloud Cost**: Code evaluates inside an isolated client-side Web Worker powered by Pyodide v0.26. No servers, no accounts, no queues, completely free to host on GitHub Pages and fully functional offline.
2. **Rich Diagnostic Visualizers**: In-memory test runners generate ASCII diagrams for binary trees, linked lists, and 2D matrices on test failures, showing inputs, expected outcomes, and user outputs side-by-side.
3. **AST Complexity & Recursion Guardrails**: Static AST analysis and runtime step counters flag suboptimal solutions (e.g. detecting $O(n^2)$ nested loops where $O(n)$ hash mapping is required, or unauthorized calls to `list.sort()` when bucket sort is being tested).
4. **Graduated Hint Ladder & Monaco Diff**: A 4-stage progressive hint reveal (Intuition → Invariant & Pointers → Pseudocode → Side-by-side Monaco Diff against optimal reference solutions).
5. **Pure Python Authoring & Verification**: All 150 exercises and solutions are standard Python 3.12 modules validated locally with `pytest`, `ruff`, and `pyright` before bundling into static JSON.

---

## 2. System Architecture

```text
+--------------------------------------------------------------------------------------------------------+
|                                    BROWSER UI (index.html SPA)                                         |
|                                                                                                        |
|  +---------------------------+  +--------------------------------+  +-------------------------------+  |
|  |  Pane 1: Problem & Hints  |  |    Pane 2: Monaco Editor       |  |  Pane 3: Diagnostics & Diff   |  |
|  |  - Markdown problem spec  |  |    - VS Code keybindings       |  |  - ANSI test case results     |  |
|  |  - Constraints & examples |  |    - Python syntax & folding   |  |  - ASCII tree/list diagrams   |  |
|  |  - 4-Tier hint ladder     |  |    - Ctrl+Enter hotkey         |  |  - Step counter & AST alerts  |  |
|  |  - Category selector      |  |    - Draft auto-save (Local)   |  |  - Side-by-side Monaco diff   |  |
|  +---------------------------+  +--------------------------------+  +-------------------------------+  |
+-------------------------------------------------+------------------------------------------------------+
                                                  | postMessage({ type: "RUN", code, exerciseId })
                                                  v
+--------------------------------------------------------------------------------------------------------+
|                                 BACKGROUND WEB WORKER (Pyodide v0.26)                                  |
|                                                                                                        |
|  +--------------------------------------------------------------------------------------------------+  |
|  | Pyodide WebAssembly Runtime (Python 3.12)                                                        |  |
|  |                                                                                                  |  |
|  |  Virtual Filesystem (/lib/neetlings/):                                                           |  |
|  |  ├── models.py        (TreeNode, ListNode, GraphNode, Interval)                                  |  |
|  |  ├── visualizers.py   (ASCII tree printer, list arrow renderer, matrix formatter)               |  |
|  |  ├── complexity.py    (AST rule checks, step counter, recursion limits)                          |  |
|  |  └── test_runner.py   (Captures stdout/stderr, runs TEST_CASES, formats timing & diffs)          |  |
|  |                                                                                                  |  |
|  |  Execution Sandbox:                                                                              |  |
|  |  - Evaluates user code against test cases in under 20ms                                           |  |
|  |  - Enforces 2000ms max timeout to protect against infinite loops                                 |  |
|  +--------------------------------------------------------------------------------------------------+  |
+--------------------------------------------------------------------------------------------------------+
```

---

## 3. Repository Layout

```text
neetlings/
├── exercises/                           # 18 category directories containing 150 starter problems
│   ├── 01_arrays_and_hashing/
│   │   ├── 01_contains_duplicate.py
│   │   ├── 02_valid_anagram.py
│   │   ├── 03_two_sum.py
│   │   ├── 04_group_anagrams.py
│   │   ├── 05_top_k_frequent_elements.py
│   │   ├── 06_product_of_array_except_self.py
│   │   ├── 07_valid_sudoku.py
│   │   ├── 08_encode_and_decode_strings.py
│   │   └── 09_longest_consecutive_sequence.py
│   ├── 02_two_pointers/
│   ├── 03_sliding_window/
│   ├── 04_stack/
│   ├── 05_binary_search/
│   ├── 06_linked_list/
│   ├── 07_trees/
│   ├── 08_tries/
│   ├── 09_heap_priority_queue/
│   ├── 10_backtracking/
│   ├── 11_graphs/
│   ├── 12_advanced_graphs/
│   ├── 13_1d_dynamic_programming/
│   ├── 14_2d_dynamic_programming/
│   ├── 15_greedy/
│   ├── 16_intervals/
│   ├── 17_math_and_geometry/
│   └── 18_bit_manipulation/
├── solutions/                           # Optimal reference solutions matching exercise files
│   ├── 01_arrays_and_hashing/
│   └── ...
├── src/neetlings/                       # In-memory virtual library mounted into Pyodide
│   ├── __init__.py
│   ├── models.py                        # ListNode, TreeNode, GraphNode, Interval helpers
│   ├── visualizers.py                   # ASCII visualizers for trees, lists, grids
│   ├── complexity.py                    # AST syntax inspector and runtime step counter
│   ├── test_runner.py                   # In-memory execution test harness
│   ├── manifest.py                      # Curriculum manifest, category and exercise metadata
│   └── bundler.py                       # Bundle generator compiling assets into JSON
├── scripts/
│   └── build_playground_bundle.py       # CLI script to build playground-bundle.json
├── docs/
│   ├── playground/
│   │   └── index.html                   # Responsive 3-pane SPA entry point
│   └── assets/playground/
│       ├── playground.css               # Styling and theme definitions
│       ├── playground.js                # UI controller, Monaco loader, local storage engine
│       ├── playground-worker.js         # Dedicated Web Worker Pyodide runtime
│       └── playground-bundle.json        # Compiled catalog containing all 150 problems
├── tests/
│   ├── test_reference_solutions.py      # Automated pytest run against all 150 solutions
│   ├── test_visualizers.py              # Tests for ASCII tree and list generators
│   └── test_bundler.py                  # Tests for asset generation
├── pyproject.toml                       # Python package configuration (uv, ruff, pyright, pytest)
└── README.md
```

---

## 4. Curriculum Structure (The 18 Categories)

The curriculum covers all 150 problems from the NeetCode pattern hierarchy:

1. **Arrays & Hashing (9 problems)**: Contains Duplicate, Valid Anagram, Two Sum, Group Anagrams, Top K Frequent Elements, Product of Array Except Self, Valid Sudoku, Encode and Decode Strings, Longest Consecutive Sequence.
2. **Two Pointers (5 problems)**: Valid Palindrome, Two Sum II, 3Sum, Container With Most Water, Trapping Rain Water.
3. **Sliding Window (6 problems)**: Best Time to Buy and Sell Stock, Longest Substring Without Repeating Characters, Longest Repeating Character Replacement, Permutation in String, Minimum Window Substring, Sliding Window Maximum.
4. **Stack (7 problems)**: Valid Parentheses, Min Stack, Evaluate Reverse Polish Notation, Generate Parentheses, Daily Temperatures, Car Fleet, Largest Rectangle in Histogram.
5. **Binary Search (7 problems)**: Binary Search, Search a 2D Matrix, Koko Eating Bananas, Find Minimum in Rotated Sorted Array, Search in Rotated Sorted Array, Time Based Key-Value Store, Median of Two Sorted Arrays.
6. **Linked List (11 problems)**: Reverse Linked List, Merge Two Sorted Lists, Reorder List, Remove Nth Node From End of List, Copy List with Random Pointer, Add Two Numbers, Linked List Cycle, Find The Duplicate Number, LRU Cache, Merge K Sorted Lists, Reverse Nodes in K-Group.
7. **Trees (15 problems)**: Invert Binary Tree, Maximum Depth of Binary Tree, Diameter of Binary Tree, Balanced Binary Tree, Same Tree, Subtree of Another Tree, Lowest Common Ancestor of a BST, Binary Tree Level Order Traversal, Binary Tree Right Side View, Count Good Nodes in Binary Tree, Validate Binary Search Tree, Kth Smallest Element in a BST, Construct Binary Tree from Preorder and Inorder Traversal, Binary Tree Maximum Path Sum, Serialize and Deserialize Binary Tree.
8. **Tries (3 problems)**: Implement Trie Prefix Tree, Design Add and Search Words Data Structure, Word Search II.
9. **Heap / Priority Queue (7 problems)**: Kth Largest Element in a Stream, Last Stone Weight, K Closest Points to Origin, Kth Largest Element in an Array, Task Scheduler, Design Twitter, Find Median from Data Stream.
10. **Backtracking (9 problems)**: Subsets, Combination Sum, Permutations, Subsets II, Combination Sum II, Word Search, Palindrome Partitioning, Letter Combinations of a Phone Number, N-Queens.
11. **Graphs (13 problems)**: Number of Islands, Max Area of Island, Clone Graph, Walls and Gates, Rotting Oranges, Pacific Atlantic Water Flow, Surrounded Regions, Course Schedule, Course Schedule II, Graph Valid Tree, Number of Connected Components in an Undirected Graph, Redundant Connection, Word Ladder.
12. **Advanced Graphs (6 problems)**: Reconstruct Itinerary, Min Cost to Connect All Points, Network Delay Time, Swim in Rising Water, Alien Dictionary, Cheapest Flights Within K Stops.
13. **1-D Dynamic Programming (12 problems)**: Climbing Stairs, Min Cost Climbing Stairs, House Robber, House Robber II, Longest Palindromic Substring, Palindromic Substrings, Decode Ways, Coin Change, Maximum Product Subarray, Word Break, Longest Increasing Subsequence, Partition Equal Subset Sum.
14. **2-D Dynamic Programming (11 problems)**: Unique Paths, Longest Common Subsequence, Best Time to Buy and Sell Stock with Cooldown, Coin Change II, Target Sum, Interleaving String, Longest Increasing Path in a Matrix, Distinct Subsequences, Edit Distance, Burst Balloons, Regular Expression Matching.
15. **Greedy (8 problems)**: Maximum Subarray, Jump Game, Jump Game II, Gas Station, Hand of Straights, Merge Triplets to Form Target Triplet, Partition Labels, Valid Parenthesis String.
16. **Intervals (6 problems)**: Insert Interval, Merge Intervals, Non-overlapping Intervals, Meeting Rooms, Meeting Rooms II, Minimum Interval to Include Each Query.
17. **Math & Geometry (8 problems)**: Rotate Image, Spiral Matrix, Set Matrix Zeroes, Happy Number, Plus One, Pow(x, n), Multiply Strings, Detect Squares.
18. **Bit Manipulation (7 problems)**: Single Number, Number of 1 Bits, Counting Bits, Reverse Bits, Missing Number, Sum of Two Integers, Reverse Integer.

---

## 5. Exercise File Specification

Every exercise file is a self-contained, valid Python module formatted as follows:

```python
"""
# 01. Contains Duplicate
Difficulty: Easy
Category: Arrays & Hashing
Time Target: O(n) | Space Target: O(n)

## Problem Statement
Given an integer array `nums`, return `true` if any value appears at least twice in the array,
and return `false` if every element is distinct.

## Examples
Input: nums = [1, 2, 3, 1] -> Output: True
Input: nums = [1, 2, 3, 4] -> Output: False
"""

from __future__ import annotations

# ==============================================================================
# Progressive Hints
# ==============================================================================
HINTS = [
    "A brute-force comparison of every pair takes O(n^2) time. Can you do it in one pass with extra memory?",
    "What data structure provides O(1) average-time lookups to check if an element was previously encountered?",
    "Iterate through nums; if num in seen_set return True, else seen_set.add(num). If loop finishes, return False.",
]


class Solution:
    def contains_duplicate(self, nums: list[int]) -> bool:
        # TODO: Implement your solution below
        raise NotImplementedError("Implement contains_duplicate")


# ==============================================================================
# Self-Contained Test Suite
# ==============================================================================
TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "basic_duplicate"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "all_unique"},
    {"input": ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), "expected": True, "name": "multiple_duplicates"},
    {"input": ([42],), "expected": False, "name": "single_element"},
    {"input": ([],), "expected": False, "name": "empty_list"},
]


def test_solution() -> None:
    sol = Solution()
    for case in TEST_CASES:
        actual = sol.contains_duplicate(*case["input"])
        assert actual == case["expected"], f"Failed {case['name']}: expected {case['expected']}, got {actual}"
```

---

## 6. Virtual Runtime Engine (`src/neetlings/`)

Mounted directly into the Pyodide Web Worker virtual filesystem at `/lib/neetlings/`:

### 6.1 `models.py`
- `ListNode(val, next)`:
  - `.from_list(vals: list[int]) -> ListNode | None`
  - `.to_list() -> list[int]`
  - `.to_ascii() -> str` (e.g. `1 ➔ 2 ➔ 3 ➔ 4 ➔ None`)
- `TreeNode(val, left, right)`:
  - `.from_level_order(vals: list[int | None]) -> TreeNode | None`
  - `.to_level_order() -> list[int | None]`
  - `.to_ascii() -> str` (renders a multi-line branch diagram)
- `GraphNode(val, neighbors)`

### 6.2 `visualizers.py`
- `format_tree_diff(expected: TreeNode, actual: TreeNode) -> str`: Renders side-by-side ASCII comparison trees with mismatched nodes highlighted.
- `format_list_diff(expected: ListNode, actual: ListNode) -> str`: Formats linked list differences.
- `format_grid(grid: list[list[Any]], row_labels: bool = True) -> str`: Renders 2D boards and DP tables cleanly.

### 6.3 `complexity.py`
- `check_banned_syntax(code: str, banned_nodes: list[str]) -> list[str]`: Uses Python `ast.parse` to identify forbidden constructs (e.g. `ast.Call` to `sort` when testing sorting algorithms).
- `StepCounter`: Context manager instrumenting iteration loops and recursive calls to detect $O(n^2)$ behavior on large test cases.

### 6.4 `test_runner.py`
- Executes user code against `TEST_CASES`.
- Captures `sys.stdout` and `sys.stderr` using `io.StringIO()`.
- Records wall-clock execution time with `time.perf_counter()`.
- Formats structured JSON result payload sent back to the UI via `postMessage`:
  ```json
  {
    "status": "PASSED" | "FAILED" | "ERROR",
    "passedCount": 5,
    "totalCount": 5,
    "durationMs": 0.12,
    "stdout": "...",
    "cases": [
      { "name": "basic_duplicate", "status": "PASSED", "durationMs": 0.04 }
    ],
    "diagnosticDiff": null
  }
  ```

---

## 7. Frontend UI / UX Specification

### 7.1 Single Page Application Layout
- **Header**:
  - Logo with WebAssembly badge.
  - Category and Problem selector dropdown with status indicators (🟢 Solved, ⚪ Unsolved).
  - Search input filtering by name, tag, or difficulty.
  - Global solved counter: `[ 0 / 150 Solved ]`.
  - Actions: `Reset`, `Export JSON`, `Import JSON`, Light/Dark mode toggle.
- **Left Pane (Problem & Hints)**:
  - Markdown rendered description with syntax highlighted examples.
  - Progressive Hint Accordion:
    - `💡 Hint 1: Intuition & Pattern`
    - `💡 Hint 2: Invariant & State Rules`
    - `💡 Hint 3: Step-by-Step Pseudocode`
    - `🔍 Compare Solution (Monaco Diff)`
- **Center Pane (Monaco Editor)**:
  - Monaco Editor configured for Python.
  - Keybinding: `Ctrl+Enter` / `Cmd+Enter` dispatches code to worker.
  - Run button with loading spinner during worker execution.
- **Right Pane (Diagnostics & Results)**:
  - Tab 1: Test Results (ANSI green/red test suite results and execution timing).
  - Tab 2: Visual Diff (ASCII tree/list/matrix comparisons on failures).
  - Tab 3: Stdout Console (Captures `print()` logs).
  - Tab 4: Reference Diff (Side-by-side Monaco diff viewer against canonical solution).

### 7.2 Persistence Engine (`NeetlingsStorage`)
- In-progress code automatically saved to `localStorage` per problem key (debounced at 300ms).
- Records `solved: true`, `completed_at: timestamp`, and `revealed_hints: int`.
- Full backup export and restore via JSON.

---

## 8. Verification & Testing Strategy

1. **Reference Solution Validation**:
   - `pytest tests/test_reference_solutions.py` imports and runs `test_solution()` for every one of the 150 solutions.
   - All 150 solutions must pass 100% of test cases.
2. **AST & Visualizer Unit Tests**:
   - Tests validating that `format_tree_diff` and `format_list_diff` correctly render edge cases (single nodes, unbalanced trees, empty lists).
   - Tests validating that `check_banned_syntax` accurately catches forbidden AST calls.
3. **Bundle Integrity Verification**:
   - `pytest tests/test_bundler.py` verifies that `playground-bundle.json` builds cleanly, contains all 18 categories, 150 exercises, valid starter codes, solutions, and hints.
4. **Static Code Quality**:
   - `uv run ruff check src exercises solutions tests`
   - `uv run ruff format --check src exercises solutions tests`
   - `uv run pyright src tests`
