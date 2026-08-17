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

def search_anime(app: toga.App) -> toga.Box:
    search_input = toga.TextInput(
        placeholder="Search for an anime...",
        style=Pack(
            flex=1,
            padding=5,
        ),
    )

    async def on_search(widget):
        query = search_input.value
        animes = await anime_gui.anime_info_api.anime.find_by_name(query)

        results.clear()
        for anime in animes:
            result = toga.Label(
                f"Id: {anime.id} Name: {anime.title}",
                style=Pack(
                    padding=10,
                ),
            )
            results.add(result)

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
            results,
        ],
        style=Pack(
            direction=COLUMN,
            padding=20,
            flex=1,
        ),
    )
