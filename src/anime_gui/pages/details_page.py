from __future__ import annotations
from anime_gui.context import ApplicationContext
from toga.style.pack import COLUMN, ROW
from typing import Optional
import toga
import toga.style

from anime_info_api.anime import get_by_id
from anime_gui.components.image import LoadImage
from kitsu_extended import Anime


class AnimeDetailPage(toga.Box):
    """Page displaying the details of an anime."""

    anime_id: Optional[int]
    anime: Optional[Anime]
    context: ApplicationContext

    def __init__(
        self,
        context: ApplicationContext,
        *,
        style: toga.style.Pack | None = None,
        id: str | None = None,
        **kwargs,
    ):
        self.anime_id = None
        self.anime = None
        self.context = context

        super().__init__(
            style=toga.style.Pack(
                direction=COLUMN,
                flex=1,
                **(style.__dict__ if style else {}),
            ),
            id=id,
            **kwargs,
        )

        self._build_empty()

    # =========================================================
    # PUBLIC API
    # =========================================================

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

    # =========================================================
    # PAGE BUILDERS
    # =========================================================

    def _build_empty(self) -> None:
        """Display the empty state."""

        self.clear()

        self.add(
            toga.Box(
                children=[
                    toga.Label(
                        "Nothing to find.",
                        style=toga.style.Pack(
                            font_size=20,
                            font_weight="bold",
                            padding_bottom=10,
                        ),
                    ),
                    toga.Label(
                        "Select an anime to see its details.",
                    ),
                ],
                style=toga.style.Pack(
                    direction=COLUMN,
                    alignment="center",
                    flex=1,
                    padding=20,
                ),
            )
        )

    def _build_loading(self) -> None:
        """Display the loading state."""

        self.clear()

        self.add(
            toga.Box(
                children=[
                    toga.Label(
                        "Loading anime...",
                        style=toga.style.Pack(
                            font_size=20,
                            font_weight="bold",
                            padding_bottom=10,
                        ),
                    ),
                    toga.Label(
                        "Please wait.",
                    ),
                ],
                style=toga.style.Pack(
                    direction=COLUMN,
                    alignment="center",
                    flex=1,
                    padding=20,
                ),
            )
        )

    def _build_anime(self, anime: Anime) -> None:
        """Build the anime details page."""

        self.clear()

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        back_button = toga.Button(
            "← Back",
            on_press=self._go_back,
            style=toga.style.Pack(
                padding=8,
            ),
        )

        refresh_button = toga.Button(
            "↻",
            on_press=self._refresh,
            style=toga.style.Pack(
                width=45,
                padding=8,
            ),
        )

        header = toga.Box(
            children=[
                back_button,

                toga.Box(
                    children=[],
                    style=toga.style.Pack(
                        flex=1,
                    ),
                ),

                refresh_button,
            ],
            style=toga.style.Pack(
                direction=ROW,
                padding=10,
            ),
        )

        # -----------------------------------------------------
        # Poster
        # -----------------------------------------------------

        poster = LoadImage(
            anime.poster_image("small"),
            style=toga.style.Pack(
                width=220,
                height=330,
            ),
        )

        # -----------------------------------------------------
        # Basic information
        # -----------------------------------------------------

        title = toga.Label(
            anime.title or "Unknown title",
            style=toga.style.Pack(
                font_size=26,
                font_weight="bold",
                padding_bottom=8,
            ),
        )

        subtitle = toga.Label(
            self._get_subtitle(anime),
            style=toga.style.Pack(
                padding_bottom=15,
            ),
        )

        # -----------------------------------------------------
        # Action buttons
        # -----------------------------------------------------

        favorite_button = toga.Button(
            "♡ Favorite",
            on_press=self._toggle_favorite,
            style=toga.style.Pack(
                padding=7,
            ),
        )

        watchlist_button = toga.Button(
            "+ Watchlist",
            on_press=self._add_to_watchlist,
            style=toga.style.Pack(
                padding=7,
            ),
        )

        trailer_button = toga.Button(
            "▶ Trailer",
            on_press=self._open_trailer,
            style=toga.style.Pack(
                padding=7,
            ),
        )

        share_button = toga.Button(
            "↗ Share",
            on_press=self._share,
            style=toga.style.Pack(
                padding=7,
            ),
        )

        actions = toga.Box(
            children=[
                favorite_button,
                watchlist_button,
                trailer_button,
                share_button,
            ],
            style=toga.style.Pack(
                direction=ROW,
                padding_bottom=15,
            ),
        )

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        metadata = self._build_metadata(anime)

        # -----------------------------------------------------
        # Synopsis
        # -----------------------------------------------------

        synopsis_title = toga.Label(
            "Synopsis",
            style=toga.style.Pack(
                font_size=18,
                font_weight="bold",
                padding_bottom=7,
            ),
        )

        synopsis = toga.Label(
            anime.synopsis or "No synopsis available.",
            style=toga.style.Pack(
                padding_bottom=20,
            ),
        )

        # -----------------------------------------------------
        # Genres
        # -----------------------------------------------------

        genres = self._build_genres(anime)

        # -----------------------------------------------------
        # Information panel
        # -----------------------------------------------------

        information = toga.Box(
            children=[
                title,
                subtitle,
                actions,
                metadata,
                synopsis_title,
                synopsis,
                genres,
            ],
            style=toga.style.Pack(
                direction=COLUMN,
                flex=1,
                padding_left=25,
            ),
        )

        # -----------------------------------------------------
        # Hero section
        # -----------------------------------------------------

        hero = toga.Box(
            children=[
                poster,
                information,
            ],
            style=toga.style.Pack(
                direction=ROW,
                padding=20,
            ),
        )

        # -----------------------------------------------------
        # Additional sections
        # -----------------------------------------------------

        additional = self._build_additional_information(anime)

        content = toga.Box(
            children=[
                hero,
                additional,
            ],
            style=toga.style.Pack(
                direction=COLUMN,
                padding_bottom=20,
            ),
        )

        scroll = toga.ScrollContainer(
            content=content,
            horizontal=False,
            vertical=True,
            style=toga.style.Pack(
                flex=1,
            ),
        )

        self.add(header)
        self.add(scroll)

    # =========================================================
    # COMPONENT BUILDERS
    # =========================================================

    def _build_metadata(self, anime: Anime) -> toga.Box:
        """Build the anime metadata section."""

        metadata = toga.Box(
            style=toga.style.Pack(
                direction=COLUMN,
                padding_bottom=15,
            )
        )

        # Keep these as placeholders for now.
        #
        # Depending on the actual Anime object from kitsu_extended,
        # you can replace these with real attributes.

        metadata.add(
            toga.Label(
                "⭐ Rating: —",
                style=toga.style.Pack(
                    padding_bottom=4,
                ),
            )
        )

        metadata.add(
            toga.Label(
                "📺 Episodes: —",
                style=toga.style.Pack(
                    padding_bottom=4,
                ),
            )
        )

        metadata.add(
            toga.Label(
                "🎬 Type: —",
                style=toga.style.Pack(
                    padding_bottom=4,
                ),
            )
        )

        metadata.add(
            toga.Label(
                "📅 Status: —",
                style=toga.style.Pack(
                    padding_bottom=4,
                ),
            )
        )

        metadata.add(
            toga.Label(
                "⏱ Duration: —",
                style=toga.style.Pack(
                    padding_bottom=4,
                ),
            )
        )

        return metadata

    def _build_genres(self, anime: Anime) -> toga.Box:
        """Build the genres section."""

        container = toga.Box(
            style=toga.style.Pack(
                direction=COLUMN,
                padding_bottom=20,
            )
        )

        container.add(
            toga.Label(
                "Genres",
                style=toga.style.Pack(
                    font_size=18,
                    font_weight="bold",
                    padding_bottom=7,
                ),
            )
        )

        # TODO:
        # Get genres from the Anime object and create buttons/labels.
        #
        # Example:
        #
        # for genre in anime.genres:
        #     container.add(
        #         toga.Label(
        #             genre.name,
        #             style=toga.style.Pack(
        #                 padding_right=8,
        #             ),
        #         )
        #     )

        container.add(
            toga.Label(
                "No genres available.",
            )
        )

        return container

    def _build_additional_information(
        self,
        anime: Anime,
    ) -> toga.Box:
        """Build additional anime information."""

        container = toga.Box(
            children=[
                toga.Label(
                    "More information",
                    style=toga.style.Pack(
                        font_size=18,
                        font_weight="bold",
                        padding_bottom=10,
                    ),
                ),
                toga.Label(
                    "Studios: —",
                    style=toga.style.Pack(
                        padding_bottom=5,
                    ),
                ),
                toga.Label(
                    "Original title: —",
                    style=toga.style.Pack(
                        padding_bottom=5,
                    ),
                ),
                toga.Label(
                    "Aired: —",
                    style=toga.style.Pack(
                        padding_bottom=5,
                    ),
                ),
                toga.Label(
                    "Source: —",
                    style=toga.style.Pack(
                        padding_bottom=5,
                    ),
                ),
            ],
            style=toga.style.Pack(
                direction=COLUMN,
                padding_left=20,
                padding_right=20,
                padding_bottom=20,
            ),
        )

        return container

    # =========================================================
    # HELPERS
    # =========================================================

    def _get_subtitle(self, anime: Anime) -> str:
        """Return a small subtitle for the anime."""

        # TODO:
        # Add alternative title / Japanese title here.

        return "Anime details"

    # =========================================================
    # NAVIGATION
    # =========================================================

    async def _go_back(self, widget: toga.Widget) -> None:
        """Go back to the previous page."""

        self.context.page_manager.back()

    # =========================================================
    # ACTIONS
    # =========================================================

    async def _toggle_favorite(self, widget: toga.Widget) -> None:
        """Add/remove the anime from favorites."""

        self.context.not_implemented_notification(
            "Favorite support is not implemented yet. "
            "This will allow you to save and remove anime from your favorites."
        )

    async def _add_to_watchlist(self, widget: toga.Widget) -> None:
        """Add the anime to the user's watchlist."""

        self.context.not_implemented_notification(
            "Watchlist support is not implemented yet. "
            "This will allow you to keep track of anime you want to watch."
        )

    async def _open_trailer(self, widget: toga.Widget) -> None:
        """Open the anime trailer."""

        self.context.not_implemented_notification(
            "Trailer support is not implemented yet. "
            "This will open the anime's trailer when one is available."
        )

    async def _share(self, widget: toga.Widget) -> None:
        """Share the anime."""

        self.context.not_implemented_notification(
            "Share function will be implemented soon"
        )

    async def _refresh(self, widget: toga.Widget) -> None:
        """Reload the current anime."""

        if self.anime_id is not None:
            await self.load(self.anime_id)

    # =========================================================
    # FUTURE FEATURES
    # =========================================================

    async def _mark_as_watched(self, widget: toga.Widget) -> None:
        """Mark the anime as watched."""

        self.context.not_implemented_notification(
            "Watch progress tracking is not implemented yet. "
            "This will mark the entire anime as watched."
        )

    async def _mark_episode_watched(
        self,
        episode: int,
    ) -> None:
        """Mark a specific episode as watched."""

        self.context.not_implemented_notification(
            f"Episode progress tracking is not implemented yet. "
            f"Episode {episode} will be marked as watched here."
        )

    async def _add_rating(
        self,
        rating: float,
    ) -> None:
        """Rate the anime."""

        self.context.not_implemented_notification(
            f"Anime rating is not implemented yet. "
            f"A rating of {rating} will be saved here."
        )

    async def _open_external_page(
        self,
        widget: toga.Widget,
    ) -> None:
        """Open the anime's external page."""

        self.context.not_implemented_notification(
            "External page support is not implemented yet. "
            "This will open the anime's page on the external service."
        )

    async def _download_poster(
        self,
        widget: toga.Widget,
    ) -> None:
        """Download/save the anime poster."""

        self.context.not_implemented_notification(
            "Poster download is not implemented yet. "
            "This will allow you to save the anime poster locally."
        )

    async def _add_to_collection(
        self,
        widget: toga.Widget,
    ) -> None:
        """Add anime to a custom collection."""

        self.context.not_implemented_notification(
            "Custom collections are not implemented yet. "
            "This will allow you to add the anime to one of your collections."
        )

    async def _remove_from_collection(
        self,
        widget: toga.Widget,
    ) -> None:
        """Remove anime from a custom collection."""

        self.context.not_implemented_notification(
            "Custom collection management is not implemented yet. "
            "This will allow you to remove the anime from a collection."
        )

    async def _show_related_anime(
        self,
        widget: toga.Widget,
    ) -> None:
        """Display related anime."""

        self.context.not_implemented_notification(
            "Related anime are not available yet. "
            "This section will show anime connected to this title."
        )

    async def _show_characters(
        self,
        widget: toga.Widget,
    ) -> None:
        """Display anime characters."""

        self.context.not_implemented_notification(
            "Character information is not implemented yet. "
            "This will display the characters and their roles in the anime."
        )

    async def _show_staff(
        self,
        widget: toga.Widget,
    ) -> None:
        """Display anime staff."""

        self.context.not_implemented_notification(
            "Staff information is not implemented yet. "
            "This will display the people involved in producing the anime."
        )

    async def _show_recommendations(
        self,
        widget: toga.Widget,
    ) -> None:
        """Display recommended anime."""

        self.context.not_implemented_notification(
            "Anime recommendations are not implemented yet. "
            "This will show titles similar to the current anime."
        )

    # =========================================================
    # ERROR HANDLING
    # =========================================================

    def _build_error(self, error: Exception) -> None:
        """Display the error state."""

        self.clear()

        retry_button = toga.Button(
            "Retry",
            on_press=self._retry,
            style=toga.style.Pack(
                padding=8,
            ),
        )

        back_button = toga.Button(
            "← Back",
            on_press=self._go_back,
            style=toga.style.Pack(
                padding=8,
            ),
        )

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
                    toga.Box(
                        children=[
                            back_button,
                            retry_button,
                        ],
                        style=toga.style.Pack(
                            direction=ROW,
                            padding=5,
                        ),
                    ),
                ],
                style=toga.style.Pack(
                    direction=COLUMN,
                    alignment="center",
                    flex=1,
                    padding=20,
                ),
            )
        )

    async def _retry(self, widget: toga.Widget) -> None:
        """Retry loading the current anime."""

        if self.anime_id is not None:
            await self.load(self.anime_id)