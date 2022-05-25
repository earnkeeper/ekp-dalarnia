# from app.utils.game_constants import (HERO_BOX_NAME_CONTRACT,
#                                       HERO_BOX_NAME_IMAGE, MTB_ICON)
from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, collection, commify, documents,
                        format_age, format_currency, format_datetime, format_mask_address,
                        format_template, is_busy, switch_case)


def profit_tracker_tab(HISTORY_COLLECTION_NAME):
    return Container([
        Div([], class_name="mb-2"),
        table_row(HISTORY_COLLECTION_NAME)
    ])


def table_row(HISTORY_COLLECTION_NAME):
    return Datatable(
        data=documents(HISTORY_COLLECTION_NAME),
        busy_when=is_busy(collection(HISTORY_COLLECTION_NAME)),
        default_sort_field_id="timestamp",
        default_sort_asc=False,
        columns=[
            Column(
                id="timestamp",
                sortable=True,
                cell=timestamp_cell(),
                width="200px"
            ),
            Column(
                id="description",
                sortable=True,
                cell=description_cell(),
                searchable=True,
                min_width="400px"
            ),
            Column(
                id="cost_bnb",
                sortable=True,
                right=True,
                cell=price_cell(price="cost_bnb", price_fiat="cost_bnb_fiat")
            ),
            Column(
                id="cost_dar",
                sortable=True,
                right=True,
                cell=price_cell(price="cost_dar", price_fiat="cost_dar_fiat")
            ),
            Column(
                id="revenue_dar",
                sortable=True,
                right=True,
                cell=price_cell(price="revenue_dar", price_fiat="revenue_dar_fiat")
            ),
            Column(
                id="spacer",
                title="",
                width="2px"
            ),
        ]
    )


def timestamp_cell():
    return Row([
        Col(
            class_name="my-auto col-auto pr-0",
            children=[
                Span(format_age("$.timestamp"))
            ]
        ),
        Col(
            class_name="my-auto col-auto pr-0",
            children=[
                Span(format_datetime("$.timestamp"))
            ]
        ),
    ])


def description_cell():
    return Row(
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Span(
                        "$.description"
                    )
                ]
            ),
            Col(
                class_name="col-12",
                children=[
                    Span(
                        format_mask_address("$.transaction_hash")
                    )
                ]
            )

        ]
    )


def price_cell(price, price_fiat):
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency(f"$.{price_fiat}", "$.fiat_symbol"))
            ]
        ),
        Col(
            class_name="col-12 text-right font-small-1",
            children=[
                Row([
                    Col(),
                    Col(
                        class_name="col-auto pl-0 my-auto text-success",
                        children=[
                            Span(commify(f"$.{price}"))
                        ]
                    )
                ])

            ]
        ),
    ])
