from app.features.profit_tracker.services.profit_tracker_tab import history_page
# from app.features.market.boxes.listings.boxes_listings_tab import listings_page
# from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case)


def page(HISTORY_COLLECTION_NAME):
    return Container(
        children=[
            page_title('shopping-cart', 'Player Profit and Loss'),
            # summary_row(),
            tabs_row(HISTORY_COLLECTION_NAME),
        ]
    )




def tabs_row(HISTORY_COLLECTION_NAME):
    return Tabs(
        [
            Tab(
                label="History",
                children=[history_page(HISTORY_COLLECTION_NAME)]
            ),
        ]
    )
    # return []