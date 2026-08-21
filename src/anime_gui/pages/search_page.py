from anime_gui.context import ApplicationContext
from kitsu_extended import Anime
from toga.constants import COLUMN, ROW
from toga import OptionContainer, Box, TextInput, Button, Label, ScrollContainer
from toga.style import Pack

from anime_info_api.main import PageParam
from anime_info_api import anime
from anime_gui.components.search_list import PaginationButton, SingleAnimeSearchResult
from anime_gui.navigation import PageManager


# TODO: reset pagination for new query
class SearchPage(OptionContainer):
    pagination: PageParam
    animes_component: list[SingleAnimeSearchResult]
    context: ApplicationContext

    search_input: TextInput
    search_button: Button
    search_bar: Box
    results: Box
    results_scroll: ScrollContainer
    pagination_button: PaginationButton
    pagination_section: Box
    header: Box
    search_card: Box
    results_header: Label
    search_tab: Box
    
    def __init__(self, context: ApplicationContext):
        # Variables
        self.pagination = PageParam(0, 10)
        self.animes_component = []
        self.context = context

        # Components
        self.search_input = TextInput(
            placeholder="Search for an anime...",
            style=Pack(
                flex=1,
                padding=8,
            ),
        )

        self.search_button = Button(
            "Search",
            on_press=self.on_search,
            style=Pack(
                width=100,
                padding=8,
            ),
        )

        self.search_bar = Box(
            children=[
                self.search_input,
                self.search_button,
            ],
            style=Pack(
                direction=ROW,
                gap=8,
                padding=12,
            ),
        )

        self.results = Box(
            style=Pack(
                direction=COLUMN,
                padding=5,
            ),
        )

        self.results_scroll = ScrollContainer(
            content=self.results,
            horizontal=False,
            vertical=True,
            style=Pack(
                flex=1,
            ),
        )

        self.pagination_button = PaginationButton(
            on_page_change=self.on_change_page,
        )

        self.pagination_section = Box(
            children=[
                self.pagination_button,
            ],
            style=Pack(
                direction=ROW,
                padding_top=10,
                padding_bottom=5,
                align_items="center",
            ),
        )

        self.header = Box(
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

        self.search_card = Box(
            children=[
                self.search_bar,
            ],
            style=Pack(
                direction=COLUMN,
                padding_bottom=10,
            ),
        )

        self.results_header = Label(
            "Search results",
            style=Pack(
                font_size=16,
                padding_top=5,
                padding_bottom=8,
            ),
        )

        # Tab creation
        self.search_tab = Box(
            children=[
                self.header,
                self.search_card,
                self.results_header,
                self.results_scroll,
                self.pagination_section,
            ],
            style=Pack(
                direction=COLUMN,
                padding=20,
                flex=1,
            ),
        )

        super().__init__(
            content=[
                ("Search", self.search_tab),
            ],
            style=Pack(
                flex=1,
            ),
        )

    async def on_search(self, widget=None):
        animes = await anime.find_by_name(
            self.search_input.value,
            self.pagination,
        )

        self.build_anime_list(animes)
        self.reload_anime()

        for element in self.animes_component:
            element.start_loading()
    
    def build_anime_list(self, animes: list[Anime] | None) -> None:
        self.animes_component.clear()

        if animes is None:
            return

        for anime in animes:
            self.animes_component.append(
                SingleAnimeSearchResult(
                    anime,
                    self.context,
                )
            )

    def reload_anime(self) -> None:
        self.results.clear()

        if len(self.animes_component) == 0:
            self.results.add(
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

        for anime in self.animes_component:
            result = Box(
                children=[
                    anime,
                ],
                style=Pack(
                    direction=COLUMN,
                    padding=10,
                    margin_bottom=8,
                ),
            )

            self.results.add(result)

    async def on_change_page(self, page: int):
        self.pagination.page_number = page
        await self.on_search()
