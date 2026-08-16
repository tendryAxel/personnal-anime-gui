from toga_gtk.widgets.base import Widget
from typing import cast
import toga
from toga.style import Pack
from toga.style.pack import ROW

from .layout import create_tab


class MyApp(toga.App):
    def startup(self) -> None:
        self.main_window: toga.MainWindow = toga.MainWindow(title=self.formal_name)

        list_tab = create_tab(self)

        tabs = toga.OptionContainer(
            content=[
                ("List", list_tab),
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
