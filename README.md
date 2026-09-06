# Neetlings

100% client-side WebAssembly learning platform for NeetCode 150.

## Overview

Neetlings is a lightweight, zero-Node, browser-first interactive learning platform for the NeetCode 150 curriculum. It leverages WebAssembly via Pyodide v0.26 to execute Python code entirely client-side, featuring AST complexity analysis, step counting guardrails, and rich diagnostic visualizers.

## Tech Stack

- **Core**: Python 3.12, Pyodide v0.26.2
- **Editor**: Monaco Editor
- **Tooling**: `uv`, `ruff`, `pyright`, `pytest`

## Getting Started

### Prerequisites

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

### Run Tests and Linters

```bash
uv run pytest -q && uv run ruff check src tests
```
