"""Texture abstraction built on top of pygame surfaces."""

import pygame as pg

from api.assets.ResourceManager import Resource
from api.utils.Console import *

class Texture(pg.Surface):
    """
    Texture class, based on pygame.Surface. Contains the image of a texture and its path.
    """
    path = str
    image = pg.Surface
    def __init__(self, path:str, resource:Resource, is_missing=False) :
        """
        Initializes the texture with the given path and resource.

        :param path: Path to the texture image
        :param resource: Resource manager to load the image
        """

        if is_missing:
            self.missing_texture()
            super().__init__(self.image.get_size())
            return

        self.path = path

        try:
            self.image = resource.image(path)
        except Exception as e:
            print_error(f"loading texture from {path}: {e}")
            self.missing_texture()


        super().__init__(self.image.get_size())

    def override_image(self, param):
        """
        Overrides the current image with a new one.

        :param param: The new image to use
        """
        self.image = param
        self.blit(self.image, (0, 0))

    def missing_texture(self):
        """
        Returns a magenta and black checkerboard pattern to indicate a missing texture.
        """
        # Magenta and black color to indicate missing texture
        self.image = pg.Surface((32, 32))
        magenta_rect_2 = pg.Rect(0, 0, 16, 16)
        magenta_rect = pg.Rect(16, 16, 16, 16)
        black_rect = pg.Rect(0, 16, 16, 16)
        black_rect_2 = pg.Rect(16, 0, 16, 16)
        self.image.fill((255, 0, 255), magenta_rect)
        self.image.fill((255, 0, 255), magenta_rect_2)
        self.image.fill((0, 0, 0), black_rect)
        self.image.fill((0, 0, 0), black_rect_2)