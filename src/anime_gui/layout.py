from kitsu_extended import Anime, Client
from anime_gui.anime_info_api.main import PageParam
from anime_gui.anime_info_api.components.search_list import anime_in_search_result, create_pagination_button, PaginationButton
import anime_gui.anime_info_api.anime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


# TODO: convert to class
def search_anime(app: toga.App) -> toga.Box:
    actual_page = PageParam(0, 10)

    # ---------------------------------------------------------
    # Search input
    # ---------------------------------------------------------

    search_input = toga.TextInput(
        placeholder="Search for an anime...",
        style=Pack(
            flex=1,
            padding=8,
        ),
    )

    async def on_search(widget=None):
        animes = await anime_gui.anime_info_api.anime.find_by_name(
            search_input.value,
            actual_page,
        )

        reload_anime(animes)

    search_button = toga.Button(
        "Search",
        on_press=on_search,
        style=Pack(
            width=100,
            padding=8,
        ),
    )

    search_bar = toga.Box(
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

    results = toga.Box(
        style=Pack(
            direction=COLUMN,
            padding=5,
        ),
    )

    def reload_anime(animes: list[Anime]) -> None:
        results.clear()

        if not animes:
            results.add(
                toga.Box(
                    children=[
                        toga.Label(
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
            result = toga.Box(
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

    results_scroll = toga.ScrollContainer(
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

    pagination = toga.Box(
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

    header = toga.Box(
        children=[
            toga.Label(
                "Anime Explorer",
                style=Pack(
                    font_size=24,
                    padding_bottom=3,
                ),
            ),
            toga.Label(
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

    search_card = toga.Box(
        children=[
            search_bar,
        ],
        style=Pack(
            direction=COLUMN,
            padding_bottom=10,
        ),
    )

    results_header = toga.Label(
        "Search results",
        style=Pack(
            font_size=16,
            padding_top=5,
            padding_bottom=8,
        ),
    )

    return toga.Box(
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
