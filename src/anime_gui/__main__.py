from toga_gtk.widgets.base import Widget
from typing import cast
import toga
from toga.style import Pack
from toga.style.pack import ROW

from anime_gui.pages.search_page import SearchPage
from anime_gui.pages.details_page import AnimeDetailPage
from anime_gui.navigation import PageManager


class MyApp(toga.App):
    def startup(self) -> None:
        self.main_window: toga.MainWindow = toga.MainWindow(
            title="Anime Explorer",
        )
        self.pages = PageManager(self.main_window)

        self.search_page = SearchPage(self.pages)
        self.detail_page = AnimeDetailPage()

        self.pages.register("search", self.search_page)
        self.pages.register("details", self.detail_page)
        self.main_window.show()


def main():
    return MyApp(
        "My App",
        "com.example.myapp",
    )


if __name__ == "__main__":
    main().main_loop()
