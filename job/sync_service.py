import sys
from ast import literal_eval
from collections import Counter

from db.contract_transactions_repo import ContractTransactionsRepo
from ekp_sdk.services import EtherscanService
from db.contract_logs_repo import ContractLogsRepo


def handle_0x(log_item):
    if log_item == "0x":
        log_item = 0
    else:
        log_item = literal_eval(log_item)
    return log_item


class SyncService:
    def __init__(
            self,
            contract_transactions_repo: ContractTransactionsRepo,
            contract_logs_repo: ContractLogsRepo,
            etherscan_service: EtherscanService,
    ):
        self.contract_transactions_repo = contract_transactions_repo
        self.contract_logs_repo = contract_logs_repo
        self.etherscan_service = etherscan_service
        self.page_size = 1000

    async def sync_transactions(self, contract_address):
        start_block = 0

        latest_transaction = self.contract_transactions_repo.get_latest(
            contract_address
        )

        if latest_transaction is not None and len(latest_transaction):
            start_block = latest_transaction[0]["blockNumber"]

        while True:
            # if start_block in [12355171, 12355172]:
            #     start_block = 12355175
            trans = await self.etherscan_service.get_transactions(contract_address, start_block, self.page_size)

            c = Counter(t['blockNumber'] for t in trans)
            # print(c)
            if 1000 in c.values():
                stdoutOrigin = sys.stdout
                sys.stdout = open(f"trans_blocks_missing.txt", "a")
                print(f'Transaction with block number {start_block} is skipped')
                sys.stdout.close()
                sys.stdout = stdoutOrigin
                start_block = start_block + 1
                continue

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
                tran["isError"] = tran["isError"] == "1"
                tran["timeStamp"] = int(tran["timeStamp"])
                tran["transactionIndex"] = int(tran["transactionIndex"])

                models.append(tran)

            self.contract_transactions_repo.save(models)

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
            # print(start_block)
            # print(type(start_block))
            # if start_block in [12355171, 12355172, 12355244]:
            #     start_block = start_block + 1
            # start_block = hex(start_block)

            # start_block = 17691873
            # print(f'start_block after is {start_block}')
            # print(f'start_block type after is {type(start_block)}')
            logs = await self.etherscan_service.get_logs(log_address, start_block)

            c = Counter(l['blockNumber'] for l in logs)
            if 1000 in c.values():
                stdoutOrigin = sys.stdout
                sys.stdout = open(f"logs_blocks_missing.txt", "a")
                print(f'Log with block number {start_block} and address {log_address} is skipped')
                sys.stdout.close()
                sys.stdout = stdoutOrigin
                start_block = start_block + 1
                continue

            if len(logs) == 0:
                break

            print(f"Retrieved {len(logs)} logs from the api, saving to db...")

            models = []

            for log in logs:
                # print(f'Here we are fetching the logs for the address {log["address"]}')
                block_number = literal_eval(log["blockNumber"])

                if block_number > start_block:
                    start_block = block_number
                # print(log["gasUsed"])
                log["blockNumber"] = block_number
                log["gasUsed"] = handle_0x(log["gasUsed"])
                log["gasPrice"] = handle_0x(log["gasPrice"])
                log["timeStamp"] = handle_0x(log["timeStamp"])
                # log["gasUsed"] = literal_eval(log["gasUsed"])
                # log["gasPrice"] = literal_eval(log["gasPrice"])
                # log["timeStamp"] = literal_eval(log["timeStamp"])
                log["logIndex"] = handle_0x(log["logIndex"])
                log["transactionIndex"] = handle_0x(log["transactionIndex"])


                models.append(log)

            self.contract_logs_repo.save(models)
            self.contract_transactions_repo.save_logs(models)

            if (len(logs) < 1000):
                break
