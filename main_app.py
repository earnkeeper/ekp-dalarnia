from decouple import AutoConfig
from ekp_sdk import BaseContainer
from app.features.player.player_controller import PlayerController
from app.features.player.services.player_service import PlayerService
from app.features.player.services.player_summary_service import PlayersSummaryService
from app.features.players.players_controller import PlayersController
from app.features.players.players_service import PlayersService
from db.dalarnia_transactions_repo import DalarniaTransactionsRepo

class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        # DB

        self.dalarnia_transactions_repo = DalarniaTransactionsRepo(
            mg_client=self.mg_client,
        )

        # FEATURES - PLAYER

        self.player_service = PlayerService(
            coingecko_service=self.coingecko_service,
            dalarnia_transactions_repo=self.dalarnia_transactions_repo
        )

        self.player_summary_service = PlayersSummaryService(
            coingecko_service=self.coingecko_service,
            dalarnia_transactions_repo=self.dalarnia_transactions_repo,
        )

        self.player_controller = PlayerController(
            client_service=self.client_service,
            player_service=self.player_service,
            player_summary_service=self.player_summary_service
        )
        
        # FEATURES - PLAYERS

        self.players_service = PlayersService(
        )

        self.players_controller = PlayersController(
            client_service=self.client_service,
            players_service=self.players_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.player_controller)
    container.client_service.add_controller(container.players_controller)

    container.client_service.listen()