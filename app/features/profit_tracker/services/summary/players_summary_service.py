from datetime import datetime

from db.dalarnia_transactions_repo import DalarniaTransactionsRepo
from ekp_sdk.services import CoingeckoService


class PlayersSummaryService:
    def __init__(
            self,
            dalarnia_transactions_repo: DalarniaTransactionsRepo,
            coingecko_service: CoingeckoService
    ):
        self.dalarnia_transactions_repo = dalarnia_transactions_repo
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])
        total_bnb_cost = (self.dalarnia_transactions_repo.filter_and_sum('bnbCostUsd') or 0) * rate
        total_dar_cost = (self.dalarnia_transactions_repo.filter_and_sum('darCostUsd') or 0) * rate
        total_dar_revenue = (self.dalarnia_transactions_repo.filter_and_sum('darRevUsd') or 0) * rate
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
