"""Entity abstraction with movement, collisions, and animation state."""

from typing import Optional

from pygame.surface import Surface

from api.GameObject import GameObject
from api.assets.Animation import Animation
import pygame as pg

from api.assets.Texture import Texture
from api.physics.Collision import get_collided_objects
from api.utils import Debug, GlobalVariables


class Entity(GameObject):
    """
    Entity class, based on GameObject. Contains all the attributes and methods common to all entities in the game (player, enemies, etc.).
    
    ==> parallel with Unity: the Entity behaves like a **Rigidbody2D**, while the GameObject behaves like a GameObject. The Entity is a GameObject with physics and animations.
    """

    animations: dict[str, Animation | Texture]
    vel: pg.Vector2
    jump: bool
    fall: bool
    boost: bool
    gravity: Optional[float]
    collided_objs : list[tuple[GameObject, str]]
    is_hitting_ground: bool

    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        """
        Initializes the entity with the given attributes.

        :param pos: Entity position
        :param size: Entity size
        """
        super().__init__(pos, size)
        self.boost = False
        self.vel = pg.Vector2(0, 0)
        self.jump = False
        self.fall = False
        self.animations = {}
        self.gravity = None
        self.collided_objs = []
        self.is_hitting_ground = False
        self.projectiles = []
        self.weapon_point = pg.Vector2(size[0]//2, size[1]//2)
        self.sfx_list = {}
        self.add_tag("entity")


    def add_animation(self, name: str, animation: Animation):
        """
        Adds an animation to the entity.

        :param name: Name of the animation
        :param animation: Animation object to be added
        """
        self.animations[name] = animation

    def bind_animations(self, animation_names: dict[str, Animation | Texture]):
        """
        Binds multiple animations to the entity at once.

        :param animation_names: Dictionary of animation names and their corresponding Animation or Texture objects
        """
        for name in animation_names:
            self.animations[name] = animation_names[name]

    def set_gravity(self, gravity: float):
        """
        Sets the gravity for the entity.

        :param gravity: Gravity value to be applied to the entity
        """

        self.gravity = gravity

    def land(self):
        """
        Handles the landing of the entity when it hits the ground.
        """
        self.is_hitting_ground = True
        self.vel.y = 0
        self.jump = False
        self.fall = False

    def hit_head(self):
        """
        Handles the entity hitting its head on a ceiling or platform above it.
        """
        self.vel.y = 0
        self.jump = False
    
    def hit_wall(self):
        """
        Handles the entity hitting a wall on its left or right side.
        """
        ...

    def update(self):
        """
        Updates the entity's position, velocity, and animation. 
        Should be called every frame
        """
        super().update()
        self.update_sprite()
        others = [obj for obj in GlobalVariables.get_variable("game_objects") if obj.id != self.id]
        self.collided_objs = get_collided_objects(self, "solid", others, self.vel.x, self.vel.y)
        on_ground = False

        for obj in self.collided_objs:
            if obj[1] == "top" and obj[1] not in ["left", "right"]:
                self.land()
                on_ground = True
            if obj[1] == "bottom":
                self.hit_head()
            if obj[1] == "left":
                self.hit_wall()
                self.vel.x = 0
                if self.direction == "left":
                    self.vel.x = -0.1
            if obj[1] == "right":
                self.hit_wall()
                self.vel.x = 0
                if self.direction == "right":
                    self.vel.x = 0.1

        if not on_ground:
            self.fall = True
        else:
            self.fall = False

        if self.gravity and self.fall:
            self.vel.y += self.gravity

        if self.vel.x != 0 and self.collided_objs:
            for obj in self.collided_objs:
                if obj[1] in ["left", "right"]:
                    if obj[1] == "left":
                        self.set_position((obj[0].rect.left - self.rect.width, self.pos.y))
                    else:
                        self.set_position((obj[0].rect.right, self.pos.y))

        if self.vel.y != 0 and self.collided_objs:
            for obj in self.collided_objs:
                if obj[1] in ["top", "bottom"]:
                    if obj[1] == "top":
                        self.set_position((self.pos.x, obj[0].rect.top - self.rect.height))
                    else:
                        self.set_position((self.pos.x, obj[0].rect.bottom))
                    break

        self.set_position((self.pos.x + self.vel.x, self.pos.y + self.vel.y))

        self.is_hitting_ground = False

    def update_sprite(self):
        """
        Updates the entity's sprite based on its current state (idle, running, jumping, falling, etc.).
        """
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
        """
        Sets the sprite for the entity.

        :param name: Name of the sprite to be set
        """
        if name in self.animations:
            anim = self.animations[name]
            if isinstance(anim, Animation):
                self.set_animation(anim)
            elif isinstance(anim, Texture):
                self.set_texture(anim)

    def set_sfx_list(self, sfx_list):
        self.sfx_list = sfx_list
