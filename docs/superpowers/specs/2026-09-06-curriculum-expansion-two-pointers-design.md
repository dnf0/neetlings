# Curriculum Expansion Design Spec: Category 2 — Two Pointers (5 Problems)

**Date:** 2026-09-06  
**Status:** Approved  
**Category:** Two Pointers (NeetCode 150)  

---

## 1. Executive Summary

This specification defines the complete expansion of Category 2 (**Two Pointers**) in Neetlings from its initial single exercise (`01_valid_palindrome`) to all **5 canonical problems** from the NeetCode 150 curriculum.

It formalizes:
- Exercise starter templates and optimal reference solutions for problems 02 through 05.
- AST guardrails banning hash maps on Two Sum II (enforcing true $O(1)$ space).
- ASCII elevation and water diagnostics in `src/neetlings/visualizers.py` for graphical test feedback.
- Category manifest registration and playground bundle compilation to 30 exercises.

---

## 2. Problem Catalog & Specifications

### 2.1 Problem Roster

| File Name | Title | Method Signature | Time Target | Space Target | Algorithmic Invariants |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_valid_palindrome.py` | Valid Palindrome | `isPalindrome(self, s: str) -> bool` | $O(n)$ | $O(1)$ | *(Already implemented)* Alphanumeric filter & two-pointer convergence. |
| `02_two_sum_ii_input_array_is_sorted.py` | Two Sum II | `twoSum(self, numbers: list[int], target: int) -> list[int]` | $O(n)$ | $O(1)$ | 1-based index return `[i + 1, j + 1]`. AST ban on `dict` & `defaultdict` to force $O(1)$ two-pointer solution. |
| `03_3sum.py` | 3Sum | `threeSum(self, nums: list[int]) -> list[list[int]]` | $O(n^2)$ | $O(1)^*$ | No duplicate triplets. Triplet and list order-independent multiset assertion. Array sort permitted. |
| `04_container_with_most_water.py` | Container With Most Water | `maxArea(self, height: list[int]) -> int` | $O(n)$ | $O(1)$ | Boundary squeeze moving shorter line. Step counter aborts $O(n^2)$ nested loops. |
| `05_trapping_rain_water.py` | Trapping Rain Water | `trap(self, height: list[int]) -> int` | $O(n)$ | $O(1)$ | Bidirectional convergence with `left_max` and `right_max`. Strictly $O(1)$ auxiliary space. |

---

## 3. Visualizers & Diagnostic Diffing

### 3.1 ASCII Elevation Diagram
To provide intuitive diagnostics in the web playground when test cases fail on `04_container_with_most_water` and `05_trapping_rain_water`, `src/neetlings/visualizers.py` provides:

- `render_ascii_elevation(heights: list[int], water: list[int] | None = None) -> str`:
  Renders columns using `#` for solid elevation, `~` for trapped water, and `.` for empty airspace.
- `format_rainwater_diff(heights: list[int], expected: int, actual: int) -> str`:
  Integrates into `test_runner.py`'s `diagnosticDiff` return object on failure.

---

## 4. AST Guardrails & Security

- **`02_two_sum_ii`**: AST check flags disallowed type instantiation `dict(...)` or literal dict `{...}` to prevent falling back to the hash map pattern from Two Sum.
- **`04_container_with_most_water` & `05_trapping_rain_water`**: Step limit threshold ensures $O(n^2)$ nested loops fail with `StepLimitExceeded`.

---

## 5. Manifest & Web Asset Integration

- **Manifest**: Update `CATEGORIES[1]` (`id: "two_pointers"`) in `src/neetlings/manifest.py` with all 5 exercise IDs.
- **Playground Bundle**: Rebuild `docs/assets/playground/playground-bundle.json` containing 30 total exercises (9 Arrays & Hashing + 5 Two Pointers + 16 remaining placeholders).
- **Test Suite**: Update test thresholds in `test_bundler.py` and `test_web_assets.py` to expect >= 30 exercises.

---

## 6. Verification Checklist

1. `uv run pytest -v` passes 100% of tests.
2. `uv run ruff check src tests exercises solutions scripts` produces 0 violations.
3. `uv run pyright src` passes with 0 errors/warnings.
4. `python scripts/build_playground_bundle.py` succeeds.
5. All reference solutions in `solutions/02_two_pointers/` execute optimally.
