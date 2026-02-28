from api.GameObject import GameObject
import pygame as pg

class Solid(GameObject):
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.add_tag("solid")

    def update(self):
        super().update()
