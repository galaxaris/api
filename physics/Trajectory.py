"""Projectile trajectory preview utilities."""

import math
import pygame
import random

from api.utils import GlobalVariables



class Trajectory:
    """Builds and renders a predicted ballistic path."""

    def __init__(self, player_pos: pygame.Vector2, shot_speed: int, gravity: float, mouse_pos: pygame.Vector2):
        """Initialize a trajectory computation context.

        :param player_pos: Shooter world position.
        :param shot_speed: Initial projectile speed.
        :param gravity: Gravity increment applied per simulation step.
        :param mouse_pos: Cursor position used to compute shoot angle.
        """
        self.angle_radians = None
        self.entity_pos = player_pos
        self.shot_speed = shot_speed
        self.gravity = gravity
        self.trajectory_coordinates = []
        self.mouse_pos = mouse_pos
        self.entity_screen_pos = pygame.Vector2(0,0)
        self.test_collision = []
        self.trajectory_colour = "blue"

    def build_trajectory_coordinates(self):
        """Compute trajectory points until max steps or collision.

        The preview is generated in screen space relative to the current camera.
        Simulation stops early when a predicted point intersects a solid object.

        :return:
        """
        self.trajectory_coordinates.clear()
        cam_pos = GlobalVariables.get_variable("cam_pos")
        self.entity_screen_pos = self.entity_pos - cam_pos

        dx, dy = self.mouse_pos / GlobalVariables.get_variable("scale_ratio") - self.entity_screen_pos

        self.angle_radians = math.atan2(-dy, dx)

        if self.mouse_pos == (0, 0):
            self.angle_radians = 1

        vx = self.shot_speed * math.cos(self.angle_radians)
        vy = -self.shot_speed * math.sin(self.angle_radians)

        virtual_traj = self.entity_screen_pos.copy()

        # offset = GlobalVariables.get_variable("offset")

        # cam_pos = GlobalVariables.get_variable("cam_pos")

        # camera_limit_topleft = GlobalVariables.get_variable("camera_limit_topleft") + cam_pos + offset
        # camera_limit_bottomright = GlobalVariables.get_variable("camera_limit_bottomright") + cam_pos + offset


        # print("camera_limit_topleft", camera_limit_topleft)
        # print("camera_limit_bottomright", camera_limit_bottomright)

        # FIXME: Trajectory needs to stop when encountering screen border

        hit = False
        i = 0
        while not hit:
            obstacles = []
            game_objects = GlobalVariables.get_variable("game_objects")
            for game_object in game_objects:
                if "solid" in game_object.tags:
                    obstacles.append(game_object)

            position = self.entity_screen_pos.copy()

            virtual_point = pygame.Rect(virtual_traj.x + cam_pos.x, virtual_traj.y + cam_pos.y,  4, 4)

            for obstacle in obstacles:
                if virtual_point.colliderect(obstacle.rect):
                    hit = True
                    break

                """elif camera_limit_topleft.x > virtual_traj.x > camera_limit_bottomright.y or camera_limit_topleft.y > virtual_traj.y > camera_limit_bottomright.y:
                    hit = True
                    break"""

            if hit:
                break

            vy += self.gravity

            virtual_traj = position + i*pygame.Vector2(vx, vy)
            self.trajectory_coordinates.append(virtual_traj)
            i += 1

        self.trajectory_coordinates.pop(-1)

    def draw_trajectory(self, surface):
        """Draw previously computed trajectory points.

        :param surface: Destination surface.
        :return:
        """

        trajectory_coordinates = self.trajectory_coordinates
        for point in trajectory_coordinates:
            pygame.draw.circle(surface, self.trajectory_colour, (int(point[0]), int(point[1])), 2)


