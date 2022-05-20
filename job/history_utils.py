# from dalarnia_mongodb import MongoDb
import json
from datetime import datetime
from pprint import pprint

from decouple import config
from web3 import Web3
import requests as requests
from pymongo import MongoClient
from db.contract_transactions_repo import ContractTransactionsRepo
from ekp_sdk.services import (CacheService, CoingeckoService, EtherscanService,
                              Web3Service)


class PlayerHistory:
    # BSCSACN_API_KEY = '89A5FPSU6ABR84API3YMY4GJ9W45H7V4QZ'
    # con_link = 'mongodb://localhost:27017/'
    # cluster = MongoClient(con_link)
    # db = cluster['dalarnia']
    # collection_1 = db['contract_transactions']

    def __init__(
            self,
            contract_transactions_repo: ContractTransactionsRepo,
            etherscan_service: EtherscanService,
            web3_service: Web3Service,
    ):
        self.contract_transactions_repo = contract_transactions_repo
        self.etherscan_service = etherscan_service
        self.web3_service = web3_service

    # async def get_input_decoded_dict(self, hsh):
    #     tx = list(
    #         self.contract_transactions_repo.collection.find({
    #             'hash': hsh
    #         })
    #     )[0]
    #     contr_address = tx['to']
    #     return contr_address, func_params

    def craft_handler(self, param_dict):
        # print('recipe_id is:')
        # print(param_dict['_recipeId'])
        recipe_map = {
            "1001": "Garpen Copper Pick",
            "1011": "Unknown Armor",
            "1101": "Garpen Copper Armor",
            "1002": "Iron Pick",
            "1102": "Iron Armor",
            "1003": "Silver Pick",
            "1103": "Silver Armor",
            "1004": "Ozymodium Pick",
            "1104": "Ozymodium Armor",
            "1041": "Unknown Armor 2",
            "1131": "Unknown Armor 1131",
            "1005": "Unknown Armor 1005"
        }
        # try:
        if str(param_dict['_recipeId']) not in recipe_map.keys():
            recipe_map[str(param_dict['_recipeId'])] = f'Unknown Armor{param_dict["_recipeId"]}'
        armor = recipe_map[str(param_dict['_recipeId'])]
        # except KeyError:
        #     raise Exception({'Recipe Error': f'The recipe with id {param_dict["_recipeId"]} not found'})
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
        descr = ''
        if '_resourceIn' in param_dict.keys():
            descr = self.swap_handler(param_dict=param_dict, contract=contract,
                                 buy_key='_resourceOut', sell_key='_resourceIn')
        elif '_stableIdFrom' in param_dict.keys():
            descr = self.swap_handler(param_dict=param_dict, contract=contract,
                                 buy_key='_stableIdTo', sell_key='_stableIdFrom')
        elif '_digsToClose' in param_dict.keys():
            descr = f'Close Dig & Open Chests'
        elif '_digsToOpen' in param_dict.keys():
            descr = f'Buy 1 x Dig on Plot Id: {param_dict["_tokenId"]}'
        elif '_recipeId' in param_dict.keys() and '_tokenIds' in param_dict.keys():
            descr = self.craft_handler(param_dict)
        elif 'approved' in param_dict.keys():
            descr = f'Approve DAR for spending on {param_dict["operator"].lower()}'

        return descr

    def calc_cost_and_rev_dar(self, tran, descr, param_dict):
        cost_dar = None
        rev_dar = None
        # try:
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
            # try:
            cost_dar = int(data[10:74], 16) / 1000000
            # except ValueError as e:
                # print(tran)
                # print(list(tran['logs'].keys()))
                # print(min(list(tran['logs'].keys())))
                # print(first_log_key)
                # print(data)
                # print(tran['hash'])
                # raise Exception(e)
        # except KeyError:
        #     return cost_dar, rev_dar
        return cost_dar, rev_dar





# collection_2 = db['contract_transactions_updated']


# transactions_hashs = [
#                 '0x2013dd748f40766193ac50b4ce13df91a35b849d9d887c6e17fd88ca7699e270',  # sell tokens
#                 '0x545b83edbb3122bc29d0be63cfe53702dbd65aad44d3d15bfdc355ded485149b',  # buy tokens
#                 '0xf6009bf6f1657421b916d10c1114494c8579109d45847f7a27f7cb4f4bef6b5e',  # close dig
#                 '0xea6ddfb4be6944a13a03df8ab3a72a5f9aeb21fd92ba32198ee8a1d3b1fd92ae',  # open dig
#                 '0x9752285c0e5f50bab5d111a10fd963febb0bb1e0791888a390dc63648f9080a4',  # close dig
#                 '0x757f82ac922335b1c0d3c73e2c38353783e50fe89d033b2ce8551a09a3a54797',  # buy 150 iron
# #                 '0x88ac8f7fa0943b858879e314589795471eec24b15830bbc7c8bce53689870f8b'
#                 ]



# resource_name = map[tran["to"]]
# '_resourceIn'
# '_resourceOut'




# def dig_close_handler(param_dict):



# ph = PlayerHistory()
# for tr_hash in transactions_hashs:
#     contr_address, param_dict = ph.get_input_decoded_dict(ph.collection_1, hash=tr_hash)
#     # print(param_dict)
#     descr = ph.set_description(param_dict, contr_address)
#     print(descr)

# func_obj, func_params = contract.decode_function_input(res["input"])

# pprint(param_dict)

# print(int(res["input"][10:74], 16))
# print(int(res["input"][74:138], 16))
# print(int(res["input"][138:202], 16))
