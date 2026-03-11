"""Entity abstraction with movement, collisions, and animation state."""

from typing import Optional

from pygame.surface import Surface

from api.GameObject import GameObject
from api.assets.Animation import Animation
import pygame as pg

from api.assets.Texture import Texture
from api.physics.Collision import get_collided_objects
from api.utils import Debug

#TODO: Player is kind of shaking
#TODO: Remove clipping
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


    def __init__(self, pos: tuple[int, int], size: tuple[int, int], max_velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        """
        Initializes the entity with the given attributes.

        :param pos: Entity position
        :param size: Entity size
        """
        super().__init__(pos, size)
        self.max_velocity = 0
        self.acceleration = 0
        self.resistance = 0
        self.force = 0
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
        self.is_controlled = False
        self.start_pos = pg.Vector2(pos)
        self.set_physics_properties(max_velocity, acceleration, resistance, force)
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

        [ADVICE] 9.8 should be the Earth-like default gravity

        :param gravity: Gravity value to be applied to the entity
        """

        self.gravity = gravity/20 #Divided by 20 so 10 ~= 9.8 m/s**2 would be the default gravity!
        self.displayed_gravity = gravity

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

    def update(self, scene=None):
        """
        Updates the entity's position, velocity, and animation. 
        Should be called every frame
        """
        super().update(scene)
        self.update_sprite()
        others = [obj for obj in scene.game_objects if obj.id != self.id]
        on_ground = False

        # Gets normalized frame factor (1.0 ~= one frame at target FPS).
        Time = scene.Time
        

        if not Debug.is_enabled("freecam") and not self.is_controlled:
            if self.vel.x > 0:
                self.vel.x = max(0, self.vel.x - self.resistance * Time.deltaTime)
            elif self.vel.x < 0:
                self.vel.x = min(self.vel.x + self.resistance * Time.deltaTime, 0)

        next_dx = self.vel.x * Time.deltaTime
        next_dy = self.vel.y * Time.deltaTime
        self.collided_objs = get_collided_objects(self, "solid", others, next_dx, next_dy)

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
            self.vel.y += self.gravity * Time.deltaTime

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


        self.set_position((self.pos.x + self.vel.x * Time.deltaTime, self.pos.y + self.vel.y * Time.deltaTime))

        self.is_hitting_ground = False
        self.is_controlled = False

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

    def set_physics_properties(self, max_velocity: float, acceleration: float, resistance: float, force: float):
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.force = force
        self.resistance = resistance

    def do_jump(self):
        if not self.jump:
            gravity = self.gravity if self.gravity else 1
            self.vel.y += -self.acceleration * max(1, gravity) * self.force
            self.jump = True

            # SFX
            if self.sfx_list:
                if "jump" in self.sfx_list:
                    audio_manager = self.audio_manager
                    if audio_manager:
                        audio_manager.play_sfx("jump", allow_overlap=False)

    def respawn(self):
        """
        Kills the player.

        Working: the player is respawned at the starting position (temporarily)

        :return:
        """
        self.vel = pg.Vector2(0, 0)
        self.set_position(self.start_pos)

    def kill(self):
        """
        Kills the player.

        Working: the player is respawned at the starting position (temporarily)

        :return:
        """
        self.respawn()

    def do_right(self, Time):
        boost_val = 1 if self.boost else 0
        self.vel.x = max(0, min(self.vel.x + self.acceleration * Time.deltaTime, self.max_velocity + boost_val))

    def do_left(self, Time):
        boost_val = 1 if self.boost else 0
        self.vel.x = max(-(self.max_velocity + boost_val), min(self.vel.x - self.acceleration * Time.deltaTime, 0))