# from app.features.market.boxes.history.boxes_history_tab import history_page
# from app.features.market.boxes.listings.boxes_listings_tab import listings_page
# from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case)


def page():
    return Container(
        children=[
            page_title('shopping-cart', 'Marketplace'),
            # summary_row(),
            # tabs_row(BOX_LISTINGS_COLLECTION_NAME,
            #          BOX_HISTORY_COLLECTION_NAME),
        ]
    )


def summary_row():
    # return Container(
    #     context=f"$.{SUMMARY_COLLECTION_NAME}[0]",
    #     children=[
    #         Row([
    #             Col("col-auto", [
    #                 summary_card("common"),
    #             ]),
    #             Col("col-auto", [
    #                 summary_card("premium"),
    #             ]),
    #             Col("col-auto", [
    #                 summary_card("ultra"),
    #             ])
    #         ])
    #     ]
    # )
    return []


def summary_card(boxId):
    return Container(
        context=f"$.{boxId}",
        children=[
            Card(
                class_name="p-1",
                children=[
                    Row([
                        Col("col-auto", [
                            Image(
                                src=switch_case("$.name", "dalarnia_hero"),
                                style={"height": "64px"}
                            )
                        ]),
                        Col("col-auto pr-4", [
                            Span("$.name", "font-medium-3 font-weight-bold d-block"),
                            Span(
                                content=format_template(
                                    "Floor Price: {{ price }}",
                                    {
                                        "price": format_currency("$.floorPrice", "$.fiatSymbol")
                                    }
                                ),
                                class_name="font-small-2 d-block"
                            ),
                            Div(style={"marginBottom": "2px"}),
                            Span(
                                content=format_template(
                                    "24h Avg Price: {{ price }}",
                                    {
                                        "price": format_currency("$.avgPrice", "$.fiatSymbol")
                                    }
                                ),
                                class_name="font-small-2 d-block"
                            )
                        ]),

                    ])
                ])
        ]
    )


def tabs_row(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME):
    # return Tabs(
    #     [
    #         Tab(
    #             label="Listings",
    #             children=[listings_page(LISTINGS_COLLECTION_NAME)]
    #         ),
    #         Tab(
    #             label="History",
    #             children=[history_page(HISTORY_COLLECTION_NAME)]
    #         ),
    #     ]
    # )
    return []