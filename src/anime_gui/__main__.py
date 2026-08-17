from toga_gtk.widgets.base import Widget
from typing import cast
import toga
from toga.style import Pack
from toga.style.pack import ROW

from .layout import create_tab, search_anime


class MyApp(toga.App):
    def startup(self) -> None:
        self.main_window: toga.MainWindow = toga.MainWindow(title=self.formal_name)

        list_number = create_tab(self, list(map(str, range(10))))
        list_string = create_tab(self, ["hello", "no hello"])
        search_anime_tab = search_anime(self)

        tabs = toga.OptionContainer(
            content=[
                ("Search", search_anime_tab),
                ("Numbers", list_number),
                ("Strings", list_string),
            ],
            style=Pack(flex=1),
        )

        self.main_window.content = tabs
        self.main_window.show()


def main():
    return MyApp(
        "My App",
        "com.example.myapp",
    )


if __name__ == "__main__":
    main().main_loop()
