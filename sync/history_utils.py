from ekp_sdk.db import ContractTransactionsRepo
from ekp_sdk.services import EtherscanService, Web3Service


class PlayerHistory:

    def __init__(
            self,
            contract_transactions_repo: ContractTransactionsRepo,
            etherscan_service: EtherscanService,
            web3_service: Web3Service,
    ):
        self.contract_transactions_repo = contract_transactions_repo
        self.etherscan_service = etherscan_service
        self.web3_service = web3_service

    def craft_handler(self, param_dict):
        recipe_map = {
            "1001": "Garpen Copper Pick",
            "1101": "Garpen Copper Armor",
            "1002": "Iron Pick",
            "1102": "Iron Armor",
            "1003": "Silver Pick",
            "1103": "Silver Armor",
            "1004": "Ozymodium Pick",
            "1104": "Ozymodium Armor",
        }
        if str(param_dict['_recipeId']) not in recipe_map.keys():
            recipe_map[str(param_dict['_recipeId'])
                       ] = f'Unknown Armor {param_dict["_recipeId"]}'
        armor = recipe_map[str(param_dict['_recipeId'])]
        descr = f'Craft 1 x {armor}'
        return descr

    def swap_handler(self, param_dict, contract, buy_key, sell_key):
        token_mapper = {
            "0x92fe453dd29ceb6c631cb06ccec50f23e1220d14": "Garpen Copper",
            "0x96dfbd2c945bca02378ffd8e4593054d098e8bac": "Crafting Catalyst",
            "0xca9160f5637d7160168ee2064741e17cc31a0d29": "Iron",
        }
        swap_type = ''
        token_amount = ''
        if param_dict[sell_key] == 0 and param_dict[buy_key] != 0:
            swap_type = 'Market Buy'
            token_amount = param_dict[buy_key]
        elif param_dict[sell_key] != 0 and param_dict[buy_key] == 0:
            swap_type = 'Market Sell'
            token_amount = param_dict[sell_key]

        descr = f'{swap_type} {token_amount} x {token_mapper[contract]}'
        return descr

    def set_description(self, param_dict, contract):
        descr = None
        if '_resourceIn' in param_dict.keys():
            descr = self.swap_handler(
                param_dict=param_dict,
                contract=contract,
                buy_key='_resourceOut',
                sell_key='_resourceIn'
            )
        elif '_stableIdFrom' in param_dict.keys():
            descr = self.swap_handler(
                param_dict=param_dict,
                contract=contract,
                buy_key='_stableIdTo',
                sell_key='_stableIdFrom'
            )
        elif '_digsToClose' in param_dict.keys():
            descr = f'Close Dig & Open Chests'
        elif '_digsToOpen' in param_dict.keys():
            descr = f'Buy 1 x Dig on Plot Id: {param_dict["_tokenId"]}'
        elif '_recipeId' in param_dict.keys() and '_tokenIds' in param_dict.keys():
            descr = self.craft_handler(param_dict)
        elif '_plotTokenId' in param_dict.keys():
            descr = "Plot RU"
        elif 'approved' in param_dict.keys():
            descr = f'Approve DAR for spending on {param_dict["operator"].lower()}'

        return descr

    def calc_cost_and_rev_dar(self, tran, descr, param_dict):
        cost_dar = None
        rev_dar = None
        if 'Market' in descr:
            log_keys = list(map(int, list(tran['logs'].keys())))
            last_log_key = str(max(log_keys))
            data = tran['logs'][last_log_key]['data']
            if 'Sell' in descr:
                rev_dar = int(data[138:202], 16) / 1000000
            elif 'Buy' in descr:
                cost_dar = int(data[138:202], 16) / 1000000

        elif 'Dig' in descr:
            if 'Buy' in descr:
                cost_dar = int(param_dict['_currentRent']) / 1000000

        elif 'Craft' in descr:
            log_keys = list(map(int, list(tran['logs'].keys())))
            first_log_key = str(min(log_keys))
            data = tran['logs'][first_log_key]['data']
            cost_dar = int(data[10:74], 16) / 1000000

        return cost_dar, rev_dar
