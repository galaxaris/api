from dataclasses import dataclass

from api.UI.MenuUI import MenuUI


@dataclass()
class Text(MenuUI):
    content: str
    color: tuple[int, int, int]
    font_size: int
    def set_content(self, new_content: str):
        self.content = new_content