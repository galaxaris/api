import pygame as pg
import math

from api.entity.Entity import Entity


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, gravity: float, shot_speed: float, angle_radians: float, size: tuple[int, int] = (8,8), effect: str = None, target: str = None, Time = None):
        super().__init__(pos, size)
        self.pos = pg.Vector2(pos)
        self.vel = shot_speed * pg.Vector2(math.cos(angle_radians), -math.sin(angle_radians))* Time.deltaTime * 2.4
        self.add_tag("projectile")
        self.image = pg.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True
        self.to_kill = False
        self.set_gravity(gravity*98.1)
        self.resistance = 0.1

    def update(self, scene=None) :
        super().update(scene)

        print(self.resistance)
        if self.collided_objs:
            self.on_impact()

    def on_impact(self):
        self.to_kill = True















