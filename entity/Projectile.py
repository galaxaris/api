import pygame as pg
import math

from api.entity.Entity import Entity
from api.physics.Collision import get_collided_objects


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, gravity: float, shot_speed: float, angle_radians: float, size: tuple[int, int] = (8,8), damage: int = 10):
        super().__init__(pos, size)
        self.pos = pg.Vector2(pos)
        self.vel = shot_speed * pg.Vector2(math.cos(angle_radians), -math.sin(angle_radians))
        self.add_tag("projectile")
        self.image = pg.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True
        self.to_kill = False
        self.set_gravity(gravity)
        self.resistance = 0
        self.damage = damage

    def update(self, scene=None) :
        super().update(scene)

        enemies_collisions = get_collided_objects(self, "enemy", scene.game_objects, self.vel.x, self.vel.y)
        if enemies_collisions:
            for obj in enemies_collisions:
                obj[0].take_damage(self.damage)
            self.collided_objs += enemies_collisions

        if self.collided_objs:
            self.on_impact()

    def on_impact(self):
        self.to_kill = True















