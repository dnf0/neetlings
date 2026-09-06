# Curriculum Expansion: Arrays & Hashing (9 Problems) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose an execution mode:
> 1. `superpowers:subagent-driven-development` (recommended for multi-agent reviews, backed by `SKILL.state` / `.agent-state/state.json`)
> 2. `agent-rules:stateful-execution` (SKILL.state) (recommended for deterministic single-agent linear execution)
> 3. `superpowers:executing-plans` (batch execution with manual checkpoints)
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the remaining 8 problems for Category 1 (Arrays & Hashing) with starter templates, optimal reference solutions, 4-tier progressive hints, AST guardrails, and full test suites, bringing Arrays & Hashing to 9 fully validated problems.

**Architecture:** Each problem is authored as a standalone executable module in `exercises/01_arrays_and_hashing/` and verified in `solutions/01_arrays_and_hashing/`. The curriculum manifest `src/neetlings/manifest.py` registers all 9 exercise IDs, and `scripts/build_playground_bundle.py` compiles them into `docs/assets/playground/playground-bundle.json` for in-browser execution.

**Tech Stack:** Python 3.12, Pytest, Ruff, Pyright, Hatchling.

## Global Constraints
- Target Python 3.12 syntax with explicit type annotations.
- Every exercise must provide docstring, `HINTS` (4 tiers), AST guardrails (`BANNED_CALLS`, `BANNED_OPS`, `STEP_LIMIT`), `TEST_CASES`, and `test_solution(solution_cls)`.
- Reference solutions must be optimal in time and space complexity without using disallowed functions.
- All code must pass `ruff check`, `pyright`, and `pytest`.
- Never commit directly to `main`; work in an isolated worktree.

---

### Task 1: Valid Anagram & Two Sum

- **Depends on:** none

**Files:**
- Create: `exercises/01_arrays_and_hashing/02_valid_anagram.py`
- Create: `solutions/01_arrays_and_hashing/02_valid_anagram.py`
- Create: `exercises/01_arrays_and_hashing/03_two_sum.py`
- Create: `solutions/01_arrays_and_hashing/03_two_sum.py`
- Test: `tests/test_reference_solutions.py`

**Interfaces:**
- Consumes: `evaluate_code` from `neetlings.test_runner`
- Produces: `02_valid_anagram` (`isAnagram(s: str, t: str) -> bool`) and `03_two_sum` (`twoSum(nums: list[int], target: int) -> list[int]`)

- [ ] **Step 1: Create starter templates**
Create `exercises/01_arrays_and_hashing/02_valid_anagram.py` and `exercises/01_arrays_and_hashing/03_two_sum.py` with 4-tier `HINTS`, AST configuration, `TEST_CASES`, and starter `class Solution` raising `NotImplementedError`.

- [ ] **Step 2: Create reference solutions**
Create `solutions/01_arrays_and_hashing/02_valid_anagram.py` ($O(n)$ time, $O(1)$ extra space using frequency array/dict, banned `sort`, `Counter`) and `solutions/01_arrays_and_hashing/03_two_sum.py` ($O(n)$ one-pass complement hash map, step limit 200,000).

- [ ] **Step 3: Run pytest to verify solutions**
Run: `uv run pytest tests/test_reference_solutions.py -v`
Expected: PASS for all discovered reference solutions.

- [ ] **Step 4: Lint and typecheck**
Run: `uv run ruff check exercises solutions && uv run pyright src`
Expected: 0 errors.

- [ ] **Step 5: Commit**
```bash
git add exercises/01_arrays_and_hashing/02_valid_anagram.py solutions/01_arrays_and_hashing/02_valid_anagram.py exercises/01_arrays_and_hashing/03_two_sum.py solutions/01_arrays_and_hashing/03_two_sum.py
git commit --no-gpg-sign -m "feat(curriculum): add Valid Anagram and Two Sum exercises and reference solutions"
```

---

### Task 2: Group Anagrams & Top K Frequent Elements

- **Depends on:** Task 1

**Files:**
- Create: `exercises/01_arrays_and_hashing/04_group_anagrams.py`
- Create: `solutions/01_arrays_and_hashing/04_group_anagrams.py`
- Create: `exercises/01_arrays_and_hashing/05_top_k_frequent_elements.py`
- Create: `solutions/01_arrays_and_hashing/05_top_k_frequent_elements.py`
- Test: `tests/test_reference_solutions.py`

**Interfaces:**
- Produces:
  - `04_group_anagrams`: `groupAnagrams(strs: list[str]) -> list[list[str]]`
  - `05_top_k_frequent_elements`: `topKFrequent(nums: list[int], k: int) -> list[int]`

- [ ] **Step 1: Create starter templates**
Create `exercises/01_arrays_and_hashing/04_group_anagrams.py` and `exercises/01_arrays_and_hashing/05_top_k_frequent_elements.py` with 4-tier hints, normalized multiset test comparisons, and starter skeletons.

- [ ] **Step 2: Create reference solutions**
Create `solutions/01_arrays_and_hashing/04_group_anagrams.py` (frequency count tuple hash keys, $O(m \cdot n)$ time) and `solutions/01_arrays_and_hashing/05_top_k_frequent_elements.py` ($O(n)$ bucket sort without calling `sort` or `sorted`).

- [ ] **Step 3: Run pytest to verify solutions**
Run: `uv run pytest tests/test_reference_solutions.py -v`
Expected: PASS.

- [ ] **Step 4: Lint and typecheck**
Run: `uv run ruff check exercises solutions && uv run pyright src`
Expected: 0 errors.

- [ ] **Step 5: Commit**
```bash
git add exercises/01_arrays_and_hashing/04_group_anagrams.py solutions/01_arrays_and_hashing/04_group_anagrams.py exercises/01_arrays_and_hashing/05_top_k_frequent_elements.py solutions/01_arrays_and_hashing/05_top_k_frequent_elements.py
git commit --no-gpg-sign -m "feat(curriculum): add Group Anagrams and Top K Frequent Elements"
```

---

### Task 3: Product of Array Except Self & Valid Sudoku

- **Depends on:** Task 2

**Files:**
- Create: `exercises/01_arrays_and_hashing/06_product_of_array_except_self.py`
- Create: `solutions/01_arrays_and_hashing/06_product_of_array_except_self.py`
- Create: `exercises/01_arrays_and_hashing/07_valid_sudoku.py`
- Create: `solutions/01_arrays_and_hashing/07_valid_sudoku.py`
- Test: `tests/test_reference_solutions.py`

**Interfaces:**
- Produces:
  - `06_product_of_array_except_self`: `productExceptSelf(nums: list[int]) -> list[int]` (Banned `/`, `//`)
  - `07_valid_sudoku`: `isValidSudoku(board: list[list[str]]) -> bool`

- [ ] **Step 1: Create starter templates**
Create `exercises/01_arrays_and_hashing/06_product_of_array_except_self.py` and `exercises/01_arrays_and_hashing/07_valid_sudoku.py` with 4-tier hints, matrix/array test cases, and starter skeletons.

- [ ] **Step 2: Create reference solutions**
Create `solutions/01_arrays_and_hashing/06_product_of_array_except_self.py` ($O(n)$ time, $O(1)$ extra space prefix and postfix accumulator without division) and `solutions/01_arrays_and_hashing/07_valid_sudoku.py` (row, col, and `(r // 3, c // 3)` box hash sets).

- [ ] **Step 3: Run pytest to verify solutions**
Run: `uv run pytest tests/test_reference_solutions.py -v`
Expected: PASS.

- [ ] **Step 4: Lint and typecheck**
Run: `uv run ruff check exercises solutions && uv run pyright src`
Expected: 0 errors.

- [ ] **Step 5: Commit**
```bash
git add exercises/01_arrays_and_hashing/06_product_of_array_except_self.py solutions/01_arrays_and_hashing/06_product_of_array_except_self.py exercises/01_arrays_and_hashing/07_valid_sudoku.py solutions/01_arrays_and_hashing/07_valid_sudoku.py
git commit --no-gpg-sign -m "feat(curriculum): add Product of Array Except Self and Valid Sudoku"
```

---

### Task 4: Encode and Decode Strings & Longest Consecutive Sequence

- **Depends on:** Task 3

**Files:**
- Create: `exercises/01_arrays_and_hashing/08_encode_and_decode_strings.py`
- Create: `solutions/01_arrays_and_hashing/08_encode_and_decode_strings.py`
- Create: `exercises/01_arrays_and_hashing/09_longest_consecutive_sequence.py`
- Create: `solutions/01_arrays_and_hashing/09_longest_consecutive_sequence.py`
- Test: `tests/test_reference_solutions.py`

**Interfaces:**
- Produces:
  - `08_encode_and_decode_strings`: `encode(strs: list[str]) -> str`, `decode(s: str) -> list[str]`
  - `09_longest_consecutive_sequence`: `longestConsecutive(nums: list[int]) -> int` (Banned `sort`, `sorted`)

- [ ] **Step 1: Create starter templates**
Create `exercises/01_arrays_and_hashing/08_encode_and_decode_strings.py` and `exercises/01_arrays_and_hashing/09_longest_consecutive_sequence.py` with 4-tier hints, edge cases, and starter skeletons.

- [ ] **Step 2: Create reference solutions**
Create `solutions/01_arrays_and_hashing/08_encode_and_decode_strings.py` (length-prefixed chunking `f"{len(s)}#{s}"`) and `solutions/01_arrays_and_hashing/09_longest_consecutive_sequence.py` ($O(n)$ hash set sequence start detection without sorting).

- [ ] **Step 3: Run pytest to verify solutions**
Run: `uv run pytest tests/test_reference_solutions.py -v`
Expected: PASS.

- [ ] **Step 4: Lint and typecheck**
Run: `uv run ruff check exercises solutions && uv run pyright src`
Expected: 0 errors.

- [ ] **Step 5: Commit**
```bash
git add exercises/01_arrays_and_hashing/08_encode_and_decode_strings.py solutions/01_arrays_and_hashing/08_encode_and_decode_strings.py exercises/01_arrays_and_hashing/09_longest_consecutive_sequence.py solutions/01_arrays_and_hashing/09_longest_consecutive_sequence.py
git commit --no-gpg-sign -m "feat(curriculum): add Encode/Decode Strings and Longest Consecutive Sequence"
```

---

### Task 5: Manifest, AST Guardrail Tests, Bundler & Web Assets Integration

- **Depends on:** Task 4

**Files:**
- Modify: `src/neetlings/manifest.py:11-20`
- Modify: `tests/test_complexity.py`
- Modify: `tests/test_bundler.py`
- Modify: `tests/test_web_assets.py`
- Modify: `docs/assets/playground/playground-bundle.json`

**Interfaces:**
- Consumes: all 9 exercises from `exercises/01_arrays_and_hashing/`
- Produces: Updated curriculum manifest with 9 Arrays & Hashing exercises, verified AST enforcement, and built bundle.

- [ ] **Step 1: Update manifest.py**
Update `CATEGORIES[0]` in `src/neetlings/manifest.py` to register all 9 exercise IDs.

- [ ] **Step 2: Add AST guardrail tests**
Update `tests/test_complexity.py` with test cases verifying:
  - Disallowed `sort` in `top_k_frequent_elements` or `longest_consecutive_sequence` raises `BannedSyntaxError`.
  - Disallowed `/` or `//` in `product_of_array_except_self` raises `BannedSyntaxError`.

- [ ] **Step 3: Rebuild bundle and verify bundler tests**
Run: `python scripts/build_playground_bundle.py`
Run: `uv run pytest tests/test_bundler.py tests/test_web_assets.py -v`
Expected: PASS, 26 total exercises in bundle.

- [ ] **Step 4: Full test suite verification**
Run: `uv run pytest -v`
Run: `uv run ruff check src tests exercises solutions scripts`
Run: `uv run pyright src`
Expected: All 28+ tests pass, 0 lint errors, 0 type errors.

- [ ] **Step 5: Commit**
```bash
git add src/neetlings/manifest.py tests/test_complexity.py tests/test_bundler.py tests/test_web_assets.py
git commit --no-gpg-sign -m "feat(curriculum): register all 9 Arrays & Hashing problems and verify bundle compilation"
```
