from api.engine import Scene
from api.physics.Trajectory import Trajectory
from api.utils.Constants import MIN_SHOT_SPEED, MAX_SHOT_SPEED, DEFAULT_SHOT_ANGLE, DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY
from api.items.Weapon import Weapon
from api.entity.Interfaces import AimState
from api.utils import Debug, State

from api.entity.Entity import Entity
from api.utils.Inputs import get_inputs

import pygame as pg

class Player(Entity):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], direction = "right", max_velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        super().__init__(pos, size)
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.force = force
        self.boost = False
        self.add_tag("player")
        self.active_trajectory = None
        self.set_direction(direction)
        self.shot_angle = DEFAULT_SHOT_ANGLE
        self.shot_speed = DEFAULT_SHOT_SPEED
        self.gravity = DEFAULT_GRAVITY
        # self.scene = scene
        #self.weapon = Weapon()

    def update(self, others):
        inputs = get_inputs()
        boost_val = 1 if self.boost else 0

        if not Debug.is_enabled("freecam"):

            if inputs["shoot"]:
                self.vel.x = 0

                if inputs["up"]:
                    self.shot_angle += 1

                if inputs["down"]:
                    self.shot_angle -= 1

                if inputs["right"]:
                    self.shot_speed += 1

                if inputs["left"]:
                    self.shot_speed -= 1

                self.active_trajectory = Trajectory(self.pos, self.shot_angle, self.shot_speed, self.gravity)
                self.active_trajectory.build_trajectory_coordinates(self.pos, self.shot_angle, self.shot_speed, self.gravity)

            else:
                self.active_trajectory = None
                self.shot_angle = DEFAULT_SHOT_ANGLE
                self.shot_speed = DEFAULT_SHOT_SPEED

                if inputs["right"] and State.is_enabled("player_control"):
                    if self.vel.x < (self.max_velocity + boost_val):
                        self.vel.x += self.acceleration
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
            super().update(others)


    def draw(self, surface, offset = pg.Vector2(0, 0), game_objects = None):

        super().draw(surface, offset, game_objects)

        if self.active_trajectory:
            self.active_trajectory.draw_trajectory(surface, offset)

