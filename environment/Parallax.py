from typing import Optional, List
import pygame as pg
from api.GameObject import GameObject
from api.assets.Texture import Texture

class ParallaxLayer:
    def __init__(self, speed: pg.Vector2 | tuple[float, float], texture: Texture):
        self.speed = pg.Vector2(speed)
        self.image = texture.image.convert_alpha()
        self.size = pg.Vector2(self.image.get_size())

class ParallaxBackground:
    def __init__(self, render_size: pg.Vector2 | tuple[int, int], parallax_layers: Optional[List[ParallaxLayer]] = None, fill_color: Optional[tuple[int, int, int]] = None):
        self.layers = parallax_layers if parallax_layers else []
        self.render_size = pg.Vector2(render_size)
        self.fill_color = fill_color
        self.layers.sort(key=lambda l: l.speed.x)

    def add_layer(self, speed: pg.Vector2, texture: Texture):
        self.layers.append(ParallaxLayer(speed, texture))
        self.layers.sort(key=lambda l: l.speed.x)

    def draw(self, scene_surface: pg.Surface, camera_offset: pg.Vector2 | tuple[float, float], layer: str = "background"):
        camera_offset = pg.Vector2(camera_offset)

        if self.fill_color:
            scene_surface.fill(self.fill_color)

        for layer_data in self.layers:
            off_x = -int(camera_offset.x * layer_data.speed.x % layer_data.size.x)
            off_y = -int(camera_offset.y * layer_data.speed.y % layer_data.size.y)

            for y in range(off_y, int(self.render_size.y), int(layer_data.size.y)):
                for x in range(off_x, int(self.render_size.x), int(layer_data.size.x)):
                    scene_surface.blit(layer_data.image, (x, y))