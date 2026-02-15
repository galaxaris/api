from enum import Enum
from os.path import join
import pygame as pg
from pygame import Surface
from pygame.mixer import Sound


class ResourceType(Enum):
    GLOBAL = 0
    BUNDLED = 1

class Resource:
    path = str
    type = ResourceType
    def __init__(self, resource_type:ResourceType, path):
        self.type = resource_type
        if resource_type.GLOBAL:
            self.path = path

    def image(self, image_path)-> Surface | None:
        if self.type.GLOBAL:
            return pg.image.load(join(self.path, image_path))
        return None

    def sound(self, sound_path)-> Sound | None:
        if self.type.GLOBAL:
            return pg.mixer.Sound(join(self.path, sound_path))
        return None