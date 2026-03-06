"""Parallax background rendering utilities."""

from typing import Optional, List
import pygame as pg
from api.GameObject import GameObject
from api.assets.Texture import Texture

class ParallaxLayer:
    """Single parallax layer with speed coefficients and image data."""

    def __init__(self, speed: pg.Vector2 | tuple[float, float], texture: Texture):
        """Initialize a parallax layer.

        :param speed: Relative movement speed on x/y axes.
        :param texture: Texture used for this layer.
        """
        self.speed = pg.Vector2(speed)
        self.image = texture.image.convert_alpha()
        self.size = pg.Vector2(self.image.get_size())

class ParallaxBackground:
    """Collection of parallax layers rendered behind the scene."""

    def __init__(self, render_size: pg.Vector2 | tuple[int, int], parallax_layers: Optional[List[ParallaxLayer]] = None, fill_color: Optional[tuple[int, int, int]] = None):
        """Initialize the parallax background.

        :param render_size: Render target size.
        :param parallax_layers: Optional initial list of layers.
        :param fill_color: Optional color filled before drawing layers.
        """
        self.layers = parallax_layers if parallax_layers else []
        self.render_size = pg.Vector2(render_size)
        self.fill_color = fill_color
        self.layers.sort(key=lambda l: l.speed.x)

    def add_layer(self, speed: pg.Vector2, texture: Texture):
        """Add a parallax layer and keep layers sorted by speed.

        :param speed: Relative movement speed for the new layer.
        :param texture: Texture used by the new layer.
        :return:
        """
        self.layers.append(ParallaxLayer(speed, texture))
        self.layers.sort(key=lambda l: l.speed.x)

    def draw(self, scene_surface: pg.Surface, camera_offset: pg.Vector2 | tuple[float, float], layer: str = "background"):
        """Render all parallax layers according to camera offset.

        Layer textures are tiled to fill the render area and shifted according
        to each layer's speed factor.

        :param scene_surface: Destination surface.
        :param camera_offset: Current camera position.
        :param layer: Reserved parameter for compatibility.
        :return:
        """
        camera_offset = pg.Vector2(camera_offset)

        if self.fill_color:
            scene_surface.fill(self.fill_color)

        for layer_data in self.layers:
            off_x = -int(camera_offset.x * layer_data.speed.x % layer_data.size.x)
            off_y = -int(camera_offset.y * layer_data.speed.y % layer_data.size.y)

            for y in range(off_y, int(self.render_size.y), int(layer_data.size.y)):
                for x in range(off_x, int(self.render_size.x), int(layer_data.size.x)):
                    scene_surface.blit(layer_data.image, (x, y))