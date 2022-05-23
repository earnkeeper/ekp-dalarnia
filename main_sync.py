import asyncio

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.dalarnia_transactions_repo import MarketTransactionsRepo
from sync.history_utils import PlayerHistory
from sync.transactions_decode_services import TransactionDecoderService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        self.hist_utils = PlayerHistory(
            contract_transactions_repo=self.contract_transactions_repo,
            etherscan_service=self.etherscan_service,
            web3_service=self.web3_service,
        )

        self.market_decoder_service = TransactionDecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_logs_repo=self.contract_logs_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            etherscan_service=self.etherscan_service,
            hist_utils=self.hist_utils,
            market_transactions_repo=self.market_transactions_repo,
            web3_service=self.web3_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    loop = asyncio.get_event_loop()

    contract_addresses = [
        '0x2e0058951ded269e33f776c8ea44136803b23a88',  # PlanetPlotHandler
        '0x92fe453dd29ceb6c631cb06ccec50f23e1220d14',  # Pair
        '0xc4ea71878a4f1d92215e2ed680e325966ab6e1eb',  # ResourcesHandler
        '0x96dfbd2c945bca02378ffd8e4593054d098e8bac',  # Pair
        '0xca9160f5637d7160168ee2064741e17cc31a0d29',  # Pair
        '0x23ce9e926048273ef83be0a3a8ba9cb6d45cd978',  # BEP20Token
        '0xa1cb40dcd114a06bc484880c1cf57a6b1b42950b',  # Items
        '0x3c45e5c77cc40eb51eaa5e85c1a9b30a43764ca9'  # Resources
    ]

    log_addresses = [
        '0x2e0058951ded269e33f776c8ea44136803b23a88',  # PlanetPlotHandler
        '0x92fe453dd29ceb6c631cb06ccec50f23e1220d14',  # Pair
        '0xc4ea71878a4f1d92215e2ed680e325966ab6e1eb',  # ResourcesHandler
        '0x96dfbd2c945bca02378ffd8e4593054d098e8bac',  # Pair
        '0xca9160f5637d7160168ee2064741e17cc31a0d29',  # Pair
        '0x23ce9e926048273ef83be0a3a8ba9cb6d45cd978',  # BEP20Token
        '0xa1cb40dcd114a06bc484880c1cf57a6b1b42950b',  # Items
        '0x3c45e5c77cc40eb51eaa5e85c1a9b30a43764ca9'  # Resources
    ]

    futures = []

    start_block = 17573419  # This is where the market pairs opened

    for contract_address in contract_addresses:
        futures.append(
            container.transaction_sync_service.sync_transactions(
                contract_address,
                start_block
            )
        )

    for log_address in log_addresses:
        futures.append(
            container.transaction_sync_service.sync_logs(
                log_address,
                start_block
            )
        )

    loop.run_until_complete(
        asyncio.gather(*futures)
    )

    loop.run_until_complete(
        container.market_decoder_service.decode_trans()
    )
