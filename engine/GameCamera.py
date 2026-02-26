from typing import Optional

import pygame as pg

from api.GameObject import GameObject
from api.utils import Debug
from api.utils.Inputs import get_inputs


class GameCamera:
    def __init__(self, position: tuple[int, int]):

        self.limit_bottomright : Optional[pg.Vector2] = None
        self.limit_topleft : Optional[pg.Vector2] = None
        self.position : pg.Vector2 = pg.Vector2(position)
        self.offset : pg.Vector2  = pg.Vector2(0, 0)
        self.focused_object : Optional[GameObject] = None
        self.freecam_old = self.position.copy()
        self.camera_mode = "Free"

    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy

    def focus(self, game_object: GameObject):
        self.focused_object = game_object

    def set_offset(self, offset: tuple[int, int] | tuple[float, float] | pg.Vector2):
        self.offset = pg.Vector2(offset)

    def set_limits(self, topleft: tuple[int , int], bottomright: tuple[int , int]):
        self.limit_topleft = pg.Vector2(topleft)
        self.limit_bottomright = pg.Vector2(bottomright)

    def set_position(self, position: tuple[int, int] | tuple[float, float] | pg.Vector2):
        self.position = pg.Vector2(position)


    def update(self):

        if Debug.is_enabled("freecam"):
            self.camera_mode = "Freecam"
            if not self.freecam_old:
                self.freecam_old = self.position.copy()


            inputs = get_inputs()
            boost = 5 if inputs["boost"] else 0

            if inputs["right"]:
                self.move(5+boost, 0)
            if inputs["left"]:
                self.move(-5-boost, 0)
            if inputs["down"]:
                self.move(0, 5+boost)
            if inputs["up"]:
                self.move(0, -5-boost)

        elif self.focused_object and hasattr(self.focused_object, 'pos'):
            if self.limit_topleft and self.limit_bottomright:
                target_x = max(self.limit_topleft.x, min(self.focused_object.pos.x - self.offset.x, self.limit_bottomright.x))
                target_y = max(self.limit_topleft.y, min(self.focused_object.pos.y - self.offset.y, self.limit_bottomright.y))
            else:
                target_x = self.focused_object.pos.x - self.offset.x
                target_y = self.focused_object.pos.y - self.offset.y

            self.camera_mode = self.focused_object.__class__.__name__
            self.position.x = target_x
            self.position.y = target_y
        else:
            if self.freecam_old:
                self.position = self.freecam_old.copy()
                self.freecam_old = None
            self.camera_mode = "Free"