"""UI image element wrapper."""

from api.UI.GameUI import UIElement
from api.assets.Texture import Texture

class Image(UIElement):
    """UI element displaying a static texture."""

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], texture: Texture):
        """Initialize an image element.

        :param pos: Top-left position.
        :param size: Declared element size.
        :param texture: Texture to display.
        """
        super().__init__(pos, size)
        self.texture = texture
        self.image = self.texture.image
        self.rect = self.image.get_rect(topleft=self.pos)