from typing import Optional

import pygame as pg

from api.assets.Animation import Animation
from api.assets.Texture import Texture

class GameObject(pg.sprite.Sprite):
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
        self.image = pg.Surface(size, pg.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=pos)
        self.animation = None
        self.id = id(self)
        self.mask = None
        self.tags = set()
        self.direction = "right"

    def set_texture(self, texture:Texture):
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

    def set_color(self, color: tuple[int, int, int]):
        self.image.fill(color)

    def set_animation(self, animation: Animation):
        self.animation = animation

    def add_tag(self, tag: str):
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        self.tags.discard(tag)

    def update(self):
        if self.animation:
            self.image = pg.transform.scale(self.animation.get_frame(self.direction), self.size)
            self.rect = self.image.get_rect(topleft=self.pos)

    def set_direction(self, direction: str):
        if direction in ["left", "right"]:
            self.direction = direction

    def draw(self, surface: pg.Surface, offset=pg.Vector2(0, 0)):
        self.update()
        surface.blit(self.image, self.pos - offset)
