from api.entity.Character import Character
import pygame as pg

class Player(Character):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], velocity = 2, acceleration = 0.5, resistance = 0.2, force = 20):
        super().__init__(pos, size)
        self.velocity = velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.force = force
        self.boost = False
        self.add_tag("player")

    def update(self, others):
        keys_pressed = pg.key.get_pressed()
        boost_val = 1 if self.boost else 0

        if keys_pressed[pg.K_d] and self.vel.x < (self.velocity + boost_val):
            self.vel.x += self.acceleration
            self.set_direction("right")
        if keys_pressed[pg.K_q] and self.vel.x > -(self.velocity + boost_val):
            self.vel.x -= self.acceleration
            self.set_direction("left")
        if keys_pressed[pg.K_SPACE] and self.jump == False:
            gravity = self.gravity if self.gravity else 1
            self.vel.y += -self.acceleration * max(1,gravity) * self.force
            self.jump = True

        if keys_pressed[pg.K_LSHIFT]:
            self.boost = True
        else:
            self.boost = False

        if self.vel.x > 0:
            self.vel.x -= self.resistance
            if self.vel.x < 0:
                self.vel.x = 0
        elif self.vel.x < 0:
            self.vel.x += self.resistance
            if self.vel.x > 0:
                self.vel.x = 0
        if self.vel.y < 0:
            self.vel.y += self.resistance
            if self.vel.y > 0:
                self.vel.y = 0

        super().update(others)