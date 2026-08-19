from typing import Optional
from anime_gui.anime_info_api.main import CachingUtilities
from threading import Thread
from io import BytesIO

import requests
import toga
import toga.style

from PIL import Image as PILImage


class LoadImage(toga.ImageView):
    """ImageView that loads an image asynchronously from a URL."""

    url: Optional[str]

    def __init__(
        self,
        url: Optional[str],
        *,
        style: toga.style.Pack | None = None,
        id: str | None = None,
        **kwargs,
    ):
        super().__init__(
            self._create_skeleton(),
            style=style,
            id=id,
            **kwargs,
        )

        self.url = url

        if url is not None:
            Thread(
                target=self._load,
                daemon=True,
            ).start()

    @staticmethod
    def _create_skeleton(
        width: int = 300,
        height: int = 450,
        color: str = "#E5E7EB",
    ) -> toga.Image:
        """Create an in-memory loading skeleton."""
        image = PILImage.new(
            "RGB",
            (width, height),
            color,
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        return toga.Image(buffer.getvalue())

    def _load(self) -> None:
        try:
            if self.url is None:
                return

            data = self._fetch_image(self.url)

            if self.app is None:
                raise Exception(f"App of {self} is None")

            self.app.loop.call_soon_threadsafe(
                self._set_image,
                data,
            )

        except Exception as exc:
            print(f"Failed to load image {self.url}: {exc}")

    def _set_image(self, data: bytes) -> None:
        self.image = toga.Image(data)

    @staticmethod
    @CachingUtilities.caching
    def _fetch_image(url: str) -> bytes:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.content