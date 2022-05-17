from ekp_sdk.db import MgClient
from pymongo import DESCENDING, UpdateOne


class ContractTransactionsRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.contract_transactions = self.mg_client.db['contract_transactions']
        self.contract_transactions.create_index("hash", unique=True)
        self.contract_transactions.create_index([("blockNumber", DESCENDING)])
        self.contract_transactions.create_index([("timeStamp", DESCENDING)])
        self.contract_transactions.create_index("source_contract_address")

    def get_latest(self, contract_address):
        return list(
            self.contract_transactions.find(
                {"source_contract_address": contract_address}
            )
            .sort("blockNumber", -1).limit(1)
        )

    def bulk_write(self, trans):
        self.contract_transactions.bulk_write(
            list(map(lambda tran: UpdateOne({"hash": tran["hash"]}, {"$set": tran}, True), trans))
        )
        
