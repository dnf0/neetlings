# Curriculum Expansion Plan: Two Pointers (5 Problems)

> **For agentic workers:** REQUIRED SUB-SKILL: Choose an execution mode:
> 1. `superpowers:subagent-driven-development` (recommended for multi-agent reviews, backed by `SKILL.state` / `.agent-state/state.json`)
> 2. `agent-rules:stateful-execution` (SKILL.state) (recommended for deterministic single-agent linear execution)
> 3. `superpowers:executing-plans` (batch execution with manual checkpoints)
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand Neetlings Category 2 (Two Pointers) from 1 problem to all 5 canonical NeetCode 150 problems with complete exercises, reference solutions, AST guardrails, ASCII elevation visualizers, and web bundle integration.

**Architecture:** Each problem is authored as a self-contained module in `exercises/02_two_pointers/` and `solutions/02_two_pointers/` adhering to the standard 4-tier progressive hint ladder. ASCII elevation and water diagnostics are added to `src/neetlings/visualizers.py` to render cross-section elevation profiles on test failure.

**Tech Stack:** Python 3.12, Pyodide v0.26, AST, pytest, ruff, pyright.

## Global Constraints
- Target Python 3.12 with strict typing and ruff/pyright compliance.
- 4-tier progressive hint ladder in every exercise module (`HINTS`).
- AST complexity enforcement: ban `dict` and `defaultdict` in Two Sum II to enforce O(1) space; enforce step limits on Container With Most Water and Trapping Rain Water.
- All reference solutions must run cleanly and pass 100% of test cases in `tests/test_reference_solutions.py`.

---

### Task 1: Two Sum II & 3Sum

- **Depends on:** none

**Files:**
- Create: `exercises/02_two_pointers/02_two_sum_ii_input_array_is_sorted.py`
- Create: `solutions/02_two_pointers/02_two_sum_ii_input_array_is_sorted.py`
- Create: `exercises/02_two_pointers/03_3sum.py`
- Create: `solutions/02_two_pointers/03_3sum.py`

**Interfaces:**
- Produces:
  - `Solution.twoSum(self, numbers: list[int], target: int) -> list[int]` (1-indexed output, O(n) time, O(1) space)
  - `Solution.threeSum(self, nums: list[int]) -> list[list[int]]` (O(n^2) time, O(1) space excluding output)

- [ ] **Step 1: Write Two Sum II exercise and failing solution test**
  - Implement starter template `exercises/02_two_pointers/02_two_sum_ii_input_array_is_sorted.py` raising `NotImplementedError`.
  - Create test cases covering normal, negative numbers, single pair, large differences, zeros.

- [ ] **Step 2: Implement optimal Two Sum II reference solution**
  - Implement `solutions/02_two_pointers/02_two_sum_ii_input_array_is_sorted.py` using two pointers `left = 0, right = len(numbers) - 1`. Return `[left + 1, right + 1]`.

- [ ] **Step 3: Write 3Sum exercise and failing solution test**
  - Implement starter template `exercises/02_two_pointers/03_3sum.py` raising `NotImplementedError`.
  - Test cases covering all zeros `[0, 0, 0]`, duplicate numbers `[-1, -1, -1, 2, 2]`, no triplets `[0, 1, 1]`.
  - Assert using order-independent format: `sorted([sorted(t) for t in actual]) == sorted([sorted(t) for t in expected])`.

- [ ] **Step 4: Implement optimal 3Sum reference solution**
  - Implement `solutions/02_two_pointers/03_3sum.py` sorting `nums` first, iterating `i`, and using two pointers `left, right` on the remainder while skipping duplicate values.

- [ ] **Step 5: Verify tests and quality**
  - Run: `uv run pytest tests/test_reference_solutions.py -v`
  - Run: `uv run ruff check exercises solutions`
  - Run: `uv run pyright src`

- [ ] **Step 6: Commit**
  - `git add exercises/02_two_pointers/ solutions/02_two_pointers/`
  - `git commit --no-gpg-sign -m "feat(curriculum): add Two Sum II and 3Sum exercises and solutions"`

---

### Task 2: Container With Most Water & Trapping Rain Water

- **Depends on:** Task 1

**Files:**
- Create: `exercises/02_two_pointers/04_container_with_most_water.py`
- Create: `solutions/02_two_pointers/04_container_with_most_water.py`
- Create: `exercises/02_two_pointers/05_trapping_rain_water.py`
- Create: `solutions/02_two_pointers/05_trapping_rain_water.py`

**Interfaces:**
- Produces:
  - `Solution.maxArea(self, height: list[int]) -> int` (O(n) time, O(1) space)
  - `Solution.trap(self, height: list[int]) -> int` (O(n) time, O(1) space)

- [ ] **Step 1: Write Container With Most Water exercise and tests**
  - Implement starter template `exercises/02_two_pointers/04_container_with_most_water.py`.
  - Add test cases: standard, staircase, two elements, identical heights.

- [ ] **Step 2: Implement optimal Container With Most Water reference solution**
  - Implement `solutions/02_two_pointers/04_container_with_most_water.py` using two pointers moving the shorter line inward.

- [ ] **Step 3: Write Trapping Rain Water exercise and tests**
  - Implement starter template `exercises/02_two_pointers/05_trapping_rain_water.py`.
  - Add test cases: standard LeetCode profile, flat terrain `[0,0,0]`, strictly descending `[5,4,3,2,1]`, strictly ascending `[1,2,3,4,5]`, V-valley `[3,0,3]`.

- [ ] **Step 4: Implement optimal Trapping Rain Water reference solution**
  - Implement `solutions/02_two_pointers/05_trapping_rain_water.py` using two pointers with `left_max` and `right_max` tracking in $O(1)$ extra space.

- [ ] **Step 5: Verify tests and quality**
  - Run: `uv run pytest tests/test_reference_solutions.py -v`
  - Run: `uv run ruff check exercises solutions`
  - Run: `uv run pyright src`

- [ ] **Step 6: Commit**
  - `git add exercises/02_two_pointers/ solutions/02_two_pointers/`
  - `git commit --no-gpg-sign -m "feat(curriculum): add Container With Most Water and Trapping Rain Water"`

---

### Task 3: ASCII Elevation & Water Diagnostics

- **Depends on:** Task 2

**Files:**
- Modify: `src/neetlings/visualizers.py`
- Modify: `tests/test_visualizers.py`

**Interfaces:**
- Produces:
  - `render_ascii_elevation(heights: list[int], water: list[int] | None = None) -> str`
  - `format_rainwater_diff(heights: list[int], expected: int, actual: int) -> str`

- [ ] **Step 1: Write failing test for elevation visualizers**
  - In `tests/test_visualizers.py`, add tests checking ASCII elevation diagram formatting for standard terrain and water layers.

- [ ] **Step 2: Implement `render_ascii_elevation` and `format_rainwater_diff`**
  - In `src/neetlings/visualizers.py`, implement column elevation rendering using `#` for ground, `~` for water, `.` for air.

- [ ] **Step 3: Verify tests and quality**
  - Run: `uv run pytest tests/test_visualizers.py -v`
  - Run: `uv run ruff check src tests`
  - Run: `uv run pyright src`

- [ ] **Step 4: Commit**
  - `git add src/neetlings/visualizers.py tests/test_visualizers.py`
  - `git commit --no-gpg-sign -m "feat(visualizers): implement ASCII elevation and rainwater diagnostic diffs"`

---

### Task 4: Manifest Update, AST Guardrails, Bundler & Web Assets Integration

- **Depends on:** Task 3

**Files:**
- Modify: `src/neetlings/manifest.py`
- Modify: `tests/test_complexity.py`
- Modify: `tests/test_bundler.py`
- Modify: `tests/test_web_assets.py`
- Modify: `docs/assets/playground/playground-bundle.json`

**Interfaces:**
- Produces:
  - Updated `CATEGORIES[1]` in `manifest.py` containing all 5 Two Pointers exercise IDs.
  - Recompiled `docs/assets/playground/playground-bundle.json` with 30 total exercises.

- [ ] **Step 1: Update manifest with all 5 Two Pointers IDs**
  - In `src/neetlings/manifest.py`, update `two_pointers` category with `01_valid_palindrome`, `02_two_sum_ii_input_array_is_sorted`, `03_3sum`, `04_container_with_most_water`, `05_trapping_rain_water`.

- [ ] **Step 2: Add AST guardrail tests for Two Pointers**
  - In `tests/test_complexity.py`, add test verifying that `dict` calls in Two Sum II are flagged if disallowed.

- [ ] **Step 3: Update bundler tests and recompile bundle**
  - Update `tests/test_bundler.py` and `tests/test_web_assets.py` to assert total exercise count >= 30.
  - Run `python scripts/build_playground_bundle.py`.

- [ ] **Step 4: Run full test suite and quality checks**
  - Run: `uv run pytest -v`
  - Run: `uv run ruff check src tests exercises solutions scripts`
  - Run: `uv run pyright src`

- [ ] **Step 5: Commit**
  - `git add src/ tests/ scripts/ docs/assets/playground/playground-bundle.json`
  - `git commit --no-gpg-sign -m "feat(curriculum): register all 5 Two Pointers problems and compile bundle"`
