
import asyncio
import os

from decouple import AutoConfig, config
from ekp_sdk import BaseContainer
from db.contract_logs_repo import ContractLogsRepo

from db.contract_transactions_repo import ContractTransactionsRepo
from job.transaction_sync_service import TransactionSyncService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        self.contract_transactions_repo = ContractTransactionsRepo(
            mg_client=self.mg_client,
        )
        
        self.contract_logs_repo = ContractLogsRepo(
            mg_client=self.mg_client,
        )

        self.sync_service = TransactionSyncService(
            contract_transactions_repo=self.contract_transactions_repo,
            contract_logs_repo=self.contract_logs_repo,
            etherscan_service=self.etherscan_service
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    loop = asyncio.get_event_loop()

    contract_addresses = [
        '0x2e0058951ded269e33f776c8ea44136803b23a88',
        '0x92fe453dd29ceb6c631cb06ccec50f23e1220d14',
        '0xc4ea71878a4f1d92215e2ed680e325966ab6e1eb',
        '0x96dfbd2c945bca02378ffd8e4593054d098e8bac',
        '0xca9160f5637d7160168ee2064741e17cc31a0d29',
        '0x23ce9e926048273ef83be0a3a8ba9cb6d45cd978',
        '0xa1cb40dcd114a06bc484880c1cf57a6b1b42950b',
        '0x3c45e5c77cc40eb51eaa5e85c1a9b30a43764ca9'
    ]
    
    log_addresses = [
        '0x92fe453dd29ceb6c631cb06ccec50f23e1220d14',
        '0x96dfbd2c945bca02378ffd8e4593054d098e8bac'
    ]
    
    futures = []
    
    for contract_address in contract_addresses:
        futures.append(container.sync_service.sync_transactions(contract_address))
    
    for log_address in log_addresses:
        futures.append(container.sync_service.sync_logs(log_address))
        
    loop.run_until_complete(
        asyncio.gather(*futures)
    )
