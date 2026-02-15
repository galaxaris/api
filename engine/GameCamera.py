from typing import Optional

import pygame as pg

from api.GameObject import GameObject

class GameCamera:
    def __init__(self, position: tuple[int, int]):
        self.limit_bottomright : Optional[pg.Vector2] = None
        self.limit_topleft : Optional[pg.Vector2] = None
        self.position : pg.Vector2 = pg.Vector2(position)
        self.offset : pg.Vector2  = pg.Vector2(0, 0)
        self.focused_object : Optional[GameObject] = None

    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy

    def focus(self, game_object: GameObject):
        self.focused_object = game_object
        self.update()

    def set_offset(self, offset: tuple[int, int] | pg.Vector2):
        self.offset = pg.Vector2(offset)
        self.update()

    def set_limits(self, topleft: tuple[int , int], bottomright: tuple[int , int]):
        self.limit_topleft = pg.Vector2(topleft)
        self.limit_bottomright = pg.Vector2(bottomright)

    def update(self):
        if self.focused_object and hasattr(self.focused_object, 'pos'):
            if self.limit_topleft and self.limit_bottomright:
                target_x = max(self.limit_topleft.x, min(self.focused_object.pos.x - self.offset.x, self.limit_bottomright.x))
                target_y = max(self.limit_topleft.y, min(self.focused_object.pos.y - self.offset.y, self.limit_bottomright.y))
            else:
                target_x = self.focused_object.pos.x - self.offset.x
                target_y = self.focused_object.pos.y - self.offset.y


            self.position.x = target_x
            self.position.y = target_y