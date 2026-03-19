import pygame as pg
import math

from api.entity.Entity import Entity
from api.physics.Collision import get_collided_objects


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, gravity: float, shot_speed: float, angle_radians: float, effect: str=None, target: str="enemy", size: tuple[int, int] | pg.Vector2 = (8,8), damage: int = 10, projectile_speed: int = 0.8, colour = "white"):
        super().__init__(pos, size)
        self.pos = pg.Vector2(pos) - self.size/2
        self.add_tag("projectile")
        self.image = pg.Surface((8, 8))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=pos)

        self.fall = True
        self.to_kill = False

        self.resistance = 0
        self.damage = damage

        self.projectile_speed = projectile_speed
        adjusted_speed = shot_speed * projectile_speed
        self.vel = pg.Vector2(
            math.cos(angle_radians) * adjusted_speed,
            -math.sin(angle_radians) * adjusted_speed
        )

        self.set_gravity(gravity * (projectile_speed ** 2))
        self.add_tag(effect)
        self.target = target

    def update(self, scene=None) :
        # Update every projectile speed to reduce speed
        super().update(scene)
        enemies_collisions = get_collided_objects(self, self.target, scene.game_objects, self.vel.x, self.vel.y)

        if enemies_collisions:
            for obj in enemies_collisions:
                obj[0].take_damage(self.damage)
            self.collided_objs += enemies_collisions

        if self.collided_objs:
            if "bouncy" in self.tags:
                pass

            self.on_impact()

    def on_impact(self):
        self.to_kill = True















