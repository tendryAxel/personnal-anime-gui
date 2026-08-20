from toga import Window, Widget


class PageManager:
    def __init__(self, window: Window):
        self.window = window
        self.pages = {}
        self.current = None

    def register(self, name: str, page: Widget) -> None:
        """
        The first page registered will be set as the current
        """
        self.pages[name] = page
        if self.current is None:
            self.show(name)

    def show(self, name: str) -> None:
        page = self.pages[name]

        self.window.content = page
        self.current = name
