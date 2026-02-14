import pygame as pg

from api.GameObject import GameObject

class GameCamera:
    def __init__(self, position: tuple[int, int]):
        self.position = pg.Vector2(position)
        self.offset = pg.Vector2(0, 0)
        self.focused_object = None

    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy

    def focus(self, game_object: GameObject):
        self.focused_object = game_object
        self.update()

    def set_offset(self, offset: tuple[int, int] | pg.Vector2):
        self.offset = pg.Vector2(offset)
        self.update()

    def update(self):
        if self.focused_object and hasattr(self.focused_object, 'pos'):
            target_x = self.focused_object.pos.x - self.offset.x
            target_y = self.focused_object.pos.y - self.offset.y

            self.position.x = target_x
            self.position.y = target_y