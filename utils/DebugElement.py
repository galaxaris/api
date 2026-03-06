"""Specialized UI text element for debug overlays."""

from api.UI.Text import Text


class DebugElement(Text):
    """Text element tagged for debug rendering."""

    def __init__(self, pos: tuple[int, int], size_text: int, text: str, font: str = "arial", color: tuple[int, int, int] = (255, 255, 255)):
        """Initialize a debug text element.

        :param pos: Top-left render position.
        :param size_text: Font size.
        :param text: Text content.
        :param font: Font name or path marker.
        :param color: Text color.
        """
        super().__init__(pos, size_text, text, font, color)
        self.add_tag("debug")