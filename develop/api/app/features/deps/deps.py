"""ネストした Depends を大量に組み立てる（dependency メモリ計測用）。"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from fastapi import Depends

CHAIN_DEPTH = 24
FANOUT_WIDTH = 8
ROUTE_COUNT = 40


def _with_depends_signature(
    name: str,
    param_deps: list[tuple[str, Callable[..., Any]]],
    body: Callable[..., Any],
) -> Callable[..., Any]:
    """各 Depends を個別パラメータとしてシグネチャに載せ、FastAPI に認識させる。"""
    parameters = [
        inspect.Parameter(
            param_name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=Depends(dep),
        )
        for param_name, dep in param_deps
    ]

    def wrapper(**kwargs: Any) -> Any:
        return body(**kwargs)

    wrapper.__name__ = name
    wrapper.__qualname__ = name
    wrapper.__signature__ = inspect.Signature(parameters)  # type: ignore[attr-defined]
    return wrapper


def _make_leaf(index: int) -> Callable[[], int]:
    def leaf() -> int:
        return index

    leaf.__name__ = f"leaf_{index}"
    leaf.__qualname__ = f"leaf_{index}"
    return leaf


def _make_fanout_node(
    level: int,
    index: int,
    child_deps: list[Callable[..., Any]],
) -> Callable[..., dict[str, Any]]:
    param_deps = [(f"c{i}", dep) for i, dep in enumerate(child_deps)]

    def body(**kwargs: Any) -> dict[str, Any]:
        values = list(kwargs.values())
        total = 0
        for value in values:
            total += value if isinstance(value, int) else int(value.get("sum", 0))
        return {
            "level": level,
            "index": index,
            "sum": total,
            "width": len(values),
        }

    return _with_depends_signature(f"fanout_L{level}_{index}", param_deps, body)


def _make_chain_node(
    level: int,
    prev: Callable[..., Any],
    side_deps: list[Callable[..., Any]],
) -> Callable[..., dict[str, Any]]:
    param_deps = [("previous", prev), *[ (f"s{i}", dep) for i, dep in enumerate(side_deps) ]]

    def body(**kwargs: Any) -> dict[str, Any]:
        previous = kwargs["previous"]
        sides = [kwargs[f"s{i}"] for i in range(len(side_deps))]
        side_sum = 0
        for side in sides:
            side_sum += side if isinstance(side, int) else int(side.get("sum", 0))
        prev_val = previous if isinstance(previous, int) else int(previous.get("tip", 0))
        return {
            "level": level,
            "tip": prev_val + side_sum + level,
            "side_count": len(sides),
        }

    return _with_depends_signature(f"chain_L{level}", param_deps, body)


def build_dependency_graph() -> tuple[Callable[..., dict[str, Any]], dict[str, int]]:
    leaves = [_make_leaf(i) for i in range(FANOUT_WIDTH)]

    current_layer: list[Callable[..., Any]] = list(leaves)
    for level in range(1, 4):
        next_layer: list[Callable[..., Any]] = []
        for i in range(FANOUT_WIDTH):
            children = [
                current_layer[(i + offset) % len(current_layer)]
                for offset in range(min(3, len(current_layer)))
            ]
            next_layer.append(_make_fanout_node(level, i, children))
        current_layer = next_layer

    chain: Callable[..., Any] = current_layer[0]
    for level in range(4, CHAIN_DEPTH):
        sides = [
            current_layer[j % len(current_layer)]
            for j in range(min(FANOUT_WIDTH, len(current_layer)))
        ]
        chain = _make_chain_node(level, chain, sides)

    meta = {
        "depth": CHAIN_DEPTH,
        "width": FANOUT_WIDTH,
        "route_count": ROUTE_COUNT,
    }
    return chain, meta


root_dependency, graph_meta = build_dependency_graph()
