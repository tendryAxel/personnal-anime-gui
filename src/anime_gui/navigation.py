from typing import Optional
from toga import Window, Widget


class PageManager:
    window: Window
    pages: dict[str, Widget]
    current: Optional[str]

    def __init__(self, window: Window):
        self.window = window
        self.pages = {}
        self.current = None

    def register(self, name: str, page: Widget) -> None:
        """
        The first page registered will be set as the current
        If page name already exist and another is registered, the current one will be deleted
        """
        if name in self.pages:
            del self.pages[name]
        self.pages[name] = page
        if self.current is None:
            self.show(name)

    def show(self, name: str) -> None:
        page = self.pages[name]

        self.window.content = page
        self.current = name
