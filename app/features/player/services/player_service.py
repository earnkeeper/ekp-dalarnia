from app.features.player.documents.player_transaction_document import PlayerTransactionDocument
from db.dalarnia_transactions_repo import DalarniaTransactionsRepo
from ekp_sdk.services import CoingeckoService

class PlayerService:
    def __init__(
        self,
        dalarnia_transactions_repo: DalarniaTransactionsRepo,
        coingecko_service: CoingeckoService
    ):
        self.dalarnia_transactions_repo = dalarnia_transactions_repo
        self.coingecko_service = coingecko_service

    async def get_documents(self, currency, address):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        models = self.dalarnia_transactions_repo.filter_by_address(address)
        # print(models)
        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def remove_on_from_approve(self, description):
        """ temporary method """
        if "Approve" in description:
            description = description.split(" on")[0]
        return description



    def map_document(self, model, currency, rate):

        model: PlayerTransactionDocument = {
            "cost_bnb": round(model["bnbCost"], 5) if model["bnbCost"] else None,
            "cost_bnb_fiat": model["bnbCostUsd"] * rate if model["bnbCostUsd"] else model["bnbCostUsd"],
            "cost_dar": round(model["darCost"], 5) if model["darCost"] else None,
            "cost_dar_fiat": model["darCostUsd"] * rate if model["darCostUsd"] else model["darCostUsd"],
            "description": self.remove_on_from_approve(model["description"]),
            "fiat_symbol": currency["symbol"],
            "id": model["hash"],
            "darRev": round(model["darRev"], 5) if model["darRev"] else None,
            "darRevUsd": model["darRevUsd"] * rate if model["darRevUsd"] else model["darRevUsd"],
            "timestamp": model["timestamp"],
            "transaction_hash": model["hash"],
            "updated": "",
        }

        return model