from ekp_sdk.db import MgClient
from pymongo import DESCENDING, UpdateOne


class DalarniaTransactionsRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['dalarnia_transactions']
        self.collection.create_index("hash", unique=True)
        self.collection.create_index([("blockNumber", DESCENDING)])
        self.collection.create_index([("timestamp", DESCENDING)])
        self.collection.create_index("playerAddress")

    def bulk_write(self, trans):
        self.collection.bulk_write(
            list(map(lambda tran: UpdateOne({"hash": tran["hash"]}, {"$set": tran}, True), trans))
        )
        
