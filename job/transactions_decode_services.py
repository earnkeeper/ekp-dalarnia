from datetime import datetime

from ekp_sdk.services import (CacheService, CoingeckoService, EtherscanService,
                              Web3Service)
from web3 import Web3
from db.contract_logs_repo import ContractLogsRepo
from db.contract_transactions_repo import ContractTransactionsRepo
from db.market_transaction_repo import MarketTransactionsRepo
from job.history_utils import PlayerHistory


class TransactionDecoderService:
    def __init__(
            self,
            cache_service: CacheService,
            coingecko_service: CoingeckoService,
            contract_logs_repo: ContractLogsRepo,
            contract_transactions_repo: ContractTransactionsRepo,
            market_transactions_repo: MarketTransactionsRepo,
            etherscan_service: EtherscanService,
            web3_service: Web3Service,
            hist_utils: PlayerHistory
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.contract_logs_repo = contract_logs_repo
        self.contract_transactions_repo = contract_transactions_repo
        self.etherscan_service = etherscan_service
        self.market_transactions_repo = market_transactions_repo
        self.web3_service = web3_service
        self.hist_utils = hist_utils
        self.page_size = 2000

    async def decode_trans(self):
        print("✨ Decoding market transactions..")

        latest_block = self.market_transactions_repo.find_latest_block_number()
        # latest_block = 17032108
        while True:

            next_trans = self.contract_transactions_repo.find_since_block_number(
                latest_block,
                self.page_size
            )
            # print(f'len of trans is {len(next_trans)}')
            if not len(next_trans):
                break

            buys = []

            for next_tran in next_trans:
                # abi = await self.etherscan_service.get_abi(address=next_tran['to'])
                abi_key = f"abi_for_contract_{next_tran['to']}"
                abi_cached = await self.cache_service.wrap(abi_key,
                                                           lambda: self.etherscan_service.get_abi(address=next_tran['to'])
                                                           )
                func_params = self.web3_service.decode_input(abi_cached, next_tran["input"])

                input = next_tran["input"]
                block_number = next_tran["blockNumber"]

                if len(input) < 10:
                    latest_block = block_number
                    continue
                if next_tran["isError"]:
                    latest_block = block_number
                    continue

                buy = await self.__decode_tran(next_tran, func_params)
                if buy:
                    buys.append(buy)
                # if input.startswith("0x38edf988"):
                #     buy = await self.__decode_tran(next_tran)
                #     if buy:
                #         buys.append(buy)

                latest_block = block_number
                # if buy:
                    # print('here is the buy')
                    # print(buy)
            # print('here is the buys')
            # print(buys)
            if len(buys):
                self.market_transactions_repo.save(buys)

            if len(next_trans) < self.page_size:
                break

        print("✅ Finished decoding market transactions..")


    async def __decode_tran(self, tran, param_dict):
        if tran['to'] == '':
            # print('🚨 There was no recipient in transaction, so skipped ...')
            return None
        if not param_dict:
            # print('🚨 There was no input in transaction, so skipped ...')
            return None
        # print(tran['hash'])
        # try:
        descr = self.hist_utils.set_description(param_dict, tran['to'])
        # except KeyError as e:
        #     print(f'{e}\n'
        #           f'transaction hash: {tran["hash"]}')
        #     raise Exception(e)
        if descr == '':
            # print(tran['hash'])
            # print('🚨 There was no description in transaction, so skipped ...')
            return None

        hash = tran["hash"]
        timestamp = tran["timeStamp"]
        block_number = tran["blockNumber"]
        date_str = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y")

        bnb_cache_key = f"bnb_price_{date_str}"
        bnb_usd_price = await self.cache_service.wrap(bnb_cache_key,
                                                      lambda: self.coingecko_service.get_historic_price("binancecoin",
                                                                                                        date_str,
                                                                                                        "usd"))

        bnb_cost = Web3.fromWei(tran["gasUsed"] * int(tran["gasPrice"]), 'ether')
        # price = sum(distributions)
        # fees = price - distributions[-1]
        # try:
        cost_dar, rev_dar = self.hist_utils.calc_cost_and_rev_dar(tran, descr, param_dict)
        # except KeyError as e:
        #     print(f'{e}\n'
        #           f'transaction hash: {tran["hash"]}')
        #     raise Exception(e)
        return {
            "bnbCost": float(bnb_cost) if bnb_cost else None,
            "bnbCostUsd": float(bnb_cost) * bnb_usd_price if bnb_cost else None,
            "darCost": float(cost_dar) if cost_dar else None,
            "darCostUsd": float(cost_dar) * bnb_usd_price if cost_dar else None,
            "darRev": float(rev_dar) if rev_dar else None,
            "darRevUsd": float(rev_dar) * bnb_usd_price if rev_dar else None,
            "blockNumber": block_number,
            "player_address": tran["from"],
            "description": descr,
            "hash": hash,
            "timestamp": timestamp,
        }
