from typing import TypedDict


class TrackerSummaryDocument(TypedDict):
    cost_bnb: float
    cost_bnb_fiat: float
    cost_dar: float
    cost_dar_fiat: float
    revenue_dar: float
    revenue_dar_fiat: float
    profit_fiat: float