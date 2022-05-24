from decouple import AutoConfig
from ekp_sdk import BaseContainer
# from app.features.dashboard.dashboard_controller import DashboardController
# from app.features.dashboard.dashboard_opens_service import DashboardOpensService

# from app.features.market.market_controller import MarketController
from app.features.profit_tracker.profit_tracker_controller import ProfitTrackerController
from app.features.profit_tracker.services.profit_tracker_service import ProfitTrackerService
from app.features.profit_tracker.services.summary.players_summary_service import PlayersSummaryService
# from app.features.market.boxes.history.boxes_history_service import BoxesHistoryService
# from app.features.market.boxes.listings.boxes_listings_service import BoxesListingsService
# from app.features.market.boxes.boxes_summary_service import BoxesSummaryService
# from db.dalarnia_transactions_repo import BoxOpensRepo
from db.dalarnia_transactions_repo import MarketTransactionsRepo


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        # DB

        # self.box_opens_repo = BoxOpensRepo(
        #     mg_client=self.mg_client,
        # )

        self.market_transactions_repo = MarketTransactionsRepo(
            mg_client=self.mg_client,
        )

        # FEATURES - MARKET

        self.profit_tracker_service = ProfitTrackerService(
            coingecko_service=self.coingecko_service,
            market_transactions_repo=self.market_transactions_repo
        )

        # self.market_listings_service = BoxesListingsService(
        #     coingecko_service=self.coingecko_service
        # )
        #
        # self.market_history_service = BoxesHistoryService(
        #     market_transactions_repo=self.market_transactions_repo,
        #     coingecko_service=self.coingecko_service
        # )

        self.player_summary_service = PlayersSummaryService(
            market_transactions_repo=self.market_transactions_repo,
            coingecko_service=self.coingecko_service
        )

        self.market_controller = ProfitTrackerController(
            client_service=self.client_service,
            profit_tracker_service=self.profit_tracker_service,
            players_summary_service=self.player_summary_service
            # boxes_listings_service=self.market_listings_service,
            # boxes_history_service=self.market_history_service,
            # boxes_summary_service=self.market_summary_service
        )

        # FEATURES - DASHBOARD

        # self.dashboard_opens_service = DashboardOpensService(
        #     box_opens_repo=self.box_opens_repo
        # )
        #
        # self.dashboard_controller = DashboardController(
        #     client_service=self.client_service,
        #     dashboard_opens_service=self.dashboard_opens_service,
        # )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.market_controller)
    # container.client_service.add_controller(container.dashboard_controller)

    container.client_service.listen()