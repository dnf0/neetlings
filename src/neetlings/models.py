"""Data structure representations and serializations for DSA problems."""

from __future__ import annotations

from dataclasses import dataclass


class ListNode:
    """Singly-linked list node."""

    def __init__(self, val: int = 0, next_node: ListNode | None = None) -> None:
        self.val: int = val
        self.next: ListNode | None = next_node

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
        self.val: int = val
        self.left: TreeNode | None = left
        self.right: TreeNode | None = right

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
            if idx < n:
                val = vals[idx]
                if val is not None:
                    curr.left = cls(val)
                    queue.append(curr.left)
            idx += 1
            if idx < n:
                val = vals[idx]
                if val is not None:
                    curr.right = cls(val)
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
        self.val: int = val
        self.neighbors: list[GraphNode] = neighbors if neighbors is not None else []
        # Keep each neighbor back-referenced or forward-referenced safely


@dataclass
class Interval:
    """Interval definition with start and end points."""

    start: int
    end: int

    def to_list(self) -> list[int]:
        return [self.start, self.end]

