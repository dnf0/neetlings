"""Static AST checking and execution step counting for algorithmic guardrails."""

from __future__ import annotations

import ast
from typing import Any

# Mapping of Python AST binary operator types to their canonical string representations.
AST_BIN_OP_MAP: dict[type[ast.operator], str] = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    ast.MatMult: "@",
}


class BannedSyntaxVisitor(ast.NodeVisitor):
    """AST Visitor to scan the code for any banned calls, attributes, or operators."""

    def __init__(
        self,
        banned_calls: list[str] | None = None,
        banned_ops: list[str] | None = None,
    ) -> None:
        """Initialize the visitor with disallowed calls and operators.

        Args:
            banned_calls: Function or method names that are not permitted.
            banned_ops: Operator symbol representations (e.g., '/', '//') that are not permitted.
        """
        self.banned_calls = set(banned_calls) if banned_calls else set()
        self.banned_ops = set(banned_ops) if banned_ops else set()
        self.violations: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        """Visit call nodes to find if a disallowed function or attribute is called.

        Args:
            node: The AST Call node being inspected.
        """
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        # Check if the invoked function or method matches any disallowed identifier.
        if func_name in self.banned_calls:
            self.violations.append(
                f"Disallowed call: {func_name} at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Visit binary operations to detect disallowed operators.

        Args:
            node: The AST BinOp node being inspected.
        """
        op_symbol = AST_BIN_OP_MAP.get(type(node.op))
        # Guard clause: verify if the binary operator is explicitly prohibited.
        if op_symbol and op_symbol in self.banned_ops:
            self.violations.append(
                f"Disallowed operator: {op_symbol} at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Visit augmented assignment statements to detect disallowed operators.

        Args:
            node: The AST AugAssign node being inspected.
        """
        op_symbol = AST_BIN_OP_MAP.get(type(node.op))
        # Guard clause: verify if the augmented assignment operator is explicitly prohibited.
        if op_symbol and op_symbol in self.banned_ops:
            self.violations.append(
                f"Disallowed operator: {op_symbol} at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        """Visit dictionary literals to detect disallowed dictionary creation.

        Args:
            node: The AST Dict node being inspected.
        """
        # Guard clause: check if dict literals are prohibited via banned_calls.
        if "dict" in self.banned_calls:
            self.violations.append(
                f"Disallowed syntax: dict literal at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """Visit dictionary comprehensions to detect disallowed dictionary creation.

        Args:
            node: The AST DictComp node being inspected.
        """
        # Guard clause: check if dict comprehensions are prohibited via banned_calls.
        if "dict" in self.banned_calls:
            self.violations.append(
                f"Disallowed syntax: dict comprehension at line {node.lineno}, col {node.col_offset}"
            )
        self.generic_visit(node)


def check_banned_syntax(
    code: str,
    banned_calls: list[str] | None = None,
    banned_ops: list[str] | None = None,
) -> list[str]:
    """Parse code with ast and detect any disallowed builtin or method calls or operators.

    Args:
        code: The Python source code string to analyze.
        banned_calls: Optional list of function/method names to disallow.
        banned_ops: Optional list of operator representations to disallow (e.g. ['/', '//']).

    Returns:
        A list of human-readable violation descriptions if any disallowed syntax is encountered.
    """
    # Guard clause: skip AST parsing if neither banned calls nor banned operators are configured.
    if not banned_calls and not banned_ops:
        return []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"Syntax error during AST check: {e}"]
    visitor = BannedSyntaxVisitor(banned_calls=banned_calls, banned_ops=banned_ops)
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
