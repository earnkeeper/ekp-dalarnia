from ekp_sdk.db import MgClient
from pymongo import UpdateOne
import time
from decimal import Decimal
from bson.decimal128 import Decimal128


class DalarniaTransactionsRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['market_transactions']
        self.collection.create_index("hash", unique=True)
        self.collection.create_index("blockNumber")
        self.collection.create_index("player_address")
        self.collection.create_index("timestamp")

    def find_all(self, limit):
        start = time.perf_counter()

        results = list(
            self.collection
            .find()
            .sort("timestamp")
            .limit(limit)
        )

        print(
            f"⏱  [MarketTransactionsRepo.find_all({len(results)})] {time.perf_counter() - start:0.3f}s")

        return results

    def filter_and_sum(self, field_name):
        result = list(
            self.collection.aggregate(
                [
                    {
                        "$group":
                        {
                            "_id": None,
                            "total": {"$sum": f"${field_name}"}
                        }
                    }
                ])
        )

        if not len(result):
            return None

        return result[0]['total']

    def find_latest_block_number(self):
        results = list(
            self.collection
            .find()
            .sort("blockNumber", -1)
            .limit(1)
        )

        if not len(results):
            return 0

        return results[0]["blockNumber"]

    def save(self, trans):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda tran: UpdateOne(
                {"hash": tran["hash"]}, {"$set": tran}, True), trans))
        )

        print(
            f"⏱  [MarketTransactionsRepo.save({len(trans)})] {time.perf_counter() - start:0.3f}s")
