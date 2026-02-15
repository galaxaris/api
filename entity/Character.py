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
    collided_objs : list[tuple[GameObject, str]]
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.vel = pg.Vector2(0, 0)
        self.jump = False
        self.fall = False
        self.animations = {}
        self.gravity = None
        self.collided_objs = []
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
        self.jump = False
        self.fall = True
        self.vel.y = 0

    def update(self, others):
        super().update(others)

        #Correct jump state if character is on the ground

        dx = self.vel.x
        dy = self.vel.y

        self.collided_objs = get_collided_objects(self, "solid", others, dx, dy)
        is_collide = False

        if self.vel.y == 0 and self.jump:
            self.fall = True

        for obj in self.collided_objs:
            if obj[1] == "bottom":
                self.land()
                is_collide = True
                dy = 0
            elif obj[1] == "top":
                self.hit_head()
                is_collide = True
                dy = 0
            if obj[1] in ("left", "right"):
                dx = 0

        if not is_collide:
            self.fall = True

        if self.gravity and self.fall:
            self.vel.y += self.gravity

        self.set_position((self.pos.x + dx, self.pos.y + dy))