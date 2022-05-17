import asyncio

from decouple import AutoConfig
from ekp_sdk.services import EtherscanService, RestClient, Web3Service


async def get_trans(address):
    config = AutoConfig(".env")
    rest_client = RestClient()

    etherscan_service = EtherscanService(
        rest_client=rest_client,
        api_key=config("ETHERSCAN_API_KEY"),
        base_url=config("ETHERSCAN_BASE_URL")
    )

    web3_service = Web3Service(
        provider_url=config("WEB3_PROVIDER_URL")
    )

    abi = await etherscan_service.get_abi(address)
    
    trans = await etherscan_service.get_transactions(address, 0, 100)

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
    
    recipes = {}
    
    for tran in trans:
        if tran["input"].startswith("0x75d168e3"):
            params = web3_service.decode_input(abi, tran["input"])
            recipeId = params["_recipeId"]
            recipes[recipeId] = params["_RIAmounts"]

    print(recipes)
if __name__ == '__main__':

    loop = asyncio.run(get_trans("0xc4ea71878a4f1d92215e2ed680e325966ab6e1eb"))
