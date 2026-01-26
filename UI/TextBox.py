from dataclasses import dataclass
from api.UI import UI

@dataclass()
class TextBox(UI):
    text: str
    font_size: int
    font_color: tuple[int, int, int]
    background_color: tuple[int, int, int]
    width: int
    height: int
    def set_text(self, new_text: str):
        self.text = new_text
    def set_font_size(self, new_size: int):
        self.font_size = new_size
    def set_font_color(self, new_color: tuple[int, int, int]):
        self.font_color = new_color
    def set_background_color(self, new_color: tuple[int, int, int]):
        self.background_color = new_color