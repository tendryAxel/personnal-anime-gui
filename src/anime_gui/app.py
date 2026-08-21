from anime_gui.context import ApplicationContext
from anime_gui.pages.details_page import AnimeDetailPage
from anime_gui.pages.search_page import SearchPage
from toga import App, MainWindow

from anime_gui.navigation import PageManager


class MyApp(App):
    def startup(self) -> None:
        self.main_window: MainWindow = MainWindow(
            title="Anime Explorer",
        )
        
        pages = PageManager(self.main_window)
        self.context = ApplicationContext(
            pages
        )

        self.search_page = SearchPage(self.context)

        pages.register("search", self.search_page)
        self.main_window.show()
