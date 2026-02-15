from api.UI import UIElement
import pygame as pg

class Text(UIElement):
    text : str
    font : str
    size_text : int
    color : tuple[int, int, int]
    def __init__(self, pos: tuple[int, int], size_text: int, text: str, font: str = "arial", color: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(pos, (0,0))
        self.font = font
        self.color = color
        self.size_text = size_text
        self.set_text(text)

    def set_text(self, text: str):
        self.text = text
        self.image = pg.font.SysFont(self.font, self.size_text).render(self.text, False, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.size = self.image.get_size()