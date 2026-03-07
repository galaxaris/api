import math

import pygame

from api.GameObject import GameObject
from api.utils import GlobalVariables


class Projectile(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int],shot_speed: float, shot_angle: float, gravity: float, effect: str = None, target: str = None):
        super().__init__(pos, size)
        self.add_tag("solid")
        self.shot_speed = shot_speed
        self.shot_angle = shot_angle
        self.gravity = gravity


    def update(self):
        vx = self.shot_speed * math.cos(self.shot_angle)
        vy = -self.shot_speed * math.sin(self.shot_angle)

        virtual_traj = self.pos.copy()
        for i in range(50):
            obstacles = []
            game_objects = GlobalVariables.get_variable("game_objects")
            for game_object in game_objects:
                if "solid" in game_object.tags:
                    obstacles.append(game_object)

            position = self.pos

            virtual_point = pygame.Rect(virtual_traj.x + GlobalVariables.get_variable("cam_pos").x,
                                        virtual_traj.y + GlobalVariables.get_variable("cam_pos").y, 4, 4)

            hit = False
            for obstacle in obstacles:
                if virtual_point.colliderect(obstacle.rect):
                    hit = True
                    break

            if hit:
                break

            vy += self.gravity

            position += pygame.Vector2(vx, vy)




