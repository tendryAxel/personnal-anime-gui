from kitsu_extended import Anime
from toga.constants import COLUMN, ROW
from toga import OptionContainer, Box, TextInput, Button, Label, ScrollContainer
from toga.style import Pack

from anime_info_api.main import PageParam
from anime_info_api import anime
from anime_gui.components.search_list import anime_in_search_result, PaginationButton


class SearchPage(OptionContainer):
    def __init__(self):
        super().__init__(
            content=[
                ("Search", self.search_anime()),
            ],
            style=Pack(
                flex=1,
            ),
        )
    
    def search_anime(self) -> Box:
        actual_page = PageParam(0, 10)

        # ---------------------------------------------------------
        # Search input
        # ---------------------------------------------------------

        search_input = TextInput(
            placeholder="Search for an anime...",
            style=Pack(
                flex=1,
                padding=8,
            ),
        )

        async def on_search(widget=None):
            animes = await anime.find_by_name(
                search_input.value,
                actual_page,
            )

            reload_anime(animes)

        search_button = Button(
            "Search",
            on_press=on_search,
            style=Pack(
                width=100,
                padding=8,
            ),
        )

        search_bar = Box(
            children=[
                search_input,
                search_button,
            ],
            style=Pack(
                direction=ROW,
                gap=8,
                padding=12,
            ),
        )

        # ---------------------------------------------------------
        # Results
        # ---------------------------------------------------------

        results = Box(
            style=Pack(
                direction=COLUMN,
                padding=5,
            ),
        )

        def reload_anime(animes: list[Anime]) -> None:
            results.clear()

            if not animes:
                results.add(
                    Box(
                        children=[
                            Label(
                                "No anime found.",
                                style=Pack(
                                    padding=30,
                                    text_align="center",
                                ),
                            ),
                        ],
                        style=Pack(
                            direction=COLUMN,
                            align_items="center",
                        ),
                    )
                )
                return

            for anime in animes:
                result = Box(
                    children=[
                        anime_in_search_result(anime),
                    ],
                    style=Pack(
                        direction=COLUMN,
                        padding=10,
                        margin_bottom=8,
                    ),
                )

                results.add(result)

        results_scroll = ScrollContainer(
            content=results,
            horizontal=False,
            vertical=True,
            style=Pack(
                flex=1,
            ),
        )

        # ---------------------------------------------------------
        # Pagination
        # ---------------------------------------------------------

        async def on_change_page(page: int):
            actual_page.page_number = page
            await on_search()

        pagination_button = PaginationButton(
            on_page_change=on_change_page,
        )

        pagination = Box(
            children=[
                pagination_button,
            ],
            style=Pack(
                direction=ROW,
                padding_top=10,
                padding_bottom=5,
                align_items="center",
            ),
        )

        # ---------------------------------------------------------
        # Main layout
        # ---------------------------------------------------------

        header = Box(
            children=[
                Label(
                    "Anime Explorer",
                    style=Pack(
                        font_size=24,
                        padding_bottom=3,
                    ),
                ),
                Label(
                    "Search and discover your favorite anime",
                    style=Pack(
                        padding_bottom=15,
                    ),
                ),
            ],
            style=Pack(
                direction=COLUMN,
            ),
        )

        search_card = Box(
            children=[
                search_bar,
            ],
            style=Pack(
                direction=COLUMN,
                padding_bottom=10,
            ),
        )

        results_header = Label(
            "Search results",
            style=Pack(
                font_size=16,
                padding_top=5,
                padding_bottom=8,
            ),
        )

        return Box(
            children=[
                header,
                search_card,
                results_header,
                results_scroll,
                pagination,
            ],
            style=Pack(
                direction=COLUMN,
                padding=20,
                flex=1,
            ),
        )

