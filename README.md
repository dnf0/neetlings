# ⚡ Neetlings

> **100% Client-Side WebAssembly Learning Platform for NeetCode 150**  
> Powered by Python 3.12, Pyodide v0.26, Monaco Editor, and Zero Backend Infrastructure.

Neetlings is a browser-first, interactive algorithm and data structure learning platform designed to master the **NeetCode 150** curriculum. Built with a pure client-side WebAssembly architecture, Neetlings executes your Python code directly in a browser Web Worker with sub-20ms latency, zero backend requirements, and complete privacy.

---

## 🌟 Key Features

- **⚡ 100% Client-Side WebAssembly**: Powered by Pyodide v0.26.2. Code execution, AST validation, and test assertions happen entirely within a sandboxed background Web Worker in your browser.
- **🖥️ 3-Pane Interactive IDE**: Split-screen responsive layout featuring the problem statement, Monaco Code Editor with Python 3.12 syntax highlighting, and an instant test runner console.
- **💡 4-Tier Progressive Hint Ladder**: Get unstuck without spoiling the answer:
  - **Tier 1**: Intuition & Core Observation
  - **Tier 2**: Algorithmic Pattern / Technique
  - **Tier 3**: Critical Edge Cases & Invariants
  - **Tier 4**: Code Skeleton / Step-by-Step Blueprint
- **🔍 ASCII Data Structure Visualizers**: When binary tree or linked list tests fail, Neetlings generates side-by-side ASCII diagrams illustrating exactly where your output deviates from the expected structure.
- **🛡️ AST Complexity Guardrails**: Static AST inspection flags disallowed shortcuts (e.g., calling `nums.sort()` on an $O(n)$ problem) and counts execution steps to guard against accidental infinite loops.
- **⚖️ Side-by-Side Monaco Solution Diff**: Compare your implementation directly with canonical reference solutions using Monaco's native visual diff view.
- **💾 Offline-First Local Persistence**: Progress, active code, and revealed hints automatically persist to `localStorage` with full JSON backup export and import.
- **🌓 Dark & Light Modes**: Seamless theme switching with synchronized Monaco editor themes (`vs-dark` and `vs`).

---

## 📚 Curriculum Structure (18 Categories / 150 Problems)

1. **Arrays & Hashing** (Hash maps, frequency counters, prefix sums)
2. **Two Pointers** (Converging indices, sorted search)
3. **Sliding Window** (Dynamic & fixed windows, subarrays)
4. **Stack** (Monotonic stacks, parentheses validation)
5. **Binary Search** (Search space division, rotated arrays)
6. **Linked List** (Fast/slow pointers, reversals, cycle detection)
7. **Trees** (DFS, BFS, BST invariants, path algorithms)
8. **Tries** (Prefix trees, word dictionaries)
9. **Heap / Priority Queue** (Min/Max heaps, top-K frequent elements)
10. **Backtracking** (Decision trees, state exploration, pruning)
11. **Graphs** (BFS, DFS, cycle detection, topological sort)
12. **Advanced Graphs** (Dijkstra, Prim, Kruskal, Bellman-Ford)
13. **1-D Dynamic Programming** (Subproblems, memoization, tabulation)
14. **2-D Dynamic Programming** (Grid paths, knapsack, LCS)
15. **Greedy** (Interval scheduling, local optimal choices)
16. **Intervals** (Merging, insertion, non-overlapping intervals)
17. **Math & Geometry** (Matrix rotations, spiral traversals)
18. **Bit Manipulation** (Bitwise arithmetic, XOR properties)

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python `>=3.12`
- [`uv`](https://github.com/astral-sh/uv) (recommended)

### 1. Clone & Setup

```bash
git clone https://github.com/dnf0/neetlings.git
cd neetlings
uv venv
source .venv/bin/activate
```

### 2. Run Test Suite & Quality Checks

Neetlings enforces strict typing and linting across all exercises and platform code:

```bash
# Run pytest test suite
uv run pytest -v

# Run Ruff linter & formatter check
uv run ruff check src tests exercises solutions scripts

# Run Pyright static type checker
uv run pyright src
```

### 3. Build Web Playground Asset Bundle

Compile all exercises, reference solutions, hints, and runtime modules into the static JSON bundle:

```bash
uv run python scripts/build_playground_bundle.py
```

### 4. Launch Local Web Server

Start any static web server pointing to `docs/`:

```bash
python -m http.server 8000 -d docs
```

Navigate to [http://localhost:8000/playground/](http://localhost:8000/playground/) to launch the IDE.

---

## 🏗️ Architecture & Pipeline

```
  ┌───────────────────────────────────────────────┐
  │       Neetlings Build Pipeline (Python)       │
  │                                               │
  │  exercises/ (18 Categories)                   │
  │  solutions/ (Optimal implementations)         │
  │  src/neetlings/ (models, visualizers, etc.)   │
  │                     │                         │
  │                     ▼                         │
  │   scripts/build_playground_bundle.py          │
  │                     │                         │
  │                     ▼                         │
  │   docs/assets/playground/                     │
  │     playground-bundle.json                    │
  └─────────────────────┬─────────────────────────┘
                        │
                        ▼
  ┌───────────────────────────────────────────────┐
  │           Client Browser (WebAssembly)        │
  │                                               │
  │  docs/playground/index.html (3-Pane UI)       │
  │  docs/assets/playground/playground.js         │
  │                     │                         │
  │          postMessage(RUN, code)               │
  │                     │                         │
  │                     ▼                         │
  │  docs/assets/playground/playground-worker.js  │
  │     ├─ Pyodide v0.26.2 WebAssembly            │
  │     ├─ /lib/neetlings/ (In-Memory FS)         │
  │     └─ evaluate_code() Test Engine            │
  └───────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions of new exercises, improved hints, or optimized reference solutions are warmly welcomed! Please ensure:

1. New exercise files follow the canonical schema with problem docstrings, `HINTS`, `class Solution`, `TEST_CASES`, and `test_solution()`.
2. Solutions pass 100% of test cases (`uv run pytest tests/test_reference_solutions.py`).
3. Linters and type checkers pass cleanly (`uv run ruff check` and `uv run pyright src`).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
