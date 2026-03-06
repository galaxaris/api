"""Simple text UI element."""

from api.UI.GameUI import UIElement
from api.utils.Fonts import get_font
import pygame as pg

class Text(UIElement):
    """UI element rendering a single text surface."""

    text : str
    font : str
    size_text : int
    color : tuple[int, int, int]
    def __init__(self, pos: tuple[int, int], size_text: int, text: str, font: str = "arial", color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize a text element.

        :param pos: Top-left text position.
        :param size_text: Font size.
        :param text: Text content.
        :param font: Font name or path marker.
        :param color: Text color.
        """
        super().__init__(pos, (0,0))
        self.font = font
        self.color = color
        self.size_text = size_text
        self.set_text(text)

    def set_text(self, text: str):
        """Update text content and regenerate the render surface.

        :param text: New text content.
        :return:
        """
        self.text = text
        self.image = get_font(self.font, self.size_text).render(self.text, False, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.size = self.image.get_size()