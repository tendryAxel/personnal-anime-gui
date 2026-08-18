from kitsu_extended import Anime, Client
from anime_gui.anime_info_api.main import PageParam
from anime_gui.anime_info_api.components.search_list import anime_in_search_result, create_pagination_button, PaginationButton
import anime_gui.anime_info_api.anime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


def create_tab(app: toga.App, items: list[str]) -> toga.Box:
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

# TODO: convert to class
def search_anime(app: toga.App) -> toga.Box:
    actual_page = PageParam(0, 10)

    search_input = toga.TextInput(
        placeholder="Search for an anime...",
        style=Pack(
            flex=1,
            padding=5,
        ),
    )

    def reload_anime(animes: list[Anime]) -> None:
        results.clear()
        for anime in animes:
            results.add(
                toga.Box(
                    children=[
                        anime_in_search_result(anime),
                    ],
                    style=Pack(
                        direction=ROW,
                        margin_bottom=10,
                    ),
                )
            )

    async def on_search(*arg):
        animes = await anime_gui.anime_info_api.anime.find_by_name(
            search_input.value,
            actual_page,
        )

        reload_anime(animes)
    
    async def on_change_page(a: int):        
        actual_page.page_number = a
        await on_search(None)

    search_button = toga.Button(
        "Search",
        style=Pack(
            padding=5,
            width=100,
        ),
        on_press=on_search,
    )

    search_bar = toga.Box(
        children=[
            search_input,
            search_button,
        ],
        style=Pack(
            direction=ROW,
            padding_bottom=10,
        ),
    )

    results = toga.Box(
        style=Pack(
            direction=COLUMN,
            flex=1,
            padding_top=10,
        ),
    )

    results_scroll = toga.ScrollContainer(
        content=results,
        horizontal=False,
        vertical=True,
        style=Pack(
            flex=1,
        ),
    )

    pagination_button = PaginationButton(on_page_change=on_change_page)

    return toga.Box(
        children=[
            toga.Label(
                "Search Anime",
                style=Pack(
                    font_size=20,
                    padding_bottom=10,
                ),
            ),
            search_bar,
            results_scroll,
            pagination_button,
        ],
        style=Pack(
            direction=COLUMN,
            padding=20,
            flex=1,
        ),
    )
