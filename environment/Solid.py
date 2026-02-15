from api.GameObject import GameObject
import pygame as pg

class Solid(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.mask = None
        self.add_tag("solid")

    def update(self):
        super().update()
        self.mask = pg.mask.from_surface(self.image)

