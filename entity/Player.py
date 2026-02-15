from api.entity.Entity import Entity
from api.utils.Inputs import get_inputs
import pygame as pg

class Player(Entity):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        super().__init__(pos, size)
        self.velocity = velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.force = force
        self.boost = False
        self.add_tag("player")

    def update(self, others):
        inputs = get_inputs()
        boost_val = 1 if self.boost else 0


        if inputs["right"]:
            if self.vel.x < (self.velocity + boost_val):
                self.vel.x += self.acceleration
                self.set_direction("right")
        else:
            if self.vel.x > 0:
                self.vel.x -= self.resistance
                if self.vel.x < 0:
                    self.vel.x = 0

        if inputs["left"]:
            if self.vel.x > -(self.velocity + boost_val):
                self.vel.x -= self.acceleration
                self.set_direction("left")
        else:
            if self.vel.x < 0:
                self.vel.x += self.resistance
                if self.vel.x > 0:
                    self.vel.x = 0

        if inputs["jump"] and self.jump == False:
            gravity = self.gravity if self.gravity else 1
            self.vel.y += -self.acceleration * max(1,gravity) * self.force
            self.jump = True


        if inputs["boost"]:
            self.boost = True
        else:
            self.boost = False



        super().update(others)