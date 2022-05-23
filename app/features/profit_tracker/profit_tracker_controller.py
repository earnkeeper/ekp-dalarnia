# from app.features.market.boxes.boxes_summary_service import BoxesSummaryService
# from app.features.market.boxes.history.boxes_history_service import \
#     BoxesHistoryService
# from app.features.market.boxes.listings.boxes_listings_service import \
#     BoxesListingsService
from app.features.profit_tracker.profit_tracker_page import page
from app.features.profit_tracker.services.profit_tracker_service import ProfitTrackerService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

PLAYERS_HISTORY_COLLECTION_NAME = "market_transactions"
# BOX_LISTINGS_COLLECTION_NAME = "metabomb_box_listings"
# BOX_HISTORY_COLLECTION_NAME = "metabomb_box_history"
# BOX_SUMMARY_COLLECTION_NAME = "metabomb_box_summary"


class ProfitTrackerController:
    def __init__(
        self,
        client_service: ClientService,
        profit_tracker_service: ProfitTrackerService
        # boxes_listings_service: BoxesListingsService,
        # boxes_history_service: BoxesHistoryService,
        # boxes_summary_service: BoxesSummaryService
    ):
        self.client_service = client_service
        self.profit_tracker_service = profit_tracker_service
        self.path = 'profit_tracker'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'cil-cart',
            'Profit Tracker',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(PLAYERS_HISTORY_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, PLAYERS_HISTORY_COLLECTION_NAME)
        # await self.client_service.emit_busy(sid, BOX_HISTORY_COLLECTION_NAME)
        # await self.client_service.emit_busy(sid, BOX_SUMMARY_COLLECTION_NAME)

        currency = client_currency(event)

        # History
        history_documents = await self.profit_tracker_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            PLAYERS_HISTORY_COLLECTION_NAME,
            history_documents
        )

        # Listings

        # listing_documents = await self.boxes_listings_service.get_documents(currency, history_documents)
        #
        # await self.client_service.emit_documents(
        #     sid,
        #     BOX_LISTINGS_COLLECTION_NAME,
        #     listing_documents
        # )
        #
        # # Summary
        #
        # summary_documents = self.boxes_summary_service.get_documents(
        #     listing_documents, history_documents, currency)
        #
        # await self.client_service.emit_documents(
        #     sid,
        #     BOX_SUMMARY_COLLECTION_NAME,
        #     summary_documents
        # )

        await self.client_service.emit_done(sid, PLAYERS_HISTORY_COLLECTION_NAME)
