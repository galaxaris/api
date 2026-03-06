"""Core GameObject abstraction used throughout the API.
Based on Unity's GameObject

"""

import os
from typing import Optional

import pygame as pg

from api.assets.Animation import Animation
from api.assets.Texture import Texture
from api.utils import Debug


class GameObject:
    """
    GameObject class. Represents any object in the game that can be rendered and updated. Contains attributes for position, size, image, animation, and tags for categorization.

    Based on Unity's GameObject
    """
    pos: pg.Vector2
    size: pg.Vector2
    rect: pg.Rect
    image: pg.Surface
    animation: Optional[Animation]
    direction: str = "right"
    id: int
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2):
        """
        Initializes the GameObject with given parameters.

        :param pos: Position of the GameObject (x, y)
        :param size: Size of the GameObject (width, height)
        """
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
        """
        Sets the texture for the GameObject.

        :param texture: The texture to be set
        """
        self.animation = None
        self.image = pg.transform.scale(texture.image, self.size)
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_surface(self, surface:pg.Surface):
        """
        Sets the surface for the GameObject.

        :param surface: The surface to be set
        """
        self.image = surface
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_position(self, pos: tuple[int, int] | tuple[float, float] | pg.Vector2):
        """
        Sets the position of the GameObject.

        :param pos: The new position (x, y)
        """
        self.pos = pg.Vector2(pos)
        self.rect.topleft = pos

    def set_size(self, size: tuple[int, int] | pg.Vector2):
        """
        Sets the size of the GameObject. (wow wowwowow)

        :param size: The new size (width, height)
        """
        self.size = pg.Vector2(size)
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.animation.calculate_frame_size(self.size)

    def set_color(self, color: tuple[int, int, int]):
        """
        Sets the color of the GameObject.

        :param color: The new color (r, g, b)
        """
        self.image.fill(color)

    def set_animation(self, animation: Animation):
        """
        Sets the animation for the GameObject.

        :param animation: The animation to be set
        """
        self.animation = animation
        self.animation.calculate_frame_size(self.size)

    def add_tag(self, tag: str):
        """
        Adds a tag to the GameObject. 
        
        Used to categorize specific GameObject families  (e.g., "enemy", "player", "collectible") 
        and handle them accordingly in the game logic (triggers, collisions, etc.).

        :param tag: The tag to be added
        """
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        """Removes a tag from the GameObject.

        :param tag: The tag to be removed
        """
        self.tags.discard(tag)

    def update(self):
        """
        Updates the GameObject. If it has an animation, updates the image to the current frame of the animation.
        """

        if self.animation:
            self.image = self.animation.get_frame(self.direction)
            self.rect = self.image.get_rect(topleft=self.pos)

    def set_direction(self, direction: str):
        """
        Sets the direction of the GameObject (for animations with directional frames).

        :param direction: The new direction ("left", "right", etc.)
        """
        if direction in ["left", "right"]:
            self.direction = direction

    def draw(self, surface: pg.Surface, offset=pg.Vector2(0, 0)):
        """
        Draws the GameObject. Offsets taken into accccccount!
        In debug mode, also draws the collider rect underlined in red.

        :param surface: The surface on which to draw the GameObject
        :param offset: The offset to be applied to the GameObject's position when drawing (useful for camera movement)
        """
        self.update()

        if not self.animation and self.direction == "left":
            self.image = pg.transform.flip(self.image, True, False)

        surface.blit(self.image, self.pos - offset)

        #DEBUG
        if Debug.is_enabled("colliders") and "debug" not in self.tags and "dont_debug" not in self.tags:
            pg.draw.rect(surface, (255, 0, 0), self.rect.move(-offset.x, -offset.y), 1)
