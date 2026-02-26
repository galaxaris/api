import math
import pygame
import random

from api.physics.AimState import AimState
from api.utils.Constants import OFFSET_X, OFFSET_Y


class Trajectory:
    aim_state: AimState
    surface: pygame.Surface

    def __init__(self, aim_state: AimState, surface: pygame.Surface):
        self.aim_state = aim_state
        self.aim_state.origin = aim_state.origin
        self.aim_state.shot_angle = aim_state.shot_angle
        self.aim_state.shot_speed = aim_state.shot_speed
        self.aim_state.gravity = aim_state.gravity
        self.trajectory_coordinates = []
        self.surface = surface
        self.build_trajectory_coordinates()
# build trajectory
    def build_trajectory_coordinates(self):
        self.trajectory_coordinates.clear()

        rad = math.radians(self.aim_state.shot_angle)
        vx = self.aim_state.shot_speed * math.cos(rad)
        vy = -self.aim_state.shot_speed * math.sin(rad)

        initial_x = float(self.aim_state.origin[0] + 32)
        initial_y = float(self.aim_state.origin[1] + 16)

        for i in range(50):
            self.trajectory_coordinates.append((int(initial_x), int(initial_y)))
            vy += self.aim_state.gravity
            initial_x += vx
            initial_y += vy

    def draw_trajectory(self):
        surface = pygame.Surface((), pygame.SRCALPHA).convert_alpha()

        pygame.draw.circle(self.surface, "blue", [300, 500], 50)
        for point in self.trajectory_coordinates:
            point_x = point[0] - OFFSET_X
            point_y = point[1] - OFFSET_Y

            colour_choices = ["red", "blue", "green", "yellow", "cyan", "magenta"]
            pygame.draw.circle(self.surface, "red", [300,500], 20, width=20)
            pygame.draw.circle(self.surface, random.choice(colour_choices), (int(point_x), int(point_y)), 2)



            #make a surface then add surface in Scene