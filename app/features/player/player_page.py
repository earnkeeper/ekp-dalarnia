from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs, Button,
                        format_currency, format_template, Input, Avatar, Form, Link, format_mask_address)
from app.features.player.transactions_table import transactions_table
from app.utils.page_title import page_title


def player_page(TRANSACTIONS_COLLECTION_NAME, SUMMARY_COLLECTION_NAME):
    return Container(
        children=[
            page_title('shopping-cart', 'Player Profit and Loss'),
            player_address(SUMMARY_COLLECTION_NAME),
            Div(style={"marginBottom": "10px"}),
            summary_row(SUMMARY_COLLECTION_NAME),
            transactions_table(TRANSACTIONS_COLLECTION_NAME)
        ]
    )


def player_address(SUMMARY_COLLECTION_NAME):
    return Container(
        context=f"$.{SUMMARY_COLLECTION_NAME}[0]",
        children=[
            Link(
                content=format_mask_address("$.id"),
                class_name="d-block font-small-2",
                external_icon=True,
                external=True,
                href=format_template(
                    "https://bscscan.com/address/{{ address }}",
                    {
                        "address": "$.id"
                    }
                )
            ),
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
                        Col("col-auto my-auto pr-0", [
                            Avatar(
                                icon="award",
                                size="sm",
                            )
                        ]),
                        Col("col-auto pr-4", [
                            Span("$.name", "font-medium-3 font-weight-bold d-block"),
                            Span(
                                content=format_template(
                                    "{{ price }}",
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
