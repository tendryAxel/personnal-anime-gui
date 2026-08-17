from toga.style import Pack
from toga import Box, Label
from kitsu_extended import Anime
from toga.style.pack import COLUMN


def anime_in_search_result(anime: Anime) -> Box:
    return Box(
        children=[
            Label(
                anime.title or "",
                style=Pack(
                    font_size=18,
                    font_weight="bold",
                    margin_bottom=5,
                ),
            ),
            Label(
                f"⭐ {anime.average_rating}  •  "
                f"{anime.subtype}  •  "
                f"{anime.episode_count or '?'} episodes  •  "
                f"{anime.status}",
                style=Pack(
                    margin_bottom=8,
                ),
            ),
            Label(
                anime.synopsis or "No synopsis available.",
                style=Pack(
                    flex=1,
                ),
            ),
        ],
        style=Pack(
            direction=COLUMN,
            flex=1,
            margin=10,
        ),
    )
