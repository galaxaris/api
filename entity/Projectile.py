import pygame as pg
import math

from api.entity.Entity import Entity
from api.physics.Collision import get_collided_objects
from api.utils import GlobalVariables


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, gravity: float, shot_speed: float, angle_radians: float, size: tuple[int, int] = (8,8), effect: str = None, target: str = None):
        super().__init__(pos = pos, size = (8,8))
        self.pos = pg.Vector2(pos)
        self.vel = shot_speed * pg.Vector2(math.cos(angle_radians), -math.sin(angle_radians))
        self.add_tag("projectile")
        self.image = pg.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True
        self.to_kill = False
        self.set_gravity(gravity)

    def update(self) :
        super().update()

        if self.collided_objs:
            self.on_impact()

    def on_impact(self):
        self.to_kill = True















