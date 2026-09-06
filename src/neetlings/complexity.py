"""Static AST checking and execution step counting for algorithmic guardrails."""

from __future__ import annotations

import ast
from typing import Any


class BannedSyntaxVisitor(ast.NodeVisitor):
    """AST Visitor to scan the code for any banned calls or attributes."""

    def __init__(self, banned_calls: list[str]) -> None:
        self.banned_calls = set(banned_calls)
        self.violations: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Visit call nodes to find if a disallowed function or attribute is called."""
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
        """Increment the step counter and raise StepLimitExceeded if the limit is breached."""
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
