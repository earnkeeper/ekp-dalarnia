from db.dalarnia_transactions_repo import DalarniaTransactionsRepo
from ekp_sdk.services import CoingeckoService


class PlayersService:
    def __init__(
            self,
            dalarnia_transactions_repo: DalarniaTransactionsRepo,
            coingecko_service: CoingeckoService
    ):
        self.dalarnia_transactions_repo = dalarnia_transactions_repo
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency, form_values):
        documents = []
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])
        for form_value in form_values:
            total_bnb_cost = (self.dalarnia_transactions_repo.filter_and_sum('bnbCostUsd',
                                                                             form_value["address"]) or 0)
            total_dar_cost = (self.dalarnia_transactions_repo.filter_and_sum('darCostUsd',
                                                                             form_value["address"]) or 0)
            total_dar_revenue = (self.dalarnia_transactions_repo.filter_and_sum('darRevUsd',
                                                                                form_value["address"]) or 0)
            cost = total_bnb_cost + total_dar_cost
            profit = total_dar_revenue - total_bnb_cost - total_dar_cost
            documents.append(
                {
                    "id": form_value["address"],
                    "cost": cost,
                    "cost_fiat": cost * rate,
                    "rev": total_dar_revenue,
                    "rev_fiat": total_dar_revenue * rate,
                    "profit": profit,
                    "profit_fiat": profit * rate,
                    "fiat_symbol": currency["symbol"],
                    # "cost": {
                    #     "name": "Cost",
                    #     "price": cost,
                    #     "fiatSymbol": currency["symbol"]
                    # },
                    # "rev": {
                    #     "name": "Rev",
                    #     "price": total_dar_revenue,
                    #     "fiatSymbol": currency["symbol"]
                    # },
                    # "profit": {
                    #     "name": "Profit",
                    #     "price": profit,
                    #     "fiatSymbol": currency["symbol"]
                    # }
                }
            )

            # "cost_bnb": model["bnbCost"],
            # "cost_bnb_fiat": model["bnbCostUsd"] * rate if model["bnbCostUsd"] else model["bnbCostUsd"],
            # "cost_dar": model["darCost"],
            # "cost_dar_fiat": model["darCostUsd"] * rate if model["darCostUsd"] else model["darCostUsd"],
            # "description": model["description"],
            # "fiat_symbol": currency["symbol"],
            # "id": model["hash"],
            # "darRev": model["darRev"],
            # "darRevUsd": model["darRevUsd"] * rate if model["darRevUsd"] else model["darRevUsd"],
            # "timestamp": model["timestamp"],
            # "transaction_hash": model["hash"],
            # "updated": "",

        return documents
