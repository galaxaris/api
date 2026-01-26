from dataclasses import dataclass

from api.UI import UI

@dataclass()
class Text(UI):
    content: str
    font_size: int
    font_color: tuple[int, int, int]

    def set_content(self, new_content: str):
        self.content = new_content

    def set_font_size(self, new_size: int):
        self.font_size = new_size

    def set_font_color(self, new_color: tuple[int, int, int]):
        self.font_color = new_color