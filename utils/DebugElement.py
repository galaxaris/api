"""Specialized UI text element for debug overlays."""
import pygame as pg

from api.utils.Fonts import get_font


class DebugElement():
    """Text element tagged for debug rendering."""

    text: str
    font: str
    size_text: int
    color: tuple[int, int, int]
    def __init__(self, pos: tuple[int, int], size_text: int, text: str, font: str = "arial", color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize a debug text element.

        :param pos: Top-left render position.
        :param size_text: Font size.
        :param text: Text content.
        :param font: Font name or path marker.
        :param color: Text color.
        """
        self.size = None
        self.rect = None
        self.image = None
        self.pos = pg.Vector2(pos)
        self.font = font
        self.color = color
        self.size_text = size_text
        self.set_text(text)

    def set_position(self, pos: tuple[int, int]):
        """Update render position.

        :param pos: New top-left render position.
        :return:
        """
        self.pos = pg.Vector2(pos)

    def set_text(self, text: str):
        """Update text content and regenerate the render surface.

        :param text: New text content.
        :return:
        """
        self.text = text
        self.image = get_font(self.font, self.size_text).render(self.text, False, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.size = self.image.get_size()

    def draw(self, surface: pg.Surface):
        """Render the debug element to a surface.

        :param surface: Target render surface.
        :return:
        """
        surface.blit(self.image, self.pos)


