from db.contract_logs_repo import ContractLogsRepo
from db.contract_transactions_repo import ContractTransactionsRepo
from ekp_sdk.services import EtherscanService
from ast import literal_eval

class TransactionSyncService:
    def __init__(
        self,
        contract_transactions_repo: ContractTransactionsRepo,
        contract_logs_repo: ContractLogsRepo,
        etherscan_service: EtherscanService,
    ):
        self.contract_transactions_repo = contract_transactions_repo
        self.contract_logs_repo = contract_logs_repo
        self.etherscan_service = etherscan_service
        self.page_size = 2000

    async def sync_transactions(self, contract_address):
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

            print(f"Retrieved {len(trans)} trans from the api, saving to db...")

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
                tran["gasPrice"] = int(tran["gasPrice"])
                tran["isError"] = tran["isError"] == "1"
                tran["timeStamp"] = int(tran["timeStamp"])
                tran["transactionIndex"] = int(tran["transactionIndex"])

                models.append(tran)

            self.contract_transactions_repo.bulk_write(models)

            if (len(trans) < self.page_size):
                break

    async def sync_logs(self, log_address):
        start_block = 0

        latest_log = self.contract_logs_repo.get_latest(
            log_address
        )

        if latest_log is not None and len(latest_log):
            start_block = latest_log[0]["blockNumber"]

        while True:
            logs = await self.etherscan_service.get_logs(log_address, start_block)

            if len(logs) == 0:
                break

            print(f"Retrieved {len(logs)} logs from the api, saving to db...")

            models = []

            for log in logs:
                block_number = literal_eval(log["blockNumber"])

                if block_number > start_block:
                    start_block = block_number

                log["blockNumber"] = block_number
                log["gasUsed"] = literal_eval(log["gasUsed"])
                log["gasPrice"] = literal_eval(log["gasPrice"])
                log["timeStamp"] = literal_eval(log["timeStamp"])
                log["logIndex"] = literal_eval(log["logIndex"])
                log["transactionIndex"] = None

                models.append(log)

            self.contract_logs_repo.bulk_write(models)

            if (len(logs) < 1000):
                break