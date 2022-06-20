from ekp_sdk.ui import Col, Icon, Row, Span, navigate


def page_title(icon, title):
    return Row(
        children=[
            Col(
                "col-auto my-auto pr-0",
                [
                    Icon('chevron-left', size='lg',
                         on_click=navigate("players"))
                ]),
            Col(
                class_name='col-auto pr-0 my-auto',
                children=[
                    Icon(
                        size="lg",
                        name="user"
                    )
                ],
            ),
            Col(
                class_name="my-auto",
                children=[
                    Span(title, "font-large-1")
                ]
            ),
        ],
        class_name="mb-2"
    )