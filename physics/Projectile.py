import math

import pygame

from api.GameObject import GameObject
from api.utils import GlobalVariables


class Projectile(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int],shot_speed: float, shot_angle: float, gravity: float, effect: str = None, target: str = None):
        super().__init__(pos, size)
        self.add_tag("projectile")
        self.shot_speed = shot_speed
        self.shot_angle = shot_angle
        self.gravity = gravity
        self.rect = pygame.Rect(self.pos, (10, 10))
        self.vx = self.shot_speed * math.cos(self.shot_angle)
        self.vy = -self.shot_speed * math.sin(self.shot_angle)


    def update(self):

        self.vy += self.gravity

        self.pos[0] += self.vx
        self.pos[1] += self.vy

        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2 = (0, 0)):
        cam_pos = GlobalVariables.get_variable("cam_pos")
        draw_pos = (self.rect.x - cam_pos.x, self.rect.y - cam_pos.y)

        pygame.draw.circle(surface, (255, 255, 0), draw_pos, 5)







