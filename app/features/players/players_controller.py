from app.features.players.players_page import players_page
from app.features.players.players_service import PlayersService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path, form_values

PLAYERS_COLLECTION_NAME = "darlarnia_players"

class PlayersController:
    def __init__(
        self,
        client_service: ClientService,
        players_service: PlayersService,
    ):
        self.client_service = client_service
        self.players_service = players_service
        self.path = 'players'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'users',
            'Players',
            self.path
        )
        
        await self.client_service.emit_page(
            sid,
            self.path,
            players_page(
                PLAYERS_COLLECTION_NAME,
            )
        )
        

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, PLAYERS_COLLECTION_NAME)

        currency = client_currency(event)

        address_form_values = form_values(event, "dalarnia_player_addresses")
        documents = await self.players_service.get_documents(address_form_values or [])

        await self.client_service.emit_documents(
            sid,
            PLAYERS_COLLECTION_NAME,
            documents
        )

        await self.client_service.emit_done(sid, PLAYERS_COLLECTION_NAME)
