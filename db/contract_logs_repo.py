from ekp_sdk.db import MgClient
from pymongo import DESCENDING, UpdateOne


class ContractLogsRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['contract_logs']
        self.collection.create_index("transactionHash", unique=True)
        self.collection.create_index([("blockNumber", DESCENDING)])
        self.collection.create_index([("timeStamp", DESCENDING)])
        self.collection.create_index("address")

    def get_latest(self, address):
        return list(
            self.collection.find(
                {"address": address}
            )
            .sort("blockNumber", -1)
            .limit(1)
        )

    def bulk_write(self, logs):
        self.collection.bulk_write(
            list(map(lambda log: UpdateOne({"transactionHash": log["transactionHash"]}, {"$set": log}, True), logs))
        )
        
