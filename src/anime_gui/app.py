from http.server import HTTPServer
from pathlib import Path

from toga import App, MainWindow

from anime_gui.context import ApplicationContext
from anime_gui.http_server import start_sever
from anime_gui.navigation import PageManager
from anime_gui.pages.search_page import SearchPage


class MyApp(App):
    http_server: HTTPServer
    http_server_port: int

    def startup(self) -> None:
        self.http_server_port = 8765
        self._start_resource_server()

        self.main_window: MainWindow = MainWindow(
            title="Anime Explorer",
        )

        pages = PageManager(self.main_window)
        self.context = ApplicationContext(
            pages,
            self.main_window,
            loop=self.loop,
            app=self,
            video_server_url=f"http://localhost:{self.http_server_port}",
        )

        self.search_page = SearchPage(self.context)

        pages.register("search", self.search_page)
        self.main_window.show()

    def _start_resource_server(self) -> None:
        resource_dir = Path(self.paths.app) / "resources" / "videos"
        self.http_server = start_sever(self.http_server_port, resource_dir)

    def shutdown(self) -> None:
        """Properly shutdown HTTP server"""
        if hasattr(self, "http_server"):
            self.http_server.shutdown()
