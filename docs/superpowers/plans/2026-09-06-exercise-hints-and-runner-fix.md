# Clean Exercise Hints & Fix Playground Test Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose an execution mode:
> 1. `superpowers:subagent-driven-development` (recommended for multi-agent reviews, backed by `SKILL.state` / `.agent-state/state.json`)
> 2. `agent-rules:stateful-execution` (SKILL.state) (recommended for deterministic single-agent linear execution)
> 3. `superpowers:executing-plans` (batch execution with manual checkpoints)
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strip progressive hints from all 30 exercise starter files, preserve canonical hints in reference solutions, decouple hints into the WebAssembly playground bundle, and fix the playground test runner so test cases execute and uncompleted/failing solutions fail.

**Architecture:**
1. Clean curriculum files: strip `HINTS = [...]` from all `exercises/**/*.py` files.
2. Manifest rules: add `EXERCISE_RULES` to `manifest.py` for per-exercise banned calls and ops.
3. Test runner: update `evaluate_code` in `test_runner.py` to resolve test cases from `canonical_code` or `scope["TEST_CASES"]`, flag exceptions (`NotImplementedError`) as `FAILED`, and reject 0-test runs as `ERROR`.
4. Asset bundler: update `bundler.py` to extract hints from `solutions/`, inject `hints`, `bannedCalls`, and `bannedOps` into `playground-bundle.json`, and ensure `code` is hint-free.
5. Web client & worker: update `playground-worker.js` and `playground.js` to pass `solutionCode`, `bannedCalls`, and `bannedOps`, reading hints from `ex.hints`.

**Tech Stack:** Python 3.12, Pytest, Ruff, Pyright, Pyodide (WASM), Vanilla JS / Monaco Editor.

## Global Constraints
- Target: Python 3.12 style with explicit typing, small functions, and reproducible CLI steps.
- Linting & Typing: `ruff` clean, `pyright` clean.
- GPG signing: Always skip GPG key verification (`--no-gpg-sign`).
- Git account: Always use `dnf0` account (`5225715+dnf0@users.noreply.github.com`) and remote `https://github.com/dnf0/neetlings`.

---

### Task 1: Clean Exercise Starter Files & Update Manifest Exercise Rules

- **Depends on:** none

**Files:**
- Create: `tests/test_exercise_cleanliness.py`
- Modify: `src/neetlings/manifest.py:1-40`
- Modify: `exercises/**/*.py` (all 30 exercise files)

**Interfaces:**
- Produces: `EXERCISE_RULES: dict[str, dict[str, list[str]]]` in `neetlings.manifest`.
- Guarantee: Every exercise in `exercises/**/*.py` is syntactically valid and contains no `HINTS = [` assignment.

- [ ] **Step 1: Write failing test in `tests/test_exercise_cleanliness.py`**

```python
"""Tests verifying that exercise files are clean of spoiler hints and syntactically valid."""

import ast
from pathlib import Path

from neetlings.manifest import EXERCISE_RULES


def test_no_hints_in_exercise_files() -> None:
    exercises_dir = Path("exercises")
    ex_files = sorted(exercises_dir.rglob("*.py"))
    assert len(ex_files) >= 30, f"Expected at least 30 exercise files, found {len(ex_files)}"

    for ex_file in ex_files:
        content = ex_file.read_text(encoding="utf-8")
        assert "HINTS = [" not in content, f"Spoiler hints found in {ex_file}"
        # Ensure file parses as valid Python
        ast.parse(content, filename=str(ex_file))


def test_exercise_rules_manifest() -> None:
    assert isinstance(EXERCISE_RULES, dict)
    assert "06_product_of_array_except_self" in EXERCISE_RULES
    assert EXERCISE_RULES["06_product_of_array_except_self"].get("banned_ops") == ["/", "//"]
    assert "02_two_sum_ii_input_array_is_sorted" in EXERCISE_RULES
    assert EXERCISE_RULES["02_two_sum_ii_input_array_is_sorted"].get("banned_calls") == [
        "dict",
        "defaultdict",
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_exercise_cleanliness.py -v`
Expected: FAIL with "Spoiler hints found in ..."

- [ ] **Step 3: Define `EXERCISE_RULES` in `src/neetlings/manifest.py`**

```python
# Per-exercise complexity rules and banned syntax mappings.
EXERCISE_RULES: dict[str, dict[str, list[str]]] = {
    "06_product_of_array_except_self": {"banned_ops": ["/", "//"]},
    "02_two_sum_ii_input_array_is_sorted": {"banned_calls": ["dict", "defaultdict"]},
}
```

- [ ] **Step 4: Strip `HINTS = [...]` from all 30 exercise files**

Run a script or rewrite files to remove `HINTS = [\n    ...\n]\n\n` from all 30 `exercises/**/*.py` files while leaving docstring, `class Solution:`, `TEST_CASES = [...]`, and `test_solution()`.

- [ ] **Step 5: Run tests and quality checks**

Run: `uv run pytest tests/test_exercise_cleanliness.py -v && uv run ruff check src tests exercises solutions && uv run pyright src`
Expected: PASS with 0 errors.

- [ ] **Step 6: Commit**

```bash
git add src/neetlings/manifest.py exercises/ tests/test_exercise_cleanliness.py
git commit --no-gpg-sign -m "chore: strip spoiler hints from all exercise starter files"
```

---

### Task 2: Fix Test Runner Engine to Execute Test Cases & Flag Failures

- **Depends on:** Task 1

**Files:**
- Modify: `src/neetlings/test_runner.py:60-220`
- Modify: `tests/test_test_runner.py:25-87`

**Interfaces:**
- Consumes: `code_str: str`, optional `test_cases`, `method_name`, `banned_calls`, `banned_ops`, `canonical_code: str | None`.
- Produces: `evaluate_code(...) -> dict[str, Any]` which strictly resolves test cases from `canonical_code` or `scope["TEST_CASES"]`, flags `NotImplementedError` as `FAILED`, and requires `len(test_cases) > 0` to return `PASSED`.

- [ ] **Step 1: Write failing tests in `tests/test_test_runner.py`**

Add tests:
```python
def test_evaluate_failing_code_not_implemented() -> None:
    """Verify that code raising NotImplementedError returns FAILED status, not PASSED."""
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        raise NotImplementedError
"""
    canonical_code = """
TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "example1"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "example2"},
]
"""
    res = evaluate_code(code, test_cases=None, method_name="containsDuplicate", canonical_code=canonical_code)
    assert res["status"] == "FAILED"
    assert res["passedCount"] == 0
    assert res["totalCount"] == 2
    assert len(res["cases"]) == 1
    assert res["cases"][0]["status"] == "FAILED"
    assert "NotImplementedError" in (res["cases"][0].get("error") or "")


def test_evaluate_empty_test_cases_returns_error() -> None:
    """Verify that when no test cases exist anywhere, status is ERROR, never PASSED."""
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return False
"""
    res = evaluate_code(code, test_cases=[], method_name="containsDuplicate")
    assert res["status"] == "ERROR"
    assert res["passedCount"] == 0
    assert "No test cases found" in (res["error"] or "")


def test_evaluate_extracts_canonical_code_test_cases() -> None:
    """Verify that evaluate_code automatically extracts test cases from canonical_code."""
    code = """
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))
"""
    canonical_code = """
TEST_CASES = [
    {"input": ([1, 2, 3, 1],), "expected": True, "name": "example1"},
    {"input": ([1, 2, 3, 4],), "expected": False, "name": "example2"},
]
"""
    res = evaluate_code(code, test_cases=None, method_name="containsDuplicate", canonical_code=canonical_code)
    assert res["status"] == "PASSED"
    assert res["passedCount"] == 2
    assert res["totalCount"] == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_test_runner.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement updated `evaluate_code` in `src/neetlings/test_runner.py`**

Update `evaluate_code`:
```python
def evaluate_code(
    code_str: str,
    test_cases: list[dict[str, Any]] | None = None,
    method_name: str = "solution",
    banned_calls: list[str] | None = None,
    banned_ops: list[str] | None = None,
    canonical_code: str | None = None,
) -> dict[str, Any]:
    # 1. AST syntax checks
    ...
    # 2. Redirect stdout
    ...
    try:
        # 3. Exec code_str in user scope
        scope: dict[str, Any] = {
            "ListNode": ListNode,
            "TreeNode": TreeNode,
            "Interval": Interval,
        }
        ...
        # 4. Resolve test cases if not provided or empty
        resolved_cases = list(test_cases) if test_cases else []
        if not resolved_cases and canonical_code:
            canonical_scope: dict[str, Any] = {
                "ListNode": ListNode,
                "TreeNode": TreeNode,
                "Interval": Interval,
            }
            try:
                exec(canonical_code, canonical_scope)
                if "TEST_CASES" in canonical_scope and isinstance(canonical_scope["TEST_CASES"], list):
                    resolved_cases = canonical_scope["TEST_CASES"]
            except Exception:
                pass

        if not resolved_cases and "TEST_CASES" in scope and isinstance(scope["TEST_CASES"], list):
            resolved_cases = scope["TEST_CASES"]

        if not resolved_cases:
            return {
                "status": "ERROR",
                "passedCount": 0,
                "totalCount": 0,
                "durationMs": 0.0,
                "stdout": stdout_buf.getvalue(),
                "error": "Error: No test cases found to evaluate code.",
                "cases": [],
                "diagnosticDiff": None,
            }

        # 5. Evaluate each test case
        cases_result: list[dict[str, Any]] = []
        all_passed = True
        diagnostic_diff: str | None = None

        for case in resolved_cases:
            c_name = case.get("name", "case")
            args = case["input"]
            expected = case["expected"]

            case_start = time.perf_counter()
            try:
                actual = run_with_timeout(fn, args, timeout=2.0)
                case_duration = (time.perf_counter() - case_start) * 1000.0

                passed = are_equal(actual, expected)
                if not passed:
                    all_passed = False
                    if isinstance(expected, TreeNode) or isinstance(actual, TreeNode):
                        diagnostic_diff = format_tree_diff(
                            expected if isinstance(expected, TreeNode) else None,
                            actual if isinstance(actual, TreeNode) else None,
                        )
                    elif isinstance(expected, ListNode) or isinstance(actual, ListNode):
                        diagnostic_diff = format_list_diff(
                            expected if isinstance(expected, ListNode) else None,
                            actual if isinstance(actual, ListNode) else None,
                        )

                cases_result.append(
                    {
                        "name": c_name,
                        "status": "PASSED" if passed else "FAILED",
                        "durationMs": round(case_duration, 2),
                        "expected": str(expected),
                        "actual": str(actual),
                    }
                )
                if not passed:
                    break
            except Exception:
                all_passed = False
                cases_result.append(
                    {
                        "name": c_name,
                        "status": "FAILED",
                        "durationMs": 0.0,
                        "expected": str(expected),
                        "actual": None,
                        "error": traceback.format_exc(),
                    }
                )
                break

        total_duration = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "PASSED" if all_passed and len(resolved_cases) > 0 else "FAILED",
            "passedCount": sum(1 for c in cases_result if c.get("status") == "PASSED"),
            "totalCount": len(resolved_cases),
            "durationMs": round(total_duration, 2),
            "stdout": stdout_buf.getvalue(),
            "error": None,
            "cases": cases_result,
            "diagnosticDiff": diagnostic_diff,
        }
    finally:
        sys.stdout = old_stdout
```

- [ ] **Step 4: Run tests and quality checks**

Run: `uv run pytest tests/test_test_runner.py -v && uv run ruff check src tests && uv run pyright src`
Expected: PASS with 0 errors.

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/test_runner.py tests/test_test_runner.py
git commit --no-gpg-sign -m "fix(runner): execute canonical test cases and fail uncompleted solutions"
```

---

### Task 3: Decouple Hints and Embed Exercise Rules in Asset Bundler

- **Depends on:** Task 1, Task 2

**Files:**
- Modify: `src/neetlings/bundler.py:1-85`
- Modify: `tests/test_bundler.py:1-40`

**Interfaces:**
- Consumes: `solutions/`, `exercises/`, `manifest.EXERCISE_RULES`.
- Produces: `bundle["exercises"][ex_id]["hints"]: list[str]`, `bannedCalls`, `bannedOps`.
- Guarantee: `bundle["exercises"][ex_id]["code"]` does not contain `HINTS = [`.

- [ ] **Step 1: Write failing tests in `tests/test_bundler.py`**

Add tests:
```python
def test_bundle_contains_hints_and_rules() -> None:
    bundle = generate_bundle()
    exercises = bundle["exercises"]
    assert len(exercises) >= 30

    for ex_id, ex in exercises.items():
        assert "hints" in ex, f"Missing hints key for {ex_id}"
        assert isinstance(ex["hints"], list), f"Hints must be list for {ex_id}"
        assert len(ex["hints"]) >= 3, f"Expected at least 3 hints for {ex_id}, got {len(ex['hints'])}"
        assert "HINTS = [" not in ex["code"], f"Found raw HINTS block in ex.code for {ex_id}"

    # Verify rule injection
    two_sum_ii = exercises["02_two_sum_ii_input_array_is_sorted"]
    assert "dict" in two_sum_ii.get("bannedCalls", [])
    prod = exercises["06_product_of_array_except_self"]
    assert "/" in prod.get("bannedOps", [])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_bundler.py -v`
Expected: FAIL with missing hints or raw HINTS block.

- [ ] **Step 3: Update `src/neetlings/bundler.py`**

Add `extract_hints_from_source(source: str) -> list[str]` and update `generate_bundle`:
- Extract hints from `sol_file` (or fallback to `ex_file`).
- Strip `HINTS = [\n...\n]\n` from `code`.
- Add `"hints": hints`, `"bannedCalls": rules.get("banned_calls", [])`, `"bannedOps": rules.get("banned_ops", [])`.

- [ ] **Step 4: Run tests and quality checks**

Run: `uv run pytest tests/test_bundler.py -v && uv run ruff check src tests && uv run pyright src`
Expected: PASS with 0 errors.

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/bundler.py tests/test_bundler.py
git commit --no-gpg-sign -m "feat(bundler): extract hints from solutions and embed per-exercise rules into bundle"
```

---

### Task 4: Wire Web Client, Web Worker, and Rebuild Playground Bundle

- **Depends on:** Task 2, Task 3

**Files:**
- Modify: `docs/assets/playground/playground-worker.js:65-95`
- Modify: `docs/assets/playground/playground.js:425-515`
- Modify: `docs/assets/playground/playground-bundle.json`
- Modify: `tests/test_web_assets.py:40-58`

**Interfaces:**
- `playground.js`: sends `solutionCode`, `bannedCalls`, `bannedOps` to worker.
- `playground-worker.js`: passes `canonicalCode: msg.solutionCode`, `bannedOps: msg.bannedOps`, `bannedCalls: msg.bannedCalls` to `evaluate_code`.
- `playground-bundle.json`: recompiled with all 30 exercises having decoupled hints and rules.

- [ ] **Step 1: Update `playground-worker.js`**

In `playground-worker.js`, unpack `msg.solutionCode`, `msg.bannedOps`, and pass to `evaluate_code`:
```javascript
            const pyTestCases = (msg.testCases && msg.testCases.length > 0) ? pyodide.toPy(msg.testCases) : null;
            const pyBannedCalls = (msg.bannedCalls && msg.bannedCalls.length > 0) ? pyodide.toPy(msg.bannedCalls) : null;
            const pyBannedOps = (msg.bannedOps && msg.bannedOps.length > 0) ? pyodide.toPy(msg.bannedOps) : null;
            const evaluate_code_fn = pyodide.globals.get("evaluate_code");

            const resultProxy = evaluate_code_fn(
                msg.code,
                pyTestCases,
                msg.methodName,
                pyBannedCalls,
                pyBannedOps,
                msg.solutionCode || null
            );
```

- [ ] **Step 2: Update `playground.js`**

In `playground.js`:
- `renderProblemPane()`:
```javascript
      // Render Hint Ladder from bundle hints or solution
      const hints = ex.hints && ex.hints.length > 0 ? ex.hints : this.extractHints(ex.solution || ex.code);
```
- `runCode()`:
```javascript
      this.worker.postMessage({
        type: "RUN",
        exerciseId: this.activeExerciseId,
        code: userCode,
        solutionCode: ex.solution || ex.code,
        methodName: methodName,
        bannedCalls: ex.bannedCalls || [],
        bannedOps: ex.bannedOps || [],
      });
```

- [ ] **Step 3: Rebuild playground bundle**

Run: `python scripts/build_playground_bundle.py`

- [ ] **Step 4: Update `tests/test_web_assets.py`**

Verify `bundle_json` contains `hints`, `bannedCalls`, `bannedOps`.

- [ ] **Step 5: Run full test suite and quality checks**

Run: `uv run pytest -v && uv run ruff check src tests exercises solutions scripts docs && uv run pyright src`
Expected: PASS (all 35+ tests pass, 0 lint errors, 0 pyright errors).

- [ ] **Step 6: Commit**

```bash
git add docs/assets/playground/ tests/test_web_assets.py
git commit --no-gpg-sign -m "fix(playground): wire canonical test execution, decoupled hints, and rebuild bundle"
```

