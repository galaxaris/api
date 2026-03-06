"""Static background rendering helpers."""

import pygame as pg

from api.assets.Texture import Texture

class Background:
    """Represents a static background surface, optionally tiled."""

    def __init__(self, texture: Texture, repeat: bool = True, size: tuple[int, int] | None = None):
        """Create a background from a texture.

        :param texture: Texture used as background source image.
        :param repeat: Whether the source image should be tiled.
        :param size: Output background size. Defaults to texture size.
        """
        self.image : Texture = texture.image
        self.repeat : bool = repeat
        self.surface : pg.Surface = pg.Surface(size if size else self.image.get_size(), pg.SRCALPHA, 32).convert_alpha()

        if repeat:
            if size is None:
                size = self.image.get_size()
            for y in range(0, size[1], self.image.get_height()):
                for x in range(0, size[0], self.image.get_width()):
                    self.surface.blit(self.image, (x, y))
        else:
            self.surface.blit(self.image, (0, 0))

    def draw(self):
        """Return the prepared background surface.

        :return: Render-ready background surface.
        """
        return self.surface



