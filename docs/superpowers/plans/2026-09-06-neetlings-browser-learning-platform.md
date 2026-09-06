# Neetlings WebAssembly Browser Learning Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Choose an execution mode:
> 1. `superpowers:subagent-driven-development` (recommended for multi-agent reviews, backed by `SKILL.state` / `.agent-state/state.json`)
> 2. `agent-rules:stateful-execution` (SKILL.state) (recommended for deterministic single-agent linear execution)
> 3. `superpowers:executing-plans` (batch execution with manual checkpoints)
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and test `neetlings`: a 100% client-side WebAssembly (Pyodide v0.26) learning platform for NeetCode 150 featuring Monaco Editor, AST complexity guardrails, and rich ASCII data structure visualizers hosted statically on GitHub Pages.

**Architecture:** A Python 3.12 package containing the curriculum, models, visualizers, complexity analyzers, and test runner. An automated bundler compiles exercises, solutions, and virtual library code into `docs/assets/playground/playground-bundle.json`. The web frontend is a zero-Node.js standalone SPA (`docs/playground/index.html`, `playground.js`, `playground.css`) communicating with a Pyodide background Web Worker (`playground-worker.js`).

**Tech Stack:** Python 3.12, Pyodide v0.26.2, Monaco Editor AMD Loader, vanilla HTML5/CSS3/ES6, uv, ruff, pyright, pytest.

## Global Constraints
- Target platform is 100% client-side Pyodide WebAssembly in the browser; no backend servers or database required.
- Python code style must strictly adhere to Python 3.12 with type annotations, verified by `ruff` and `pyright`.
- Zero-Node tooling: the web application requires no `npm` or `node` build step.
- All commits must skip GPG signing (`git commit --no-gpg-sign -m "..."`).
- Work must happen on feature branch `feat/neetlings-browser-platform` and isolated git worktrees.

---

### Task 1: Project Scaffolding & Tooling Configuration

- **Depends on:** none

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `src/neetlings/__init__.py`
- Create: `tests/__init__.py`

**Interfaces:**
- Consumes: none
- Produces: `neetlings.__version__` string and local `uv` execution environment.

- [ ] **Step 1: Create `.gitignore`**

```gitignore
__pycache__/
*.py[cod]
*$py.class
.venv/
.pytest_cache/
.ruff_cache/
.mypy_cache/
dist/
build/
*.egg-info/
.DS_Store
docs/assets/playground/playground-bundle.json
```

- [ ] **Step 2: Create `pyproject.toml`**

```toml
[project]
name = "neetlings"
version = "0.1.0"
description = "100% client-side WebAssembly learning platform for NeetCode 150"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "W", "UP"]

[tool.pyright]
include = ["src", "tests"]
pythonVersion = "3.12"
typeCheckingMode = "basic"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

- [ ] **Step 3: Create `src/neetlings/__init__.py`**

```python
"""Neetlings: 100% Client-Side WebAssembly Learning Platform for NeetCode 150."""

__version__ = "0.1.0"

__all__ = ["__version__"]
```

- [ ] **Step 4: Create `tests/__init__.py` and smoke test**

```python
"""Tests for neetlings package."""

from neetlings import __version__


def test_package_version() -> None:
    assert __version__ == "0.1.0"
```

- [ ] **Step 5: Run tests and linters**

Run: `uv run pytest -q && uv run ruff check src tests`
Expected: `1 passed` and clean linting.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore src/neetlings/__init__.py tests/__init__.py
git commit --no-gpg-sign -m "chore: scaffold project configuration and quality baseline"
```

---

### Task 2: Data Models & Converters (`src/neetlings/models.py`)

- **Depends on:** Task 1

**Files:**
- Create: `src/neetlings/models.py`
- Create: `tests/test_models.py`

**Interfaces:**
- Consumes: none
- Produces: `ListNode`, `TreeNode`, `GraphNode`, `Interval` classes with conversion utilities.

- [ ] **Step 1: Write the failing tests in `tests/test_models.py`**

```python
"""Tests for Neetlings data structure models."""

from neetlings.models import ListNode, TreeNode, Interval


def test_list_node_roundtrip() -> None:
    head = ListNode.from_list([1, 2, 3])
    assert head is not None
    assert head.to_list() == [1, 2, 3]
    assert head.to_ascii() == "1 ➔ 2 ➔ 3 ➔ None"


def test_list_node_empty() -> None:
    assert ListNode.from_list([]) is None


def test_tree_node_roundtrip() -> None:
    root = TreeNode.from_level_order([4, 2, 7, 1, 3, 6, 9])
    assert root is not None
    assert root.val == 4
    assert root.left.val == 2
    assert root.right.val == 7
    assert root.to_level_order() == [4, 2, 7, 1, 3, 6, 9]


def test_interval_model() -> None:
    inv = Interval(start=1, end=3)
    assert inv.to_list() == [1, 3]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_models.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'neetlings.models'`.

- [ ] **Step 3: Implement `src/neetlings/models.py`**

```python
"""Data structure representations and serializations for DSA problems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ListNode:
    """Singly-linked list node."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, vals: list[int]) -> ListNode | None:
        if not vals:
            return None
        dummy = cls(0)
        curr = dummy
        for v in vals:
            curr.next = cls(v)
            curr = curr.next
        return dummy.next

    def to_list(self) -> list[int]:
        result: list[int] = []
        curr: ListNode | None = self
        seen: set[int] = set()
        while curr is not None:
            if id(curr) in seen:
                result.append(curr.val)
                break
            seen.add(id(curr))
            result.append(curr.val)
            curr = curr.next
        return result

    def to_ascii(self) -> str:
        vals = self.to_list()
        return " ➔ ".join(str(v) for v in vals) + " ➔ None"

    def __repr__(self) -> str:
        return f"ListNode({self.to_list()})"


class TreeNode:
    """Binary tree node."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_level_order(cls, vals: list[int | None]) -> TreeNode | None:
        if not vals or vals[0] is None:
            return None
        root = cls(vals[0])
        queue: list[TreeNode] = [root]
        idx = 1
        n = len(vals)
        while queue and idx < n:
            curr = queue.pop(0)
            if idx < n and vals[idx] is not None:
                curr.left = cls(vals[idx])  # type: ignore[arg-type]
                queue.append(curr.left)
            idx += 1
            if idx < n and vals[idx] is not None:
                curr.right = cls(vals[idx])  # type: ignore[arg-type]
                queue.append(curr.right)
            idx += 1
        return root

    def to_level_order(self) -> list[int | None]:
        result: list[int | None] = []
        queue: list[TreeNode | None] = [self]
        while queue:
            curr = queue.pop(0)
            if curr is not None:
                result.append(curr.val)
                queue.append(curr.left)
                queue.append(curr.right)
            else:
                result.append(None)
        while result and result[-1] is None:
            result.pop()
        return result

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class GraphNode:
    """Node for graph algorithms."""

    def __init__(self, val: int = 0, neighbors: list[GraphNode] | None = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


@dataclass
class Interval:
    """Interval definition with start and end points."""

    start: int
    end: int

    def to_list(self) -> list[int]:
        return [self.start, self.end]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_models.py`
Expected: PASS (`3 passed`).

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/models.py tests/test_models.py
git commit --no-gpg-sign -m "feat: implement ListNode, TreeNode, GraphNode, and Interval models"
```

---

### Task 3: Diagnostic Visualizers (`src/neetlings/visualizers.py`)

- **Depends on:** Task 2

**Files:**
- Create: `src/neetlings/visualizers.py`
- Create: `tests/test_visualizers.py`

**Interfaces:**
- Consumes: `ListNode`, `TreeNode` from `src/neetlings/models.py`
- Produces: `render_ascii_tree`, `format_tree_diff`, `format_list_diff`, `format_grid`

- [ ] **Step 1: Write the failing tests in `tests/test_visualizers.py`**

```python
"""Tests for ASCII diagnostic visualizers."""

from neetlings.models import ListNode, TreeNode
from neetlings.visualizers import format_list_diff, format_tree_diff, render_ascii_tree


def test_render_ascii_tree() -> None:
    root = TreeNode.from_level_order([4, 2, 7, 1, 3])
    diagram = render_ascii_tree(root)
    assert "4" in diagram
    assert "2" in diagram
    assert "7" in diagram


def test_format_tree_diff() -> None:
    expected = TreeNode.from_level_order([4, 7, 2])
    actual = TreeNode.from_level_order([4, 2, 7])
    diff = format_tree_diff(expected, actual)
    assert "Expected Tree:" in diff
    assert "Actual Tree:" in diff


def test_format_list_diff() -> None:
    exp = ListNode.from_list([1, 2, 3])
    act = ListNode.from_list([1, 3, 2])
    diff = format_list_diff(exp, act)
    assert "Expected List:" in diff
    assert "Actual List:" in diff
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_visualizers.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'neetlings.visualizers'`.

- [ ] **Step 3: Implement `src/neetlings/visualizers.py`**

```python
"""Visualizers for data structure differences and formatted ASCII trees."""

from __future__ import annotations

from typing import Any
from neetlings.models import ListNode, TreeNode


def render_ascii_tree(root: TreeNode | None, prefix: str = "", is_left: bool = True) -> str:
    """Render a binary tree into a clean multi-line ASCII diagram."""
    if root is None:
        return ""
    lines: list[str] = []
    if root.right is not None:
        lines.append(render_ascii_tree(root.right, prefix + ("│   " if is_left else "    "), False))
    lines.append(prefix + ("└── " if is_left else "┌── ") + str(root.val))
    if root.left is not None:
        lines.append(render_ascii_tree(root.left, prefix + ("    " if is_left else "│   "), True))
    return "\n".join(line for line in lines if line)


def format_tree_diff(expected: TreeNode | None, actual: TreeNode | None) -> str:
    """Render side-by-side or stacked tree diagrams comparing expected and actual trees."""
    exp_tree = render_ascii_tree(expected) or "(Empty Tree)"
    act_tree = render_ascii_tree(actual) or "(Empty Tree)"
    return (
        "--- Expected Tree ---\n"
        f"{exp_tree}\n\n"
        "--- Actual Tree ---\n"
        f"{act_tree}\n"
    )


def format_list_diff(expected: ListNode | None, actual: ListNode | None) -> str:
    """Render linked list comparison."""
    exp_str = expected.to_ascii() if expected else "None"
    act_str = actual.to_ascii() if actual else "None"
    return (
        f"Expected List: {exp_str}\n"
        f"Actual List:   {act_str}\n"
    )


def format_grid(grid: list[list[Any]]) -> str:
    """Render 2D matrix with coordinate row/column headers."""
    if not grid or not grid[0]:
        return "[]"
    header = "     " + " ".join(f"{c:3}" for c in range(len(grid[0])))
    sep = "    +" + "---" * len(grid[0])
    rows: list[str] = [header, sep]
    for r, row in enumerate(grid):
        row_str = " ".join(f"{str(v):3}" for v in row)
        rows.append(f"{r:2} | {row_str}")
    return "\n".join(rows)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_visualizers.py`
Expected: PASS (`3 passed`).

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/visualizers.py tests/test_visualizers.py
git commit --no-gpg-sign -m "feat: implement ASCII tree, list, and matrix diff visualizers"
```

---

### Task 4: AST Complexity Analyzer & Runtime Step Counter (`src/neetlings/complexity.py`)

- **Depends on:** Task 1

**Files:**
- Create: `src/neetlings/complexity.py`
- Create: `tests/test_complexity.py`

**Interfaces:**
- Consumes: Python `ast` module
- Produces: `check_banned_syntax(code, banned_calls)` and `StepCounter` context manager.

- [ ] **Step 1: Write the failing tests in `tests/test_complexity.py`**

```python
"""Tests for AST complexity and banned syntax verification."""

from neetlings.complexity import StepCounter, check_banned_syntax


def test_check_banned_syntax_finds_sort() -> None:
    user_code = """
def sort_colors(nums):
    nums.sort()
"""
    violations = check_banned_syntax(user_code, banned_calls=["sort"])
    assert len(violations) == 1
    assert "Disallowed call: sort" in violations[0]


def test_check_banned_syntax_clean() -> None:
    user_code = """
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen: return True
        seen.add(x)
    return False
"""
    assert check_banned_syntax(user_code, banned_calls=["sort"]) == []


def test_step_counter() -> None:
    counter = StepCounter(max_steps=100)
    with counter:
        for _ in range(10):
            counter.step()
    assert counter.total_steps == 10
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_complexity.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'neetlings.complexity'`.

- [ ] **Step 3: Implement `src/neetlings/complexity.py`**

```python
"""Static AST checking and execution step counting for algorithmic guardrails."""

from __future__ import annotations

import ast


class BannedSyntaxVisitor(ast.NodeVisitor):
    def __init__(self, banned_calls: list[str]) -> None:
        self.banned_calls = set(banned_calls)
        self.violations: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in self.banned_calls:
            self.violations.append(
                f"Disallowed call: {func_name} at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)


def check_banned_syntax(code: str, banned_calls: list[str] | None = None) -> list[str]:
    """Parse code with ast and detect any disallowed builtin or method calls."""
    if not banned_calls:
        return []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"Syntax error during AST check: {e}"]
    visitor = BannedSyntaxVisitor(banned_calls)
    visitor.visit(tree)
    return visitor.violations


class StepLimitExceeded(Exception):
    """Raised when an algorithm exceeds the maximum allowed computational steps."""


class StepCounter:
    """Monitors loop and recursion steps to prevent infinite execution and flag O(n^2)."""

    def __init__(self, max_steps: int = 1_000_000) -> None:
        self.max_steps = max_steps
        self.total_steps = 0

    def step(self, amount: int = 1) -> None:
        self.total_steps += amount
        if self.total_steps > self.max_steps:
            raise StepLimitExceeded(
                f"Execution aborted: exceeded maximum step threshold ({self.max_steps})"
            )

    def __enter__(self) -> StepCounter:
        self.total_steps = 0
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_complexity.py`
Expected: PASS (`3 passed`).

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/complexity.py tests/test_complexity.py
git commit --no-gpg-sign -m "feat: implement AST syntax checker and runtime step counter"
```

---

### Task 5: In-Memory Test Runner (`src/neetlings/test_runner.py`)

- **Depends on:** Tasks 2, 3, 4

**Files:**
- Create: `src/neetlings/test_runner.py`
- Create: `tests/test_test_runner.py`

**Interfaces:**
- Consumes: `models`, `visualizers`, `complexity`
- Produces: `evaluate_code(code_str, test_cases, banned_calls, function_name)` returning structured result dict.

- [ ] **Step 1: Write the failing tests in `tests/test_test_runner.py`**

```python
"""Tests for in-memory test runner."""

from neetlings.test_runner import evaluate_code


def test_evaluate_passing_code() -> None:
    code = """
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        lookup = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in lookup:
                return [lookup[diff], i]
            lookup[n] = i
        return []
"""
    test_cases = [
        {"input": ([2, 7, 11, 15], 9), "expected": [0, 1], "name": "basic"},
        {"input": ([3, 2, 4], 6), "expected": [1, 2], "name": "unsorted"},
    ]
    res = evaluate_code(code, test_cases, method_name="two_sum")
    assert res["status"] == "PASSED"
    assert res["passedCount"] == 2
    assert res["totalCount"] == 2


def test_evaluate_failing_code() -> None:
    code = """
class Solution:
    def two_sum(self, nums, target):
        return []
"""
    test_cases = [{"input": ([2, 7, 11, 15], 9), "expected": [0, 1], "name": "basic"}]
    res = evaluate_code(code, test_cases, method_name="two_sum")
    assert res["status"] == "FAILED"
    assert res["passedCount"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_test_runner.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'neetlings.test_runner'`.

- [ ] **Step 3: Implement `src/neetlings/test_runner.py`**

```python
"""In-memory code evaluation engine for browser Pyodide and local execution."""

from __future__ import annotations

import io
import sys
import time
import traceback
from typing import Any

from neetlings.complexity import check_banned_syntax
from neetlings.models import ListNode, TreeNode
from neetlings.visualizers import format_list_diff, format_tree_diff


def evaluate_code(
    code_str: str,
    test_cases: list[dict[str, Any]],
    method_name: str,
    banned_calls: list[str] | None = None,
) -> dict[str, Any]:
    """Execute user-supplied Python code in an isolated scope against test cases."""
    # 1. Check for banned AST calls
    violations = check_banned_syntax(code_str, banned_calls)
    if violations:
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(test_cases),
            "durationMs": 0.0,
            "stdout": "",
            "error": "Security / Complexity Rule Violation:\n" + "\n".join(violations),
            "cases": [],
            "diagnosticDiff": None,
        }

    # 2. Redirect stdout
    stdout_buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buf

    # 3. Compile and execute definitions
    scope: dict[str, Any] = {
        "ListNode": ListNode,
        "TreeNode": TreeNode,
    }

    start_time = time.perf_counter()
    try:
        exec(code_str, scope)
    except Exception as e:
        sys.stdout = old_stdout
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(test_cases),
            "durationMs": 0.0,
            "stdout": stdout_buf.getvalue(),
            "error": f"Compilation/Import Error:\n{traceback.format_exc()}",
            "cases": [],
            "diagnosticDiff": None,
        }

    if "Solution" not in scope:
        sys.stdout = old_stdout
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(test_cases),
            "durationMs": 0.0,
            "stdout": stdout_buf.getvalue(),
            "error": "Error: class Solution was not defined.",
            "cases": [],
            "diagnosticDiff": None,
        }

    sol_instance = scope["Solution"]()
    if not hasattr(sol_instance, method_name):
        sys.stdout = old_stdout
        return {
            "status": "ERROR",
            "passedCount": 0,
            "totalCount": len(test_cases),
            "durationMs": 0.0,
            "stdout": stdout_buf.getvalue(),
            "error": f"Error: Solution has no method '{method_name}'.",
            "cases": [],
            "diagnosticDiff": None,
        }

    fn = getattr(sol_instance, method_name)

    # 4. Evaluate each test case
    cases_result: list[dict[str, Any]] = []
    all_passed = True
    diagnostic_diff: str | None = None

    for case in test_cases:
        c_name = case.get("name", "case")
        args = case["input"]
        expected = case["expected"]

        case_start = time.perf_counter()
        try:
            actual = fn(*args)
            case_duration = (time.perf_counter() - case_start) * 1000.0

            # Compare results
            passed = actual == expected
            if not passed:
                all_passed = False
                # Check if visualizer diff applies
                if isinstance(expected, TreeNode) and isinstance(actual, TreeNode):
                    diagnostic_diff = format_tree_diff(expected, actual)
                elif isinstance(expected, ListNode) and isinstance(actual, ListNode):
                    diagnostic_diff = format_list_diff(expected, actual)

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
        except Exception as e:
            all_passed = False
            cases_result.append(
                {
                    "name": c_name,
                    "status": "ERROR",
                    "durationMs": 0.0,
                    "error": traceback.format_exc(),
                }
            )
            break

    sys.stdout = old_stdout
    total_duration = (time.perf_counter() - start_time) * 1000.0

    return {
        "status": "PASSED" if all_passed else "FAILED",
        "passedCount": sum(1 for c in cases_result if c.get("status") == "PASSED"),
        "totalCount": len(test_cases),
        "durationMs": round(total_duration, 2),
        "stdout": stdout_buf.getvalue(),
        "error": None,
        "cases": cases_result,
        "diagnosticDiff": diagnostic_diff,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_test_runner.py`
Expected: PASS (`2 passed`).

- [ ] **Step 5: Commit**

```bash
git add src/neetlings/test_runner.py tests/test_test_runner.py
git commit --no-gpg-sign -m "feat: implement in-memory evaluation engine and test runner"
```

---

### Task 6: Manifest & Bundle Asset Generator (`src/neetlings/bundler.py`)

- **Depends on:** Tasks 1-5

**Files:**
- Create: `src/neetlings/manifest.py`
- Create: `src/neetlings/bundler.py`
- Create: `scripts/build_playground_bundle.py`
- Create: `tests/test_bundler.py`

**Interfaces:**
- Consumes: exercises directory, solutions directory, `src/neetlings/` runtime
- Produces: `docs/assets/playground/playground-bundle.json` with chapters, exercises, and virtual modules.

- [ ] **Step 1: Write failing test in `tests/test_bundler.py`**

```python
"""Tests for bundle generator."""

from neetlings.bundler import generate_bundle


def test_generate_bundle_structure() -> None:
    bundle = generate_bundle()
    assert "version" in bundle
    assert "chapters" in bundle
    assert "exercises" in bundle
    assert "runtime_modules" in bundle
    assert "models.py" in bundle["runtime_modules"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_bundler.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'neetlings.bundler'`.

- [ ] **Step 3: Implement `src/neetlings/manifest.py`**

```python
"""Curriculum manifest definitions for NeetCode 150 categories."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChapterInfo:
    number: int
    id: str
    title: str
    description: str


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
```

- [ ] **Step 4: Implement `src/neetlings/bundler.py`**

```python
"""Asset bundler compiling exercises, solutions, hints, and virtual runtime into JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neetlings import __version__
from neetlings.manifest import CATEGORIES


def generate_bundle(repo_root: Path | None = None) -> dict[str, Any]:
    if repo_root is None:
        repo_root = Path.cwd()

    src_dir = repo_root / "src" / "neetlings"
    runtime_modules: dict[str, str] = {}
    for filename in ["models.py", "visualizers.py", "complexity.py", "test_runner.py"]:
        path = src_dir / filename
        if path.exists():
            runtime_modules[filename] = path.read_text(encoding="utf-8")

    exercises_dir = repo_root / "exercises"
    solutions_dir = repo_root / "solutions"

    chapters: list[dict[str, Any]] = []
    exercises: dict[str, Any] = {}

    for cat in CATEGORIES:
        ch_dir_name = f"{cat.number:02d}_{cat.id}"
        ex_dir = exercises_dir / ch_dir_name
        ex_ids: list[str] = []

        if ex_dir.exists():
            for ex_file in sorted(ex_dir.glob("*.py")):
                ex_id = ex_file.stem
                ex_ids.append(ex_id)
                sol_file = solutions_dir / ch_dir_name / ex_file.name

                code = ex_file.read_text(encoding="utf-8")
                solution = sol_file.read_text(encoding="utf-8") if sol_file.exists() else ""

                # Extract title and hints from docstring/code
                title = ex_id.replace("_", " ").title()
                exercises[ex_id] = {
                    "id": ex_id,
                    "categoryId": cat.id,
                    "title": title,
                    "code": code,
                    "solution": solution,
                }

        chapters.append(
            {
                "number": cat.number,
                "id": cat.id,
                "title": cat.title,
                "description": cat.description,
                "exerciseIds": ex_ids,
            }
        )

    return {
        "version": __version__,
        "totalChapters": len(chapters),
        "totalExercises": len(exercises),
        "chapters": chapters,
        "exercises": exercises,
        "runtime_modules": runtime_modules,
    }


def export_bundle(dest_path: Path, repo_root: Path | None = None) -> Path:
    bundle = generate_bundle(repo_root)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    return dest_path
```

- [ ] **Step 5: Implement `scripts/build_playground_bundle.py`**

```python
#!/usr/bin/env python3
"""CLI script to build neetlings playground bundle."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from neetlings.bundler import export_bundle


def main() -> None:
    dest = Path("docs/assets/playground/playground-bundle.json")
    out = export_bundle(dest)
    print(f"✓ Built Neetlings WebAssembly Bundle at: {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run test to verify it passes**

Run: `uv run pytest tests/test_bundler.py`
Expected: PASS (`1 passed`).

- [ ] **Step 7: Commit**

```bash
git add src/neetlings/manifest.py src/neetlings/bundler.py scripts/build_playground_bundle.py tests/test_bundler.py
git commit --no-gpg-sign -m "feat: implement curriculum manifest and playground bundle generator"
```

---

### Task 7: Foundational Exercise Showcase (18 Categories)

- **Depends on:** Tasks 1-6

**Files:**
- Create: `exercises/01_arrays_and_hashing/01_contains_duplicate.py`
- Create: `solutions/01_arrays_and_hashing/01_contains_duplicate.py`
- Create: `exercises/02_two_pointers/01_valid_palindrome.py`
- Create: `solutions/02_two_pointers/01_valid_palindrome.py`
- Create: `exercises/07_trees/01_invert_binary_tree.py`
- Create: `solutions/07_trees/01_invert_binary_tree.py`
- Create: `tests/test_reference_solutions.py`

**Interfaces:**
- Consumes: `exercises/`, `solutions/`, `test_runner`
- Produces: Validated, runnable starter exercises and reference solutions.

- [ ] **Step 1: Write `01_contains_duplicate.py` in exercises and solutions**

Create starter `exercises/01_arrays_and_hashing/01_contains_duplicate.py` with `raise NotImplementedError` and `TEST_CASES`.
Create optimal solution `solutions/01_arrays_and_hashing/01_contains_duplicate.py` using hash set `seen`.

- [ ] **Step 2: Write `01_valid_palindrome.py` in exercises and solutions**

Create starter `exercises/02_two_pointers/01_valid_palindrome.py`.
Create optimal solution `solutions/02_two_pointers/01_valid_palindrome.py` using converging pointers `l` and `r`.

- [ ] **Step 3: Write `01_invert_binary_tree.py` in exercises and solutions**

Create starter `exercises/07_trees/01_invert_binary_tree.py`.
Create optimal solution `solutions/07_trees/01_invert_binary_tree.py` using recursion.

- [ ] **Step 4: Implement `tests/test_reference_solutions.py`**

```python
"""Verify that all written solutions pass 100% of test cases."""

from pathlib import Path
import importlib.util


def test_all_reference_solutions() -> None:
    solutions_dir = Path("solutions")
    for sol_file in solutions_dir.rglob("*.py"):
        spec = importlib.util.spec_from_file_location(sol_file.stem, sol_file)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "test_solution"), f"{sol_file} missing test_solution()"
        mod.test_solution()
```

- [ ] **Step 5: Run tests to verify solutions pass**

Run: `uv run pytest tests/test_reference_solutions.py`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add exercises/ solutions/ tests/test_reference_solutions.py
git commit --no-gpg-sign -m "feat: add initial exercises and reference solutions for Arrays, Pointers, and Trees"
```

---

### Task 8: Pyodide Web Worker Background Engine (`docs/assets/playground/playground-worker.js`)

- **Depends on:** Tasks 5, 6

**Files:**
- Create: `docs/assets/playground/playground-worker.js`
- Create: `tests/test_web_worker_contract.py`

**Interfaces:**
- Consumes: `playground-bundle.json`
- Produces: Web Worker responding to `INIT` and `RUN` messages.

- [ ] **Step 1: Write contract test in `tests/test_web_worker_contract.py`**

```python
"""Verify Web Worker file syntax and message contracts."""

from pathlib import Path


def test_worker_file_contains_pyodide_loading() -> None:
    worker_path = Path("docs/assets/playground/playground-worker.js")
    assert worker_path.exists()
    content = worker_path.read_text(encoding="utf-8")
    assert "importScripts" in content
    assert "pyodide" in content
    assert "evaluate_code" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_web_worker_contract.py`
Expected: FAIL (file does not exist yet).

- [ ] **Step 3: Implement `docs/assets/playground/playground-worker.js`**

Implement background Web Worker script:
- Imports Pyodide v0.26.2 CDN.
- Mounts `/lib/neetlings/` containing `models.py`, `visualizers.py`, `complexity.py`, and `test_runner.py`.
- On `RUN`, invokes `evaluate_code()` and returns results via `postMessage`.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_web_worker_contract.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/assets/playground/playground-worker.js tests/test_web_worker_contract.py
git commit --no-gpg-sign -m "feat: implement Pyodide v0.26 Web Worker background execution engine"
```

---

### Task 9: 3-Pane Interactive Web Application (`docs/playground/index.html`, `playground.js`, `playground.css`)

- **Depends on:** Tasks 6, 8

**Files:**
- Create: `docs/playground/index.html`
- Create: `docs/assets/playground/playground.css`
- Create: `docs/assets/playground/playground.js`

**Interfaces:**
- Consumes: `playground-worker.js`, `playground-bundle.json`, Monaco Editor AMD loader
- Produces: Standalone single-page web app with split-pane layout, hint ladder, diff viewer, and local persistence.

- [ ] **Step 1: Implement `docs/assets/playground/playground.css`**

Responsive 3-pane layout, dark/light theme variables, code block styling, hint accordion styles.

- [ ] **Step 2: Implement `docs/assets/playground/playground.js`**

App controller:
- Initializes Monaco Editor with Python language configuration.
- Loads `playground-bundle.json`.
- Manages `NeetlingsStorage` (auto-saving code to `localStorage`, tracking completed exercises).
- Bridges worker messages: dispatches code on `Ctrl+Enter` or Run button click.
- Renders test cases and visual ASCII diffs in diagnostics panel.
- Manages progressive hint ladder reveal and Monaco Diff comparison toggle.

- [ ] **Step 3: Implement `docs/playground/index.html`**

HTML5 shell with top navigation bar (logo, category/problem selector, solved badge, import/export, theme toggle) and 3-pane container.

- [ ] **Step 4: Generate the bundle for local testing**

Run: `uv run python scripts/build_playground_bundle.py`
Expected: `✓ Built Neetlings WebAssembly Bundle at: docs/assets/playground/playground-bundle.json`.

- [ ] **Step 5: Commit**

```bash
git add docs/playground/index.html docs/assets/playground/playground.css docs/assets/playground/playground.js
git commit --no-gpg-sign -m "feat: implement 3-pane Monaco WebAssembly learning playground"
```

---

### Task 10: End-to-End Verification & Documentation

- **Depends on:** Tasks 1-9

**Files:**
- Create: `README.md`
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: All components
- Produces: Production GitHub Pages deployment workflow and user documentation.

- [ ] **Step 1: Implement `README.md`**

Document platform overview, architecture, local development commands (`uv run ...`), and GitHub Pages hosting instructions.

- [ ] **Step 2: Implement `.github/workflows/deploy.yml`**

GitHub Actions workflow running `pytest`, `ruff`, generating `playground-bundle.json`, and publishing `docs/` to GitHub Pages.

- [ ] **Step 3: Full test suite verification**

Run: `uv run pytest -v && uv run ruff check src tests`
Expected: All tests pass, zero lint errors.

- [ ] **Step 4: Commit**

```bash
git add README.md .github/workflows/deploy.yml
git commit --no-gpg-sign -m "docs: add platform documentation and GitHub Pages CI/CD workflow"
```
