from typing import Any

from fastapi import APIRouter, Depends

from app.features.deps.deps import ROUTE_COUNT, graph_meta, root_dependency
from app.features.deps.schemas import DepsBenchResponse

router = APIRouter(tags=["deps"])


def _to_response(root: dict[str, Any]) -> DepsBenchResponse:
    tip = int(root.get("tip", 0))
    return DepsBenchResponse(
        depth=graph_meta["depth"],
        width=graph_meta["width"],
        route_count=graph_meta["route_count"],
        leaf_sum=int(root.get("sum", tip)),
        chain_tip=tip,
    )


@router.get("/deps", response_model=DepsBenchResponse)
def read_deps(root: dict[str, Any] = Depends(root_dependency)) -> DepsBenchResponse:
    """ネストした Depends グラフを解決して返す（メイン計測用）。"""
    return _to_response(root)


def _register_mirror_routes() -> None:
    """同一グラフを参照するルートを増やし、アプリ構築時の Dependant 数を膨らませる。"""

    for index in range(ROUTE_COUNT):

        def make_endpoint(route_index: int) -> Any:
            def mirror(
                root: dict[str, Any] = Depends(root_dependency),
            ) -> DepsBenchResponse:
                return _to_response(root)

            mirror.__name__ = f"read_deps_mirror_{route_index}"
            mirror.__qualname__ = f"read_deps_mirror_{route_index}"
            return mirror

        router.add_api_route(
            f"/deps/r{index}",
            make_endpoint(index),
            methods=["GET"],
            response_model=DepsBenchResponse,
            include_in_schema=False,
            name=f"read_deps_mirror_{index}",
        )


_register_mirror_routes()
