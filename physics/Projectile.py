import math

import pygame

from api.GameObject import GameObject
from api.physics.Trajectory import Trajectory
from api.utils import GlobalVariables


class Projectile(GameObject):
    def __init__(self, pos: tuple[int, int],shot_speed: float, shot_angle: float, gravity: float, trajectory: list[pygame.Vector2], effect: str = None, target: str = None):
        self.pos = pos
        self.shot_speed = shot_speed
        self.shot_angle = shot_angle
        self.gravity = gravity
        self.rect = pygame.Rect(self.pos, (10, 10))
        self.vx = self.shot_speed * math.cos(self.shot_angle)
        self.vy = -self.shot_speed * math.sin(self.shot_angle)
        self.trajectory = trajectory


    def update_position(self, coordinate: pygame.Vector2) :

        self.rect.topleft = (int(coordinate.x), int(coordinate.y))


    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = (0, 0)):
        draw_pos = (self.rect.x, self.rect.y)

        pygame.draw.circle(surface, "blue", draw_pos, 5)







