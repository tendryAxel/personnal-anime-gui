import toga
from toga.style import Pack
from toga.style.pack import COLUMN


def create_tab(app) -> toga.Box:
    items = [
        "Apple",
        "Banana",
        "Orange",
        "Mango",
        "Pineapple",
    ]

    list_view = toga.Selection(items=items)

    return toga.Box(
        children=[
            toga.Label(
                "My List",
                style=Pack(
                    padding=10,
                    font_size=20,
                ),
            ),
            list_view,
        ],
        style=Pack(
            direction=COLUMN,
            padding=10,
        ),
    )
