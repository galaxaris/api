import os
from typing import Optional

import pygame as pg

from api.assets.Animation import Animation
from api.assets.Texture import Texture
from api.utils import Debug


class GameObject:
    pos: pg.Vector2
    size: pg.Vector2
    rect: pg.Rect
    image: pg.Surface
    animation: Optional[Animation]
    direction: str = "right"
    id: int
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2):
        super().__init__()
        self.pos = pg.Vector2(pos)
        self.size = pg.Vector2(size)
        self.image = pg.Surface(size, pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.animation = None
        self.id = id(self)
        self.tags = set()
        self.direction = "right"

    def set_texture(self, texture:Texture):
        self.animation = None
        self.image = pg.transform.scale(texture.image, self.size)
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_surface(self, surface:pg.Surface):
        self.image = surface
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_position(self, pos: tuple[int, int] | tuple[float, float] | pg.Vector2):
        self.pos = pg.Vector2(pos)
        self.rect.topleft = pos

    def set_size(self, size: tuple[int, int] | pg.Vector2):
        self.size = pg.Vector2(size)
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.animation.calculate_frame_size(self.size)

    def set_color(self, color: tuple[int, int, int]):
        self.image.fill(color)

    def set_animation(self, animation: Animation):
        self.animation = animation
        self.animation.calculate_frame_size(self.size)

    def add_tag(self, tag: str):
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        self.tags.discard(tag)

    def update(self, others):
        if self.animation:
            self.image = self.animation.get_frame(self.direction)
            self.rect = self.image.get_rect(topleft=self.pos)

    def set_direction(self, direction: str):
        if direction in ["left", "right"]:
            self.direction = direction

    def draw(self, surface: pg.Surface, offset=pg.Vector2(0, 0), game_objects=None):
        self.update(game_objects)

        if not self.animation and self.direction == "left":
            self.image = pg.transform.flip(self.image, True, False)

        surface.blit(self.image, self.pos - offset)

        #DEBUG
        if Debug.is_enabled("colliders") and "debug" not in self.tags and "dont_debug" not in self.tags:
            pg.draw.rect(surface, (255, 0, 0), self.rect.move(-offset.x, -offset.y), 1)
