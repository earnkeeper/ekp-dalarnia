from app.features.profit_tracker.services.profit_tracker_tab import history_page
# from app.features.market.boxes.listings.boxes_listings_tab import listings_page
# from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from ekp_sdk.util.clean_null_terms import clean_null_terms
from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case, Avatar)


def page(HISTORY_COLLECTION_NAME, SUMMARY_COLLECTION_NAME):
    return Container(
        children=[
            page_title('shopping-cart', 'Player Profit and Loss'),
            summary_row(SUMMARY_COLLECTION_NAME),
            tabs_row(HISTORY_COLLECTION_NAME),
        ]
    )


def summary_row(SUMMARY_COLLECTION_NAME):
    return Container(
        context=f"$.{SUMMARY_COLLECTION_NAME}[0]",
        children=[
            Row([
                Col("col-auto", [
                    summary_card("total_bnb_cost"),
                ]),
                Col("col-auto", [
                    summary_card("total_dar_cost"),
                ]),
                Col("col-auto", [
                    summary_card("total_dar_revenue"),
                ]),
                Col("col-auto", [
                    summary_card("profit_to_date"),
                ])
            ])
        ]
    )


def summary_card(boxId):
    return Container(
        context=f"$.{boxId}",
        children=[
            Card(
                class_name="p-1",
                children=[
                    Row([
                        Col("col-auto", [
                            Avatar(
                                icon="avard",
                                size="sm",
                            )
                        ]),
                        Col("col-auto pr-4", [
                            Span("$.name", "font-medium-3 font-weight-bold d-block"),
                            Span(
                                content=format_template(
                                    "Total Price: {{ price }}",
                                    {
                                        "price": format_currency("$.total_price", "$.fiatSymbol")
                                    }
                                ),
                                class_name="font-small-2 d-block"
                            ),
                            Div(style={"marginBottom": "2px"})
                        ]),

                    ])
                ])
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
