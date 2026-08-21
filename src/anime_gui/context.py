from toga.window import Dialog
from toga import Window
import dataclasses

from anime_gui.navigation import PageManager


@dataclasses.dataclass(
    frozen=True,
    slots=True,
)
class ApplicationContext:
    page_manager: PageManager
    main_window: Window

    def not_implemented_notification(self, message: str) -> Dialog:
        return self.main_window.info_dialog(
            "It's not implemented yet",
            f"I am sorry\n{message}",
        )
