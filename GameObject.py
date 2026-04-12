"""Core GameObject abstraction used throughout the API.
Based on Unity's GameObject

"""

import os
from typing import Optional

import pygame as pg

from api.assets.Animation import Animation
from api.assets.Texture import Texture
from api.utils import Debug
from api.utils.Console import *


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
    surface: Optional[pg.Surface]
    direction: str = "right"
    id: int
    interact: bool = False
    visible: bool = True
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2):
        """
        Initializes the GameObject with given parameters.

        :param pos: Position of the GameObject (x, y)
        :param size: Size of the GameObject (width, height)
        """
        super().__init__()


        self.audio_manager = None
        self.pos = pg.Vector2(pos)
        self.size = pg.Vector2(size)
        self.image = pg.Surface(size, pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.animation = None
        self.id = id(self)
        self.textures = {}
        self.tags = set()
        self.direction = "right"
        self.surface = None
        self.offset = None
        self.interact = False
        self.destroyed = False
        self.visible = True
        self.in_trigger_interact = False

    def set_texture(self, texture:Texture, rescale: bool = False):
        """
        Sets the texture for the GameObject.

        :param rescale: Rescale the texture to fit the GameObject's size (if False, the texture will be repeated to fill the size)
        :param texture: The texture to be set
        """
        self.animation = None

        if rescale:
            self.image = pg.transform.scale(texture.image, self.size)
        else:
            self.image = self.repeat_texture(texture.image, self.size)

        self.rect = self.image.get_rect(topleft=self.pos)

    def repeat_texture(self, surface: pg.Surface, size:pg.Vector2 | tuple[int, int]) -> pg.Surface:
        #Avoid division by zero
        if surface.get_width() == 0 or surface.get_height() == 0:
            return surface
        s_size = pg.Vector2(surface.get_size())
        new_image = pg.Surface(size, pg.SRCALPHA, 32).convert_alpha()

        for y in range(int(self.size.y // s_size.y) + (1 if self.size.y % s_size.y != 0 else 0)):
            for x in range(int(self.size.x // s_size.x) + (1 if self.size.x % s_size.x != 0 else 0)):
                new_image.blit(surface, (x * s_size.x, y * s_size.y))

        return new_image

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
        Sets the size of the GameObject.

        :param size: The new size (width, height)
        """
        self.size = pg.Vector2(size)
        self.image = self.repeat_texture(self.image, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        if self.size and self.size != (0, 0) and self.animation:
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
        if self.size and self.size != (0, 0) and self.animation:
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

    def bind_texture(self, name: str, texture: Texture):
        """
        Binds a texture to a name for easy retrieval later.

        :param name: The name to bind the texture to
        :param texture: The texture to be bound
        """
        self.textures[name] = texture

    def bind_textures(self, textures: dict[str, Texture]):
        """
        Binds multiple textures to names for easy retrieval later.

        :param textures: A dictionary of name-texture pairs to be bound
        """
        for name, texture in textures.items():
            self.bind_texture(name, texture)

    def set_texture_bound(self, name: str, rescale: bool = False):
        """
        Set a texture bound to a name.

        :param name: The name of the texture to retrieve
        :return: The texture bound to the name, or None if not found
        """
        texture = self.textures.get(name, self.image)
        self.set_texture(texture, rescale)


    def update(self, scene=None):
        """
        Updates the GameObject. If it has an animation, updates the image to the current frame of the animation.
        """
        if self.destroyed:
            self.set_position((-1000, -1000))  # Move off-screen to avoid interactions
            return
        if self.animation:
            self.set_surface(self.animation.get_frame(self.direction))

    def set_direction(self, direction: str):
        """
        Sets the direction of the GameObject (for animations with directional frames).

        :param direction: The new direction ("left", "right", etc.)
        """
        if direction in ["left", "right"]:
            self.direction = direction

    def draw(self, surface: pg.Surface, scene=None):
        """
        Draws the GameObject. Offsets taken into account!
        In debug mode, also draws the collider rect underlined in red.

        :param scene:
        :param surface: The surface on which to draw the GameObject
        :param offset: The offset to be applied to the GameObject's position when drawing (useful for camera movement)
        """
        if self.destroyed:
            return
        offset = scene.camera.position if scene else pg.Vector2(0, 0)
        self.surface = surface
        self.offset = offset
        self.audio_manager = scene.audio_manager if scene else None

        if not self.animation and self.direction == "left":
            self.image = pg.transform.flip(self.image, True, False)

        if self.visible:
            surface.blit(self.image, self.pos - offset)

        #DEBUG
        if Debug.is_enabled("colliders") and "debug" not in self.tags and "dont_debug" not in self.tags:
            pg.draw.rect(surface, (255, 0, 0), self.rect.move(-offset.x, -offset.y), 1)
