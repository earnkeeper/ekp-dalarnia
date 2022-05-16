
import asyncio

from decouple import config
from dalarnia_mongodb import MongoDb

from sync_dalarnia_transactions import SyncTransactions

if __name__ == '__main__':
    mongo_db = MongoDb()

    loop = asyncio.get_event_loop()

    list_of_contracts = [
                         '0x2e0058951ded269e33f776c8ea44136803b23a88',
                         '0x92fe453dd29ceb6c631cb06ccec50f23e1220d14',
                         '0xc4ea71878a4f1d92215e2ed680e325966ab6e1eb',
                         '0x96dfbd2c945bca02378ffd8e4593054d098e8bac',
                         '0xca9160f5637d7160168ee2064741e17cc31a0d29',
                         '0x23ce9e926048273ef83be0a3a8ba9cb6d45cd978',
                         '0xa1cb40dcd114a06bc484880c1cf57a6b1b42950b',
                         '0x3c45e5c77cc40eb51eaa5e85c1a9b30a43764ca9']

    for contract_address in list_of_contracts:
        print(f'The contract which is going to be synced now: {contract_address}')
        market_sync = SyncTransactions(
            contract_address,
            mongo_db,
            config("MAX_TRANS_TO_FETCH", default=0, cast=int)
        )
        loop.run_until_complete(
            market_sync.process()
        )

    # Pegaxy Market

