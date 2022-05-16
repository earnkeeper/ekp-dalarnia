import json

import aiohttp
from aioretry import retry
# from db.mongo_db import MongoDb
from decouple import config
from retry import defaullt_retry_policy


class SyncTransactions:
    BSCSACN_API_KEY = config('BSCSCAN_API_KEY')

    def __init__(self, contract_address, mongo_db, max_trans_to_fetch=0):
        self.contract_address = contract_address
        self.max_trans_to_fetch = max_trans_to_fetch
        self.mongo_db = mongo_db
        self.start_block = 0
        self.page_size = 2000

    async def process(self):
        self.get_latest_start_block()

        async with aiohttp.ClientSession() as session:
            while True:
                url = f'https://api.bscscan.com/api?module=account&action=txlist&address={self.contract_address}&startblock={self.start_block}&page=1&offset={self.page_size}&sort=asc&apiKey={self.BSCSACN_API_KEY}'

                trans = await self.get_transactions(url, session)

                if len(trans) == 0:
                    break
                # print(trans)
                print(f"Retrieved {len(trans)} from the api, saving to db...")
                trans_list = []
                for tran in trans:
                    # print(tran)
                    block_number = int(tran["blockNumber"])
                    # print(f'block_number is {block_number}')
                    # print(f'startblock is {self.start_block}')
                    if block_number > self.start_block:
                        self.start_block = block_number

                    tran["blockNumber"] = block_number
                    tran["source_contract_address"] = self.contract_address
                    tran["confirmations"] = int(tran["confirmations"])
                    tran["cumulativeGasUsed"] = int(tran["cumulativeGasUsed"])
                    tran["gas"] = int(tran["gas"])
                    tran["gasUsed"] = int(tran["gasUsed"])
                    tran["gasUsed"] = int(tran["gasUsed"])
                    tran["isError"] = tran["isError"] == "1"
                    tran["timeStamp"] = int(tran["timeStamp"])
                    tran["transactionIndex"] = int(tran["transactionIndex"])

                    trans_list.append(tran)
                # print(len(trans_list))
                # print(trans_list)
                # def format_write(tran):
                #     return UpdateOne({"hash": tran["hash"]}, {"$set": tran}, True)

                self.mongo_db.insert_data(trans_list)

                if (len(trans) < self.page_size or self.max_trans_to_fetch > 0 and len(trans) > self.max_trans_to_fetch):
                    break

    def get_latest_start_block(self):
        latest = self.mongo_db.get_latest(
            contract_address=self.contract_address)
        if latest is not None and len(latest):
            self.start_block = latest[0]["blockNumber"]

    @retry(defaullt_retry_policy)
    async def get_transactions(self, url, session):
        print(url)

        response = await session.get(url=url)

        if (response.status != 200):
            raise Exception(f"Response code: {response.status}")

        text = await response.read()
        data = json.loads(text.decode())
        trans = data["result"]

        if (trans is None):
            print(text)
            raise Exception("Received None data from url")

        return trans
