# Design Spec: Clean Exercise Hints & Fix Playground Test Execution Engine

**Date:** 2026-09-06  
**Status:** Approved  
**Topic:** Exercise Hints Removal, Bundle Decoupling, and Web Playground Test Runner Execution Fix  

---

## 1. Problem Statement & Motivation

### A. Hint Leaks in Exercise Files
Every exercise file under `exercises/**/*.py` contains a `HINTS = [...]` block directly above `class Solution:`. When a student opens the exercise file in a local editor or Monaco editor in the browser, the progressive hints are immediately visible in the starter code. This ruins the discovery process and makes the interactive web Hint Ladder UI redundant.

### B. Playground Test Runner "Always Passes" Bug
When the student clicks "Run" in the web playground:
1. `playground.js` posts a message to `playground-worker.js` with `testCases: []` and an unfulfilled comment `// Handled by Python test_runner evaluating test_solution()`.
2. `test_runner.py`'s `evaluate_code()` receives `test_cases = []`, iterates 0 times, and returns `status: "PASSED"` with `passedCount: 0` and `totalCount: 0`.
3. Because `status === "PASSED"`, the web UI displays a green "PASSED" pill and immediately records the exercise as "Solved" in `localStorage`, even when the code has `raise NotImplementedError`!
4. Additionally, `playground.js` hardcoded `bannedCalls: ["sort"]` globally, which would erroneously flag legitimate sorts (such as in 3Sum).

---

## 2. Requirements & Non-Functional Goals

1. **Clean Exercise Files**:
   - `exercises/**/*.py` must NOT contain `HINTS = [...]`.
   - Exercise files must contain only: problem docstring, `class Solution:`, `TEST_CASES = [...]`, and `def test_solution()`.
2. **Canonical Hint Preservation**:
   - `solutions/**/*.py` retains all 4-tier progressive hints in `HINTS = [...]`.
3. **Decoupled Asset Bundling**:
   - `src/neetlings/bundler.py` extracts hints from `solutions/` and injects `"hints": list[str]` into `bundle["exercises"][ex_id]`.
   - `bundler.py` extracts per-exercise `bannedCalls` and `bannedOps` from `manifest.py` into `bundle["exercises"][ex_id]`.
   - `bundler.py` ensures `ex["code"]` is strictly hint-free.
4. **Reliable Test Execution**:
   - If `test_cases` is not passed or empty, `evaluate_code` automatically resolves test cases from `canonical_code` (e.g. `ex.solution`) or from `scope["TEST_CASES"]`.
   - If resolved test cases are empty (`len == 0`), `evaluate_code` MUST return `status: "ERROR"`.
   - If an exception occurs (e.g., `NotImplementedError`, index error, infinite loop timeout), `evaluate_code` records the case as `FAILED`, returns `status: "FAILED"`, and includes the error traceback.
   - The web playground only marks an exercise as "Solved" when `status === "PASSED"` and `passedCount > 0`.
5. **Quality Assurance**:
   - 100% pass rate on full test suite (`uv run pytest -v`).
   - Clean linting (`ruff`) and strict typing (`pyright`).

---

## 3. Detailed Component Architecture

### 3.1 Exercise Files Cleanup
- Strip `HINTS = [...]` and associated comments/blank lines from all 30 exercise files across `exercises/01_arrays_and_hashing/` through `exercises/18_bit_manipulation/`.

### 3.2 Manifest Exercise Rules (`src/neetlings/manifest.py`)
- Define `EXERCISE_RULES: dict[str, dict[str, list[str]]]`:
  - `"06_product_of_array_except_self"`: `{"banned_ops": ["/", "//"]}`
  - `"02_two_sum_ii_input_array_is_sorted"`: `{"banned_calls": ["dict", "defaultdict"]}`
  - Other exercises can declare specific banned calls/ops as needed.

### 3.3 Asset Bundler (`src/neetlings/bundler.py`)
- Add helper `extract_hints_from_source(source: str) -> list[str]` using AST or regex to parse `HINTS = [...]`.
- During bundle generation:
  - Read `solution_file`. If present, extract `hints`. If hints are empty, fallback to extracting from `ex_file`.
  - Strip any remaining `HINTS = [...]` definition from `ex_file` content before assigning to `exercise["code"]`.
  - Look up rules in `EXERCISE_RULES` and populate `exercise["bannedCalls"]` and `exercise["bannedOps"]`.
  - Add `"hints": hints` to the exercise record.

### 3.4 Test Runner (`src/neetlings/test_runner.py`)
- Update `evaluate_code` signature:
  ```python
  def evaluate_code(
      code_str: str,
      test_cases: list[dict[str, Any]] | None = None,
      method_name: str = "solution",
      banned_calls: list[str] | None = None,
      banned_ops: list[str] | None = None,
      canonical_code: str | None = None,
  ) -> dict[str, Any]:
  ```
- If `not test_cases`:
  - If `canonical_code`:
    - Create an isolated scope with `{"ListNode": ListNode, "TreeNode": TreeNode, "Interval": Interval}`.
    - `exec(canonical_code, canonical_scope)`.
    - `test_cases = canonical_scope.get("TEST_CASES")`.
  - If still `not test_cases`:
    - `test_cases = scope.get("TEST_CASES")`.
- If `not test_cases`:
  - Return:
    ```python
    {
        "status": "ERROR",
        "passedCount": 0,
        "totalCount": 0,
        "durationMs": 0.0,
        "stdout": stdout_buf.getvalue(),
        "error": "Error: No test cases found to evaluate code.",
        "cases": [],
        "diagnosticDiff": None,
    }
    ```
- When running `actual = run_with_timeout(fn, args, timeout=2.0)`:
  - Catch `Exception as exc`:
    - Mark case as `status: "FAILED"`.
    - Record `error: traceback.format_exc()`.
    - Set `all_passed = False`.
    - Stop further case execution.
- Final status check:
  - `status: "PASSED" if all_passed and len(test_cases) > 0 else "FAILED"`.

### 3.5 Web Client & Worker (`playground.js` & `playground-worker.js`)
- In `playground.js`:
  - `runCode()`:
    - Send `solutionCode: ex.solution || ex.code`.
    - Send `bannedCalls: ex.bannedCalls || []`.
    - Send `bannedOps: ex.bannedOps || []`.
  - `renderProblemPane()`:
    - Retrieve hints via `ex.hints || this.extractHints(ex.solution || ex.code)`.
- In `playground-worker.js`:
  - In `RUN` handler, pass `msg.solutionCode`, `msg.bannedOps`, and `msg.bannedCalls` to `evaluate_code`.

---

## 4. Verification & Testing Plan

1. **`tests/test_test_runner.py`**:
   - `test_evaluate_failing_code_not_implemented`: Verifies that code raising `NotImplementedError` returns `status: "FAILED"`, `passedCount: 0`.
   - `test_evaluate_empty_test_cases_error`: Verifies that empty test cases return `status: "ERROR"`.
   - `test_evaluate_with_canonical_code`: Verifies that `evaluate_code` resolves test cases from `canonical_code` when `test_cases` is omitted.
2. **`tests/test_bundler.py`**:
   - Verify every exercise in `generate_bundle()` has `"hints"` list of length >= 3.
   - Verify no exercise in `bundle["exercises"]` has `HINTS = [` in its `code`.
   - Verify `bannedCalls` and `bannedOps` exist on exercises matching `EXERCISE_RULES`.
3. **Rebuild Bundle**:
   - Run `python scripts/build_playground_bundle.py` and ensure `docs/assets/playground/playground-bundle.json` is updated and valid.
4. **Full Suite**:
   - `uv run pytest -v`
   - `uv run ruff check src tests exercises solutions scripts`
   - `uv run pyright src`
