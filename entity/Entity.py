from typing import Optional

from pygame.surface import Surface

from api.GameObject import GameObject
from api.assets.Animation import Animation
import pygame as pg

from api.assets.Texture import Texture
from api.physics.Collision import get_collided_objects
from api.utils import Debug


class Entity(GameObject):
    animations: dict[str, Animation | Texture]
    vel: pg.Vector2
    jump: bool
    fall: bool
    boost: bool
    gravity: Optional[float]
    collided_objs : list[tuple[GameObject, str]]
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.boost = False
        self.vel = pg.Vector2(0, 0)
        self.jump = False
        self.fall = False
        self.animations = {}
        self.gravity = None
        self.collided_objs = []
        self.add_tag("entity")

    def add_animation(self, name: str, animation: Animation):
        self.animations[name] = animation

    def bind_animations(self, animation_names: dict[str, Animation | Texture]):
        for name in animation_names:
            self.animations[name] = animation_names[name]

    def set_gravity(self, gravity: float):
        self.gravity = gravity

    def land(self):
        self.vel.y = 0
        self.jump = False
        self.fall = False

    def hit_head(self):
        self.vel.y = 0
        self.jump = False


    def update(self, others):
        super().update(others)
        self.update_sprite()
        self.collided_objs = get_collided_objects(self, "solid", others, self.vel.x, self.vel.y)
        on_ground = False

        for obj in self.collided_objs:
            if obj[1] == "top":
                self.land()
                on_ground = True
            elif obj[1] == "bottom":
                self.hit_head()
            if obj[1] == "left":
                self.vel.x = 0
                if self.direction == "left":
                    self.vel.x = -0.1
            elif obj[1] == "right":
                self.vel.x = 0
                if self.direction == "right":
                    self.vel.x = 0.1

        if not on_ground:
            self.fall = True
        else:
            self.fall = False

        if self.gravity and self.fall:
            self.vel.y += self.gravity

        self.set_position((self.pos.x + self.vel.x, self.pos.y + self.vel.y))

    def update_sprite(self):
        if self.vel.y > 0:
            self.set_sprite("fall")
        elif self.vel.y < 0:
            self.set_sprite("jump")
        elif self.vel.x != 0:
            if self.boost:
                self.set_sprite("run_fast")
            else:
                self.set_sprite("run")
        else:
            self.set_sprite("idle")

    def set_sprite(self, name: str):
        if name in self.animations:
            anim = self.animations[name]
            if isinstance(anim, Animation):
                self.set_animation(anim)
            elif isinstance(anim, Texture):
                self.set_texture(anim)