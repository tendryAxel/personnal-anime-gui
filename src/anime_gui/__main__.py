from toga_gtk.widgets.base import Widget
from typing import cast
import toga
from toga.style import Pack
from toga.style.pack import ROW

from .layout import search_anime
from anime_gui.pages.search_page import SearchPage
from anime_gui.pages.details_page import AnimeDetailPage

class PageManager:
    def __init__(self, window: toga.Window):
        self.window = window
        self.pages = {}
        self.current = None

    def register(self, name: str, page: toga.Widget):
        self.pages[name] = page

    def show(self, name: str):
        page = self.pages[name]

        self.window.content = page
        self.current = name

class MyApp(toga.App):
    def startup(self) -> None:
        self.main_window: toga.MainWindow = toga.MainWindow(
            title="Anime Explorer",
        )
        self.pages = PageManager(self.main_window)

        self.search_page = SearchPage()
        self.detail_page = AnimeDetailPage()

        self.pages.register("search", self.search_page)
        self.pages.show("search")
        self.pages.register("details", self.detail_page)
        self.main_window.show()


def main():
    return MyApp(
        "My App",
        "com.example.myapp",
    )


if __name__ == "__main__":
    main().main_loop()
