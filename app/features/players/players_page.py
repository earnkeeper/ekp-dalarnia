from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Col, Column, Container, Datatable, Div,
                        Form, Image, Input, Row, Span, Tab, Tabs, format_currency, format_template, is_busy,
                        navigate, remove_form_record, commify)


from ekp_sdk.util import collection, documents

def players_page(PLAYERS_COLLECTION_NAME):
    return Container(
        children=[
            page_title('users', 'Players'),
            form_row(),
            table_row(PLAYERS_COLLECTION_NAME)
        ]
    )


def form_row():
    return Form(
        name="dalarnia_player_addresses",
        schema={
            "type": "object",
            "properties": {
                "address": "string"
            },
        },
        multi_record={
            "idField": "address"
        },
        children=[
            Row([
                Col(
                    "col-auto my-auto",
                    [
                        Input(
                            label="Player Address",
                            name="address",
                            style={"minWidth": "240px"}
                        ),
                    ]
                ),
                Col(
                    "col-auto my-auto",
                    [
                        Button(label="Add", is_submit=True)
                    ]
                )
            ])

        ]
    )


def table_row(PLAYERS_COLLECTION_NAME):
    return Datatable(
        default_sort_field_id="id",
        data=documents(PLAYERS_COLLECTION_NAME),
        busy_when=is_busy(collection(PLAYERS_COLLECTION_NAME)),
        on_row_clicked=navigate(
            format_template(
                "player/{{ address }}",
                {
                    "address": "$.id"
                }
            ),
            new_tab=True
        ),
        columns=[
            Column(
                id="id"
            ),
            Column(
                id="cost",
                sortable=True,
                right=True,
                cell=price_cell(price="cost", price_fiat="cost_fiat")
            ),
            Column(
                id="rev",
                sortable=True,
                right=True,
                cell=price_cell(price="rev", price_fiat="rev_fiat")
            ),
            Column(
                id="profit",
                sortable=True,
                right=True,
                cell=price_cell(price="profit", price_fiat="profit_fiat")
            ),
            Column(
                id="actions",
                width="60px",
                title="",
                cell=Button(
                    icon="cil-delete",
                    size='sm',
                    color='flat-primary',
                    on_click=remove_form_record("dalarnia_player_addresses", "address", "$.id"),
                    tooltip="Remove player"
                )
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
        # Col(
        #     class_name="col-12 text-right font-small-1",
        #     children=[
        #         Row([
        #             Col(),
        #             Col(
        #                 class_name="col-auto pl-0 my-auto text-success",
        #                 children=[
        #                     Span(commify(f"$.{price}"))
        #                 ]
        #             )
        #         ])
        #
        #     ]
        # ),
    ])
