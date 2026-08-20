from toga import OptionContainer
from toga.style import Pack

from anime_gui.layout import search_anime


class SearchPage(OptionContainer):
    def __init__(self):
        super().__init__(
            content=[
                ("Search", search_anime()),
            ],
            style=Pack(
                flex=1,
            ),
        )
