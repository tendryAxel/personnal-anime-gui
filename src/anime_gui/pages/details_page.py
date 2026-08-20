from __future__ import annotations
from anime_gui.components.image import LoadImage

from typing import Optional

import toga
import toga.style

from kitsu_extended import Anime

from anime_gui.anime_info_api.anime import get_by_id


class AnimeDetailPage(toga.Box):
    """Page displaying the details of an anime."""

    anime_id: Optional[int]
    anime: Optional[Anime]

    def __init__(
        self,
        *,
        style: toga.style.Pack | None = None,
        id: str | None = None,
        **kwargs,
    ):
        self.anime_id = None
        self.anime = None

        super().__init__(
            style=toga.style.Pack(
                direction="column",
                flex=1,
                **(style.__dict__ if style else {}),
            ),
            id=id,
            **kwargs,
        )

        self._build_empty()

    async def load(self, anime_id: int) -> None:
        """Load and display an anime asynchronously."""
        self.anime_id = anime_id
        self.anime = None

        self._build_loading()

        try:
            anime = await get_by_id(anime_id)

            self.anime = anime
            self._build_anime(anime)

        except Exception as exc:
            self._build_error(exc)

    def _build_empty(self) -> None:
        self.clear()

        self.add(
            toga.Box(
                children=[
                    toga.Label(
                        "Nothing to find.",
                        style=toga.style.Pack(
                            font_size=20,
                            font_weight="bold",
                            padding=20,
                        ),
                    ),
                    toga.Label(
                        "Select an anime to see its details.",
                        style=toga.style.Pack(
                            padding=20,
                        ),
                    ),
                ],
                style=toga.style.Pack(
                    direction="column",
                    alignment="center",
                    flex=1,
                ),
            )
        )

    def _build_loading(self) -> None:
        self.clear()

        self.add(
            toga.Box(
                children=[
                    toga.Label(
                        "Loading anime...",
                        style=toga.style.Pack(
                            padding=20,
                        ),
                    ),
                ],
                style=toga.style.Pack(
                    direction="column",
                    alignment="center",
                    flex=1,
                ),
            )
        )

    def _build_anime(self, anime: Anime) -> None:
        self.clear()

        poster = LoadImage(
            anime.poster_image("small"),
            style=toga.style.Pack(
                width=220,
                height=330,
            ),
        )

        title = toga.Label(
            anime.title or "Nothing",
            style=toga.style.Pack(
                font_size=24,
                font_weight="bold",
                padding_bottom=10,
            ),
        )

        description = toga.Label(
            anime.synopsis or "No synopsis available.",
            style=toga.style.Pack(
                padding_bottom=20,
            ),
        )

        content = toga.Box(
            children=[
                poster,
                toga.Box(
                    children=[
                        title,
                        description,
                    ],
                    style=toga.style.Pack(
                        direction="column",
                        flex=1,
                        padding_left=20,
                    ),
                ),
            ],
            style=toga.style.Pack(
                direction="row",
                padding=20,
                flex=1,
            ),
        )

        self.add(content)

    def _build_error(self, error: Exception) -> None:
        self.clear()

        self.add(
            toga.Box(
                children=[
                    toga.Label(
                        "Unable to load anime.",
                        style=toga.style.Pack(
                            font_size=20,
                            font_weight="bold",
                            padding_bottom=10,
                        ),
                    ),
                    toga.Label(
                        str(error),
                        style=toga.style.Pack(
                            padding_bottom=20,
                        ),
                    ),
                    toga.Button(
                        "Retry",
                        on_press=self._retry,
                    ),
                ],
                style=toga.style.Pack(
                    direction="column",
                    alignment="center",
                    flex=1,
                    padding=20,
                ),
            )
        )

    async def _retry(self, widget: toga.Widget) -> None:
        if self.anime_id is not None:
            await self.load(self.anime_id)