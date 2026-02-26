from api.utils import Debug, State

from api.entity.Entity import Entity
from api.utils.Inputs import get_inputs
from api.physics.Trajectory import Trajectory

import pygame as pg

class Player(Entity):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], max_velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        super().__init__(pos, size)
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.force = force
        self.boost = False
        self.add_tag("player")
        self.active_trajectory = None
        self.shot_angle = 60
        self.shot_speed = 10
        self.gravity = 0.5


    def update(self, others):
        inputs = get_inputs()
        boost_val = 1 if self.boost else 0

        if not Debug.is_enabled("freecam"):
            if inputs["shoot"] and State.is_enabled("player_control"):
                self.vel.x = 0

                if inputs["up"]:
                    self.shot_speed += 1

                if inputs["down"]:
                    self.shot_speed -= 1

                if inputs["right"]:
                    self.shot_angle += 1

                if inputs["left"]:
                    self.shot_angle -= 1

                self.active_trajectory = Trajectory(self.pos, self.shot_angle, self.shot_speed, self.gravity)
                self.active_trajectory.get_trajectory_coordinates(self.pos, self.shot_angle, self.shot_speed, self.gravity)

            else:
                self.active_trajectory = None

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
