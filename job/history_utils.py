# from dalarnia_mongodb import MongoDb
import json
from datetime import datetime
from pprint import pprint

from decouple import config
from web3 import Web3
import requests as requests
from pymongo import MongoClient




class PlayerHistory:
    BSCSACN_API_KEY = config('BSCSCAN_API_KEY')
    con_link = 'mongodb://localhost:27017/'
    cluster = MongoClient(con_link)
    db = cluster['dalarnia']
    collection_1 = db['contract_transactions']

    def get_input_decoded_dict(self, coll, hsh):
        # print('Hello')
        tx = list(coll.find({
            'hash': hsh
        }
        ))[0]
        contr_address = tx['to']
        # print(contr_address)
        # if not contr_address:
        #     return contr_address, {}
        abi_endpoint = f"https://api.bscscan.com/api?module=contract&action=getabi&address={contr_address}&apikey={self.BSCSACN_API_KEY}"
        abi = json.loads(requests.get(abi_endpoint).text)
        w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
        contract = w3.eth.contract(address=Web3.toChecksumAddress(contr_address), abi=abi["result"])
        func_obj, func_params = contract.decode_function_input(tx["input"])
        for key, value in func_params.items():
            if isinstance(value, bytes):
                func_params[key] = value.decode('utf-8', 'ignore')

        # print(contr_address)
        # print(func_params)
        return contr_address, func_params

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
        elif '_recipeId' in param_dict.keys():
            descr = self.craft_handler(param_dict)
        elif 'approved' in param_dict.keys():
            descr = f'Approve DAR for spending on {param_dict["operator"].lower()}'

        return descr

    def calc_cost_and_rev_dar(self, tran, descr, param_dict):
        cost_dar = None
        rev_dar = None
        if 'Market' in descr:
            last_log_key = max(list(tran['logs'].keys()))
            data = tran['logs'][last_log_key]['data']
            if 'Sell' in descr:
                rev_dar = int(data[138:202], 16) / 1000000
            elif 'Buy' in descr:
                cost_dar = int(data[138:202], 16) / 1000000

        elif 'Dig' in descr:
            if 'Buy' in descr:
                cost_dar = int(param_dict['_currentRent']) / 1000000

        elif 'Craft' in descr:
            first_log_key = min(list(tran['logs'].keys()))
            data = tran['logs'][first_log_key]['data']
            cost_dar = int(data[10:74], 16) / 1000000

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
