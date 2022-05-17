from db.contract_transactions_repo import ContractTransactionsRepo
from ekp_sdk.services import EtherscanService


class SyncService:
    def __init__(
        self,
        contract_transactions_repo: ContractTransactionsRepo,
        etherscan_service: EtherscanService,
    ):
        self.contract_transactions_repo = contract_transactions_repo
        self.etherscan_service = etherscan_service
        self.page_size = 2000

    async def process(self, contract_address):
        start_block = 0

        latest_transaction = self.contract_transactions_repo.get_latest(
            contract_address
        )

        if latest_transaction is not None and len(latest_transaction):
            start_block = latest_transaction[0]["blockNumber"]

        while True:
            trans = await self.etherscan_service.get_transactions(contract_address, start_block, self.page_size)

            if len(trans) == 0:
                break

            print(f"Retrieved {len(trans)} from the api, saving to db...")

            models = []

            for tran in trans:
                block_number = int(tran["blockNumber"])

                if block_number > start_block:
                    start_block = block_number

                tran["blockNumber"] = block_number
                tran["source_contract_address"] = contract_address
                tran["confirmations"] = int(tran["confirmations"])
                tran["cumulativeGasUsed"] = int(tran["cumulativeGasUsed"])
                tran["gas"] = int(tran["gas"])
                tran["gasUsed"] = int(tran["gasUsed"])
                tran["gasUsed"] = int(tran["gasUsed"])
                tran["isError"] = tran["isError"] == "1"
                tran["timeStamp"] = int(tran["timeStamp"])
                tran["transactionIndex"] = int(tran["transactionIndex"])

                models.append(tran)

            self.contract_transactions_repo.bulk_write(models)

            if (len(trans) < self.page_size):
                break
