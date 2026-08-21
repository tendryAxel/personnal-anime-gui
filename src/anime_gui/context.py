from anime_gui.navigation import PageManager
import dataclasses


@dataclasses.dataclass(
    frozen=True,
    slots=True,
)
class ApplicationContext:
    page_manager: PageManager
