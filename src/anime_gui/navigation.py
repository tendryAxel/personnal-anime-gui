from toga import Window, Widget


class PageManager:
    def __init__(self, window: Window):
        self.window = window
        self.pages = {}
        self.current = None

    def register(self, name: str, page: Widget):
        self.pages[name] = page

    def show(self, name: str):
        page = self.pages[name]

        self.window.content = page
        self.current = name
