# Curriculum Expansion: Category 1 — Arrays & Hashing (9 Problems) Design Specification

## Overview & Objectives
Expand the **Neetlings** in-browser learning curriculum from the initial single showcase problem in **Arrays & Hashing** to the complete **9-problem NeetCode 150 category**. Each problem includes starter exercises, optimal reference solutions, 4-tier progressive hint ladders, strict AST complexity guardrails, and automated test suites.

---

## 1. Problem Catalog & Specifications

| # | ID | Problem Name | Difficulty | Time / Space Complexity | Key AST Guardrail |
|---|---|---|---|---|---|
| 1 | `01_contains_duplicate` | Contains Duplicate | Easy | $O(n)$ / $O(n)$ | Banned: `sort`, `sorted` |
| 2 | `02_valid_anagram` | Valid Anagram | Easy | $O(n)$ / $O(1)$ | Banned: `sort`, `sorted`, `Counter` |
| 3 | `03_two_sum` | Two Sum | Easy | $O(n)$ / $O(n)$ | Step limit: $200,000$ (prevents $O(n^2)$) |
| 4 | `04_group_anagrams` | Group Anagrams | Medium | $O(m \cdot n)$ / $O(m \cdot n)$ | Frequency tuple / normalized multiset testing |
| 5 | `05_top_k_frequent_elements` | Top K Frequent Elements | Medium | $O(n)$ / $O(n)$ | Banned: `sort`, `sorted` ($O(n)$ bucket sort) |
| 6 | `06_product_of_array_except_self` | Product of Array Except Self | Medium | $O(n)$ / $O(1)$ extra | Banned: division operators `/`, `//`, `divmod` |
| 7 | `07_valid_sudoku` | Valid Sudoku | Medium | $O(1)$ / $O(1)$ | 9x9 grid hashing, `format_grid` on mismatch |
| 8 | `08_encode_and_decode_strings` | Encode and Decode Strings | Medium | $O(n)$ / $O(n)$ | Stateless length-prefixed chunking (`len#chunk`) |
| 9 | `09_longest_consecutive_sequence`| Longest Consecutive Sequence | Medium | $O(n)$ / $O(n)$ | Banned: `sort`, `sorted` (hash set sequence starts) |

---

## 2. Pedagogical Architecture

### 2.1 Four-Tier Progressive Hint Ladders
Every exercise module contains `HINTS: list[str]` structured across 4 progressive tiers:
1. **Tier 1 (Core Intuition)**: Conceptual mathematical/logical observations without spoiling the algorithm.
2. **Tier 2 (Algorithmic Pattern)**: Identifies the optimal data structure and access pattern (e.g. bucket sort by frequency, prefix/suffix accumulators, hash set sequence origin detection).
3. **Tier 3 (Invariants & Edge Cases)**: Details corner cases (empty lists, duplicates, single elements, negative values, delimiter collisions).
4. **Tier 4 (Skeleton Blueprint)**: Step-by-step pseudo-code guiding direct Python implementation.

### 2.2 AST Guardrails & Complexity Enforcement
- The AST complexity visitor (`check_banned_syntax`) inspects user submissions prior to execution.
- Disallowed methods (`sort`, `sorted`, `Counter`) and operators (division `/`, `//`) raise informative `BannedSyntaxError` exceptions explaining why the shortcut violates the problem's learning objectives.
- `StepCounter` monitors loop and recursion iterations to block quadratic or infinite loops on large test cases.

### 2.3 Diagnostic Visualizers & Order-Independent Matching
- **Valid Sudoku**: If row, column, or 3x3 box duplicates occur, `format_grid` renders the offending board in ASCII with conflicting coordinates highlighted.
- **Group Anagrams**: Normalizes group order and inner element order (`sorted([sorted(g) for g in actual]) == sorted([sorted(g) for g in expected])`) to allow valid permutations while preserving strict correctness.
- **Top K Frequent Elements**: Validates that returned elements match expected top $K$ items regardless of output ordering.

---

## 3. Directory Layout & Manifest

```
exercises/01_arrays_and_hashing/
├── 01_contains_duplicate.py
├── 02_valid_anagram.py
├── 03_two_sum.py
├── 04_group_anagrams.py
├── 05_top_k_frequent_elements.py
├── 06_product_of_array_except_self.py
├── 07_valid_sudoku.py
├── 08_encode_and_decode_strings.py
└── 09_longest_consecutive_sequence.py

solutions/01_arrays_and_hashing/
├── 01_contains_duplicate.py
├── 02_valid_anagram.py
├── 03_two_sum.py
├── 04_group_anagrams.py
├── 05_top_k_frequent_elements.py
├── 06_product_of_array_except_self.py
├── 07_valid_sudoku.py
├── 08_encode_and_decode_strings.py
└── 09_longest_consecutive_sequence.py
```

### Manifest Update (`src/neetlings/manifest.py`)
`CATEGORIES[0]` (`arrays_and_hashing`) is updated to list all 9 exercise identifiers in order.

---

## 4. Verification & Quality Gates

1. **Unit Testing (`tests/test_reference_solutions.py`)**: All 9 reference solutions are tested using `evaluate_code()`, verifying 100% test case pass rates and strict adherence to step limits.
2. **AST Guardrail Testing (`tests/test_complexity.py`)**: Dedicated test cases asserting that AST guardrails reject disallowed operations (e.g., sorting on Bucket Sort or division on Product of Array).
3. **Bundle Build & Web Testing (`tests/test_bundler.py`, `tests/test_web_assets.py`)**: Verifies compilation into `playground-bundle.json` containing all 9 exercises, and confirms static web asset contracts.
4. **Tooling Gates**:
   - `uv run pytest -v`
   - `uv run ruff check src tests exercises solutions scripts`
   - `uv run pyright src`
