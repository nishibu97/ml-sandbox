from pydantic import BaseModel


class DepsBenchResponse(BaseModel):
    depth: int
    width: int
    route_count: int
    leaf_sum: int
    chain_tip: int
