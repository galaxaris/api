from typing import Optional

from pygame.surface import Surface

from api.GameObject import GameObject
from api.assets.Animation import Animation
import pygame as pg

from api.physics.Collision import get_collided_objects


class Character(GameObject):
    animations: dict[str, Animation]
    vel: pg.Vector2
    jump: bool
    fall: bool
    gravity: Optional[float]
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.vel = pg.Vector2(0, 0)
        self.jump = False
        self.fall = False
        self.animations = {}
        self.gravity = None
        self.add_tag("entity")

    def add_animation(self, name: str, animation: Animation):
        self.animations[name] = animation

    def set_gravity(self, gravity: float):
        self.gravity = gravity

    def land(self):
        self.vel.y = 0
        self.jump = False
        self.fall = False

    def hit_head(self):
        self.fall = False
        self.vel.y = 0

    def update(self):
        super().update()
        self.mask = pg.mask.from_surface(Surface(self.image.get_size(), pg.SRCALPHA, 32))
        self.set_position((self.pos.x + self.vel.x, self.pos.y + self.vel.y))

        objects = get_collided_objects(self, "solid")
        for obj in objects:
            if obj:
                if self.vel.y > 0:
                    self.rect.bottom = obj.rect.top
                    self.land()
                elif self.vel.y < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()


        if self.gravity is not None and self.fall:
            self.vel.y += self.gravity
