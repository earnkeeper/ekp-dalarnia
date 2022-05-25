from typing import Optional, TypedDict


class PlayerTransactionDocument(TypedDict):
    cost_bnb: Optional[float]
    cost_bnb_fiat: Optional[float]
    cost_dar: Optional[float]
    cost_dar_fiat: Optional[float]
    description: str
    fiat_symbol: str
    id: str
    revenue_dar: Optional[float]
    revenue_dar_fiat: Optional[float]
    timestamp: int
    transaction_hash: str
    updated: int