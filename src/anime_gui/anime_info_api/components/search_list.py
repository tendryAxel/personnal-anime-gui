import requests
from toga.style import Pack
from toga import Box, Label, Image, ImageView
from kitsu_extended import Anime
from toga.style.pack import COLUMN, ROW


def anime_in_search_result(anime: Anime) -> Box:
    # TODO: make image loading async
    image_url = anime.poster_image("tiny")
    if image_url is not None:
        image_data = requests.get(image_url).content

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

            Box(
                children=[
                    ImageView(
                        Image(image_data),
                        style=Pack(
                            width=180,
                            height=240,
                            margin_right=15,
                        ),
                    ),

                    # Anime information
                    Box(
                        children=[
                            Label(
                                f"⭐ {anime.average_rating or '?'}  •  "
                                f"{anime.subtype or '?'}  •  "
                                f"{anime.episode_count or '?'} episodes  •  "
                                f"{anime.status or '?'}",
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
                        ),
                    ),
                ],
                style=Pack(
                    direction=ROW,
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
