import math
import pygame
import random

class Trajectory:
    player_pos : pygame.math.Vector2
    shot_angle: int
    shot_speed : int
    gravity: float
    def __init__(self, initial_shot_position: pygame.math.Vector2, shot_angle: int, shot_speed: int, gravity: float):
        self.initial_shot_position = initial_shot_position
        self.shot_angle = shot_angle
        self.shot_speed = shot_speed
        self.gravity = gravity
        self.trajectory_coordinates = []

    def get_trajectory_coordinates(self, player_pos: pygame.math.Vector2, shot_angle : int, shot_speed: int, gravity: float):
        self.trajectory_coordinates.clear()

        rad = math.radians(shot_angle)
        vx = shot_speed * math.cos(rad)
        vy = -shot_speed * math.sin(rad)

        initial_x = float(player_pos[0] + 32)
        initial_y = float(player_pos[1] + 16)

        for i in range(50):
            self.trajectory_coordinates.append((int(initial_x), int(initial_y)))
            vy += gravity
            initial_x += vx
            initial_y += vy

    def draw_trajectory(self, surface, offset):
        trajectory_coordinates = self.trajectory_coordinates
        for point in trajectory_coordinates:
            point_x = point[0] - offset.x
            point_y = point[1] - offset.y

            colour_choices = ["red", "blue", "green", "yellow", "cyan", "magenta"]
            pygame.draw.circle(surface, random.choice(colour_choices), (int(point_x), int(point_y)), 2)








