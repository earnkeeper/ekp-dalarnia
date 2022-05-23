from typing import Optional, TypedDict


from typing import TypedDict

class DalarniaTransactionModel(TypedDict):
    bnbCost: Optional[float]
    bnbCostUsd: Optional[float]
    darCost: Optional[float]
    darCostUsd: Optional[float]
    darRev: Optional[float]
    darRevUsd: Optional[float]
    blockNumber: int
    player_address: str
    description: str
    hash: str
    timestamp: int
    
