from api.UI.Text import Text


class DebugElement(Text):
    def __init__(self, pos: tuple[int, int], size_text: int, text: str, font: str = "arial", color: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(pos, size_text, text, font, color)
        self.add_tag("debug")