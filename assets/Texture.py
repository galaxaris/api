"""Texture abstraction built on top of pygame surfaces."""

import pygame as pg

from api.assets.Resource import Resource

class Texture(pg.Surface):
    """
    Texture class, based on pygame.Surface. Contains the image of a texture and its path.
    """
    path = str
    image = pg.Surface
    def __init__(self, path:str, resource:Resource) :
        """
        Initializes the texture with the given path and resource.

        :param path: Path to the texture image
        :param resource: Resource manager to load the image
        """
        self.path = path
        self.image = resource.image(path)
        super().__init__(self.image.get_size())

    def override_image(self, param):
        """
        Overrides the current image with a new one.

        :param param: The new image to use
        """
        self.image = param
        self.blit(self.image, (0, 0))