import pygame as pg

class Scene(pg.Surface):
    def __init__(self, width: int, height: int):
        super().__init__((width, height))