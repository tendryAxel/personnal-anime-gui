from anime_gui.pages.details_page import AnimeDetailPage
from typing import Callable, Any, Coroutine
from toga.style import Pack
from toga import Box, Label, Button
from kitsu_extended import Anime
from toga.style.pack import COLUMN, ROW
from typing import TYPE_CHECKING

from anime_gui.navigation import PageManager
from anime_gui.components.image import LoadImage


class SingleAnimeSearchResult(Box):
    image_component: LoadImage
    pages: PageManager
    anime: Anime

    def __init__(
        self,
        anime: Anime,
        pages: PageManager,
    ):
        self.anime = anime
        self.pages = pages
        self.image_component = LoadImage(
            anime.poster_image("tiny"),
            style=Pack(
                width=180,
                height=240,
                margin_right=15,
            ),
        )

        super().__init__(
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
                        self.image_component,
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

                                Button(
                                    "info",
                                    on_press=self.push_anime_info_details,
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
    
    def start_loading(self) -> None:
        self.image_component.start_loading()
    
    async def push_anime_info_details(self, *args, **kwargs) -> None:
        page_id = f"details-{self.anime.id}"
        detail_page = AnimeDetailPage()

        self.pages.register(
            page_id,
            detail_page,
        )

        if self.app is None:
            raise Exception("Application not set")
        self.app.loop.create_task(detail_page.load(int(self.anime.id)))

        self.pages.show(page_id)

def create_pagination_button(
    on_previous: Callable[[Any], None],
    on_next: Callable[[Any], None],
) -> Box:
    previous_button = Button(
        "← Previous",
        on_press=on_previous,
        style=Pack(
            flex=1,
            margin_right=5,
        ),
    )

    page_label = Label(
        "Page 0",
        style=Pack(
            margin=5,
        ),
    )

    next_button = Button(
        "Next →",
        on_press=on_next,
        style=Pack(
            flex=1,
            margin_left=5,
        ),
    )

    return Box(
        children=[
            previous_button,
            page_label,
            next_button,
        ],
        style=Pack(
            direction=ROW,
            margin_top=10,
    )
)

class PaginationButton(Box):
    page: int
    on_page_change: Callable[[int], Coroutine[None, None, None]]

    def __init__(
        self,
        on_page_change: Callable[[int], Coroutine[None, None, None]],
        page: int = 0,
    ):
        self.page = page
        self.on_page_change = on_page_change

        self.previous_button = Button(
            "← Previous",
            on_press=self.previous,
            style=Pack(
                flex=1,
                margin_right=5,
            ),
        )

        self.page_label = Label(
            f"Page {self.page}",
            style=Pack(
                margin=5,
            ),
        )

        self.next_button = Button(
            "Next →",
            on_press=self.next,
            style=Pack(
                flex=1,
                margin_left=5,
            ),
        )

        super().__init__(
            children=[
                self.previous_button,
                self.page_label,
                self.next_button,
            ],
            style=Pack(
                direction=ROW,
                margin_top=10,
            ),
        )

        self.update_buttons()

    async def previous(self, widget):
        if self.page <= 0:
            return

        self.page -= 1
        await self.update()

    async def next(self, widget):
        self.page += 1
        await self.update()

    async def update(self):
        self.page_label.text = f"Page {self.page}"
        self.update_buttons()

        await self.on_page_change(self.page)

    def update_buttons(self):
        self.previous_button.enabled = self.page > 0
