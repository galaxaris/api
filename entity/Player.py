"""
API's Player utilities
"""

from api.GameObject import GameObject
from api.physics.Trajectory import Trajectory
from api.utils.Constants import MIN_SHOT_SPEED, MAX_SHOT_SPEED, DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY
from api.utils import Debug, State, Inputs

from api.entity.Entity import Entity
from api.utils.Inputs import get_inputs

from api.Game import Game


import pygame as pg

class Player(Entity):
    """
    Player class, based on Entity class. Contains all the player's attributes and methods.
    """

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], direction = "right", max_velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        """
        Initializes the player with the given attributes.

        :param pos: Player position
        :param size: Player size
        :param direction: Player direction
        :param max_velocity: Player max velocity
        :param acceleration: Player acceleration
        :param resistance: Player resistance
        :param force: Player force
        """
        super().__init__(pos, size)
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.force = force
        self.boost = False
        self.add_tag("player")
        self.active_trajectory = None
        self.set_direction(direction)
        self.shot_speed = DEFAULT_SHOT_SPEED
        self.gravity = DEFAULT_GRAVITY

        self.start_pos = pos

    def update(self):
        """
        Updates the player's position and velocity based on the inputs and the player's current state.

        :return:
        """
        inputs = get_inputs()
        boost_val = 1 if self.boost else 0

        if not Debug.is_enabled("freecam"):

            if inputs["aim"] and State.is_enabled("player_control"):
                self.vel.x = 0

                mouse_x, mouse_y = Inputs.get_mouse(Inputs.get_key_pressed("aim"))

                if Inputs.MOUSE_SCROLL > 0 and self.shot_speed < MAX_SHOT_SPEED:
                    self.shot_speed += Inputs.MOUSE_SCROLL
                    Inputs.MOUSE_SCROLL = 0

                elif Inputs.MOUSE_SCROLL < 0 and self.shot_speed > MIN_SHOT_SPEED:
                    self.shot_speed += Inputs.MOUSE_SCROLL
                    Inputs.MOUSE_SCROLL = 0

                self.active_trajectory = Trajectory(self.pos, self.shot_speed, self.gravity, pg.Vector2(mouse_x, mouse_y))
                self.active_trajectory.build_trajectory_coordinates()

                if self.active_trajectory.trajectory_coordinates and self.active_trajectory.trajectory_coordinates[-1][0] < self.pos[0]:
                    self.set_direction("left")
                elif self.active_trajectory.trajectory_coordinates and self.active_trajectory.trajectory_coordinates[-1][0] > self.pos[0]:
                    self.set_direction("right")
                else :
                    pass

            else:
                self.active_trajectory = None
                self.shot_speed = DEFAULT_SHOT_SPEED

            if inputs["right"] and State.is_enabled("player_control"):
                if self.vel.x < (self.max_velocity + boost_val):
                    self.vel.x += self.acceleration
                    if not inputs["aim"]:
                        self.set_direction("right")
                elif self.vel.x > (self.max_velocity + boost_val):
                    self.vel.x = self.max_velocity
            else:
                if self.vel.x > 0:
                    self.vel.x -= self.resistance
                    if self.vel.x < 0:
                        self.vel.x = 0

            if inputs["left"] and State.is_enabled("player_control"):
                if self.vel.x > -(self.max_velocity + boost_val):
                    self.vel.x -= self.acceleration
                    if not inputs["aim"]:
                        self.set_direction("left")
                elif self.vel.x < -(self.max_velocity + boost_val):
                    self.vel.x = -self.max_velocity
            else:
                if self.vel.x < 0:
                    self.vel.x += self.resistance
                    if self.vel.x > 0:
                        self.vel.x = 0

            if inputs["jump"] and self.jump == False and State.is_enabled("player_control"):
                gravity = self.gravity if self.gravity else 1
                self.vel.y += -self.acceleration * max(1,gravity) * self.force
                self.jump = True


            if inputs["boost"] and State.is_enabled("player_control"):
                self.boost = True
            else:
                self.boost = False



        if Debug.is_enabled("freecam"):
            self.vel.x = 0
            self.vel.y = 0
            self.update_sprite()
        else:
            super().update()

    def kill(self):
        """
        Kills the player.

        Working: the player is respawned at the starting position (temporarily)

        :return:
        """
        print("[Player] Player killed, respawning...")
        self.vel = pg.Vector2(0, 0)
        self.set_position(self.start_pos)


    def draw(self, surface, offset = pg.Vector2(0, 0)):
        """
        Draws the player on the given surface.
        
        :param surface: Surface to draw on (usually the game's surface)
        :param offset: Offset to apply to the player's position (for moving camera)
        :return:
        """

        super().draw(surface, offset)

        if self.active_trajectory:
            self.active_trajectory.draw_trajectory(surface)

