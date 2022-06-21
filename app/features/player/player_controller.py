from pprint import pprint

from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path
from app.features.player.player_page import player_page

from app.features.player.services.player_service import PlayerService
from app.features.player.services.player_summary_service import PlayersSummaryService

TRANSACTIONS_COLLECTION_NAME = "dalarnia_player_transactions"
SUMMARY_COLLECTION_NAME = "dalarnia_player_summary"


class PlayerController:
    def __init__(
        self,
        client_service: ClientService,
        player_service: PlayerService,
        player_summary_service: PlayersSummaryService
    ):
        self.client_service = client_service
        self.player_service = player_service
        self.player_summary_service = player_summary_service
        self.path = 'player/:playerAddress'

    async def on_connect(self, sid):
        await self.client_service.emit_page(
            sid,
            self.path,
            player_page(
                TRANSACTIONS_COLLECTION_NAME,
                SUMMARY_COLLECTION_NAME,
            )
        )
        

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if not path or not path.startswith("player/"):
            return

        await self.client_service.emit_busy(sid, TRANSACTIONS_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, SUMMARY_COLLECTION_NAME)

        address = path.replace("player/", "")
        print(address)
        currency = client_currency(event)

        # Transactions
        
        transaction_documents = await self.player_service.get_documents(currency, address)

        await self.client_service.emit_documents(
            sid,
            TRANSACTIONS_COLLECTION_NAME,
            transaction_documents
        )

        # Summary

        summary_documents = await self.player_summary_service.get_documents(currency, address)

        pprint(summary_documents)

        await self.client_service.emit_documents(
            sid,
            SUMMARY_COLLECTION_NAME,
            summary_documents
        )

        await self.client_service.emit_done(sid, TRANSACTIONS_COLLECTION_NAME)
        await self.client_service.emit_done(sid, SUMMARY_COLLECTION_NAME)
