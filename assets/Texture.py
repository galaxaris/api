import pygame as pg

from api.assets.Resource import Resource

class Texture(pg.Surface):
    path = str
    image = pg.Surface
    def __init__(self, path:str, resource:Resource) :
        self.path = path
        self.image = resource.image(path)
        super().__init__(self.image.get_size())