import math
import pygame
import random

from api.utils import GlobalVariables
from api.utils.Constants import OFFSET_X, OFFSET_Y


class Trajectory:
    entity_pos : pygame.Vector2
    shot_angle: float
    shot_speed : int
    gravity: float
    def __init__(self, player_pos: pygame.Vector2, shot_speed: int, gravity: float, mouse_pos: pygame.Vector2):
        self.angle_radians = None
        self.entity_pos = player_pos
        self.shot_speed = shot_speed
        self.gravity = gravity
        self.trajectory_coordinates = []
        self.mouse_pos = mouse_pos
        self.entity_screen_pos = pygame.Vector2(0,0)
        self.initial_position = pygame.Vector2(0,0)

    def build_trajectory_coordinates(self):
        self.trajectory_coordinates.clear()
        cam_pos = GlobalVariables.get_variable("cam_pos")
        self.entity_screen_pos = self.entity_pos - cam_pos


        dx, dy = self.mouse_pos / GlobalVariables.get_variable("scale_ratio") - self.entity_screen_pos


        self.angle_radians = math.atan2(-dy, dx)

        if self.mouse_pos == (0, 0):
            self.angle_radians = 0

        vx = self.shot_speed * math.cos(self.angle_radians)
        vy = -self.shot_speed * math.sin(self.angle_radians)

        for i in range(50):
            self.trajectory_coordinates.append(self.entity_screen_pos + i*pygame.Vector2(vx, vy))
            vy += self.gravity

    def draw_trajectory(self, surface):

        trajectory_coordinates = self.trajectory_coordinates
        for point in trajectory_coordinates:
            point_x = point[0]
            point_y = point[1]

            colour_choices = ["white", "yellow"]
            pygame.draw.circle(surface, random.choice(colour_choices), (int(point_x), int(point_y)), 2)

            pygame.draw.circle(surface, "green", (self.entity_pos[0], self.entity_pos[1]), 5)