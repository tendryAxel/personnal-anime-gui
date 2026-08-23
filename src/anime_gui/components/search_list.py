from typing import Callable, Any, Coroutine
from toga.style import Pack
from toga import Box, Label, Button
from kitsu_extended import Anime
from toga.style.pack import COLUMN, ROW

from anime_gui.context import ApplicationContext
from anime_gui.pages.details_page import AnimeDetailPage
from anime_gui.components.image import LoadImage


class SingleAnimeSearchResult(Box):
    image_component: LoadImage
    context: ApplicationContext
    anime: Anime

    MAX_DESCRIPTION_LENGTH = 100

    def __init__(
        self,
        anime: Anime,
        context: ApplicationContext,
    ):
        self.anime = anime
        self.context = context

        self.image_component = LoadImage(
            anime.poster_image("tiny"),
            style=Pack(
                width=150,
                height=220,
                margin_right=15,
            ),
        )

        title = Label(
            anime.title or "Unknown title",
            style=Pack(
                font_size=18,
                font_weight="bold",
                padding_bottom=8,
            ),
        )

        metadata = Label(
            f"⭐ {anime.average_rating or '?'}  •  "
            f"{anime.subtype or '?'}  •  "
            f"{anime.episode_count or '?'} episodes  •  "
            f"{anime.status or '?'}",
            style=Pack(
                padding_bottom=8,
            ),
        )

        description = Label(
            self._truncate_description(anime.synopsis or "No synopsis available."),
            style=Pack(
                flex=1,
                padding_bottom=10,
            ),
        )

        info_button = Button(
            "Info",
            on_press=self.push_anime_info_details,
            style=Pack(
                width=90,
                padding=6,
            ),
        )

        text_content = Box(
            children=[
                title,
                metadata,
                description,
                info_button,
            ],
            style=Pack(
                direction=COLUMN,
                flex=1,
                padding=5,
            ),
        )

        content = Box(
            children=[
                self.image_component,
                text_content,
            ],
            style=Pack(
                direction=ROW,
                flex=1,
            ),
        )

        super().__init__(
            children=[
                content,
            ],
            style=Pack(
                direction=COLUMN,
                flex=1,
                margin=10,
            ),
        )

    @classmethod
    def _truncate_description(
        cls,
        description: str,
    ) -> str:
        description = " ".join(description.split())

        if len(description) <= cls.MAX_DESCRIPTION_LENGTH:
            return description

        return description[: cls.MAX_DESCRIPTION_LENGTH].rsplit(" ", 1)[0] + "..."

    def start_loading(self) -> None:
        self.image_component.start_loading()

    async def push_anime_info_details(
        self,
        *args,
        **kwargs,
    ) -> None:
        page_id = f"details-{self.anime.id}"

        detail_page = AnimeDetailPage(self.context)

        self.context.page_manager.register(
            page_id,
            detail_page,
        )

        if self.app is None:
            raise Exception("Application not set")

        self.context.page_manager.show(page_id)

        self.app.loop.create_task(detail_page.load(int(self.anime.id)))


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
