from db.dalarnia_transactions_repo import MarketTransactionsRepo
from ekp_sdk.services import CoingeckoService
from app.features.profit_tracker.services.tracker_transaction_document import TrackerTransactionDocument

class ProfitTrackerService:
    def __init__(
        self,
        market_transactions_repo: MarketTransactionsRepo,
        coingecko_service: CoingeckoService
    ):
        self.market_transactions_repo = market_transactions_repo
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency):
        return []
        # rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])
        #
        # models = self.market_transactions_repo.find_all(1000)
        #
        # documents = []
        #
        # for model in models:
        #     document = self.map_document(model, currency, rate)
        #     documents.append(document)
        #
        # return documents

    def map_document(self, model, currency, rate):

        model: TrackerTransactionDocument = {
            "cost_bnb": model["cost_bnb"],
            "cost_bnb_fiat": model["cost_bnb_fiat"],
            "cost_dar": model["cost_dar"],
            "cost_dar_fiat": model["cost_dar_fiat"],
            "description": model["description"],
            "fiat_symbol": model["fiat_symbol"],
            "id": model["id"],
            "darRev": model["revenue_dar"],
            "darRevUsd": model["revenue_dar_fiat"],
            "timestamp": model["timestamp"],
            "transaction_hash": model["transaction_hash"],
            "updated": model["updated"],
        }

        return model