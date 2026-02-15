from typing import Optional

import pygame as pg
from api.GameObject import GameObject
from api.assets.Texture import Texture

class ParallaxImage(GameObject):
    speed = pg.Vector2 | tuple[float, float]
    def __init__(self, speed: pg.Vector2 | tuple[float, float], texture: Texture, coordinates: tuple[int, int] = (0, 0)):
        super().__init__((0, 0), texture.get_size())
        self.add_tag("dont_debug")
        self.speed = pg.Vector2(speed)
        self.texture = texture
        self.set_texture(texture)
        self.coordinates = pg.Vector2(coordinates)

class ParallaxBackground:
    def __init__(self, render_size: pg.Vector2 | tuple[int, int], parallax_images: Optional[list[ParallaxImage]]):
        self.group = []
        self.render_size = pg.Vector2(render_size)
        if len(parallax_images) > 0:
            for parallax in parallax_images:
                self.add(parallax)

    def add(self, parallax: ParallaxImage):
        for j in range(max(2, int(self.render_size.y // parallax.size.y + 1))):
            for i in range(max(2, int(self.render_size.x // parallax.size.x + 1))):

                if (i, j) == (0, 0):
                    self.group.append(parallax)
                else:
                    new_parallax = ParallaxImage(parallax.speed, parallax.texture, coordinates=(i,j))
                    self.group.append(new_parallax)

        self.group.sort(key=lambda p: p.speed.x)

    def draw(self, screen, camera_offset: pg.Vector2 | tuple[float, float], layer: str = "background"):
        camera_offset = pg.Vector2(camera_offset)

        for parallax in self.group:
            #the int conversion is important so we don't have pixel holes because of round
            x = -int(camera_offset.x*parallax.speed.x%parallax.size.x) + parallax.coordinates.x*parallax.size.x
            y = -int(camera_offset.y*parallax.speed.y%parallax.size.y) + parallax.coordinates.y*parallax.size.y
            parallax.set_position((x, y))
            screen.add(parallax, layer)
