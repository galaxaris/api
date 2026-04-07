"""Resource loading utilities.

This module centralizes image and sound loading through a typed resource
provider abstraction.
"""

from enum import Enum
from os.path import join
import pygame as pg
from pygame import Surface
from pygame.mixer import Sound


class ResourceType(Enum):
    """Defines supported resource origins."""

    GLOBAL = 0
    BUNDLED = 1

class Resource:
    """Loads assets from a configured base path."""

    path = str
    type = ResourceType
    def __init__(self, resource_type:ResourceType, path):
        """Initialize a resource provider.

        :param resource_type: Type of resource source to use.
        :param path: Root path used to resolve asset files.
        """
        self.type = resource_type
        if resource_type.GLOBAL:
            self.path = path

    def image(self, image_path)-> Surface | None:
        """Load an image as a pygame surface.

        :param image_path: Image path relative to the configured root.
        :return: Loaded surface, or `None` when unavailable.
        """
        if self.type.GLOBAL:
            return pg.image.load(join(self.path, image_path))
        return None

    def sound(self, sound_path)-> Sound | None:
        """Load a sound effect.

        :param sound_path: Sound path relative to the configured root.
        :return: Loaded sound, or `None` when unavailable.
        """
        if self.type.GLOBAL:
            return pg.mixer.Sound(join(self.path, sound_path))
        return None