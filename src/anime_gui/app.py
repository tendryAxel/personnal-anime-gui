from anime_gui.pages.details_page import AnimeDetailPage
from anime_gui.pages.search_page import SearchPage
from toga import App, MainWindow

from anime_gui.navigation import PageManager


class MyApp(App):
    def startup(self) -> None:
        self.main_window: MainWindow = MainWindow(
            title="Anime Explorer",
        )
        self.pages = PageManager(self.main_window)

        self.search_page = SearchPage(self.pages)
        self.detail_page = AnimeDetailPage()

        self.pages.register("search", self.search_page)
        self.pages.register("details", self.detail_page)
        self.main_window.show()
