from datetime import datetime

from db.dalarnia_transactions_repo import MarketTransactionsRepo
from ekp_sdk.services import CoingeckoService


class PlayersSummaryService:
    def __init__(
            self,
            market_transactions_repo: MarketTransactionsRepo,
            coingecko_service: CoingeckoService
    ):
        self.market_transactions_repo = market_transactions_repo
        self.coingecko_service = coingecko_service

    def aggregate_sum(self, variable_to_sum):
        total = list(
            self.market_transactions_repo.collection.aggregate(
                [{
                    "$group":
                        {"_id": None,
                         "total": {"$sum": f"${variable_to_sum}"}
                         }}
                ])
        )[0]
        return total["total"]

    async def get_documents(self, currency):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        total_bnb_cost = self.aggregate_sum('bnbCostUsd') * rate
        total_dar_cost = self.aggregate_sum('darCostUsd') * rate
        total_dar_revenue = self.aggregate_sum('darRevUsd') * rate
        profit_to_date = total_bnb_cost + total_dar_cost - total_dar_revenue

        return [
            {
                "id": "0",
                "updated": datetime.now().timestamp(),
                "total_bnb_cost": {
                    "name": "BNB Cost",
                    "total_price": total_bnb_cost,
                    "fiatSymbol": currency["symbol"]
                },
                "total_dar_cost": {
                    "name": "DAR Cost",
                    "total_price": total_dar_cost,
                    "fiatSymbol": currency["symbol"]
                },
                "total_dar_revenue": {
                    "name": "DAR Revenue",
                    "total_price": total_dar_revenue,
                    "fiatSymbol": currency["symbol"]
                },
                "profit_to_date": {
                    "name": "Profit to Date",
                    "total_price": profit_to_date,
                    "fiatSymbol": currency["symbol"]
                },
            }
        ]

