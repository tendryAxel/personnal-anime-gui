from typing import Optional
from toga import Window, Widget


class PageManager:
    window: Window
    pages: dict[str, Widget]
    current: Optional[str]
    navigation_stack: list[str]

    def __init__(self, window: Window):
        self.window = window
        self.pages = {}
        self.current = None
        self.navigation_stack = []

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

    def _show_without_navigation_history(self, name: str) -> None:
        page = self.pages[name]

        self.window.content = page
        self.current = name

    def show(self, name: str) -> None:
        self.navigation_stack.append(name)
        self._show_without_navigation_history(name)
    
    def back(self) -> None:
        self._has_2_or_more_pages_in_navigation_history()
        self.navigation_stack.pop()
        self._show_without_navigation_history(self.navigation_stack[-1])
    
    def _has_2_or_more_pages_in_navigation_history(self) -> None:
        if len(self.navigation_stack) < 2:
            raise RuntimeError(f"Less than 2 pages in navigation history, only {self.navigation_stack}")
