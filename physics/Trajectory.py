"""Projectile trajectory preview utilities."""

import math
import colorsys
import random

import pygame as pg

def free_fall(ini_pos: pg.Vector2, ini_speed: float, angle: float, gravity: float, t: float) -> pg.Vector2:
    """Free fall trajectory preview utility."""
    return pg.Vector2(ini_pos.x + math.cos(angle) * ini_speed * t, ini_pos.y + 0.5 * gravity * t**2 - math.sin(angle) * ini_speed * t)

def linear_trajectory(ini_pos: pg.Vector2, ini_speed: float, angle: float, gravity: float, t: float) -> pg.Vector2:
    """Linear trajectory preview utility. To be used for the grappling hook projectile"""
    return pg.Vector2(ini_pos.x + math.cos(angle) * ini_speed * t, ini_pos.y - math.sin(angle) * ini_speed * t)

def calculate_required_speed_from_freefall(gravity, target_range, angle_rad, delta_y):
    """
    gravity: positive (ex: 0.5)
    target_range: distance x (positive)
    angle_rad: angle de tir
    delta_y: différence de hauteur (y_start - y_target)
             Note: Dans Pygame, si la cible est plus haute, delta_y est positif.
    """
    g = abs(gravity)
    x = abs(target_range)
    y = delta_y
    theta = angle_rad

    # Formule physique complète pour v0
    # v0 = sqrt( (g * x^2) / (2 * cos(theta)^2 * (x * tan(theta) - y)) )

    cos_a = math.cos(theta)
    tan_a = math.tan(theta)

    # Le dénominateur ne doit pas être <= 0 (angle impossible pour cette cible)
    denom = 2 * (cos_a ** 2) * (x * tan_a - y)

    if denom <= 0:
        return 50  # Valeur de secours si le tir est impossible

    return math.sqrt((g * x ** 2) / denom)


def apply_accuracy(base_angle, accuracy):
    # On définit l'erreur maximale (ex: 20 degrés en radians)
    max_error = math.radians(20)
    error_range = max_error * (1.0 - accuracy)

    return base_angle + error_range

class Trajectory:
    """Builds and renders a predicted ballistic path."""
    def __init__(self, kinematic_equation, ini_pos: pg.Vector2, ini_speed: float|int, angle_radians: float, gravity: float|int, color: tuple[int, int, int] = (200, 200, 200)):
        self.kinematic_equation = kinematic_equation
        self.ini_pos = ini_pos
        self.ini_speed = ini_speed
        self.angle_radians = angle_radians
        self.gravity = gravity

        self.color = color
        h, s, v = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
        v = min(v + 0.1, 1.0)
        s = max(s - 0.2, 0.0)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.bright_color = (r*255, g*255, b*255)

    def get_pos(self, t: float | int) -> pg.Vector2:
        return self.kinematic_equation(self.ini_pos, self.ini_speed, self.angle_radians, self.gravity, t)

    def draw(self, surface: pg.Surface, scene, max_points: int, player_pos: pg.Vector2 = (0, 0)) -> None :
        time_step = 3 #sec
        step = 0
        collided = False

        offset = player_pos
        offset2 = player_pos - scene.camera.position

        obstacles = [obj for obj in scene.game_objects if "solid" in obj.tags]
        obstacles += [obj for obj in scene.game_objects if "entity" in obj.tags]
        obstacles = [obj for obj in obstacles if obj.pos != player_pos]

        render_width, render_height = scene.get_width(), scene.get_height()

        to_enemy = 0
        while not collided and max_points > 0:
            pos = self.get_pos(step)
            draw_pos = pos + offset2
            pos += offset

            #we don't continue if we are out of cam WARNING, IS ONLY PERTINENT IF THE TRAJECTORY DOES NOT DO A U TURN
            if 0 > pos.x > render_width and 0 > pos.y > render_height:
                collided = True

            else:
                virtual_point = pg.Rect(pos.x, pos.y, 4, 4)
                for obstacle in obstacles:
                    if "entity" in obstacle.tags and virtual_point.colliderect(obstacle.rect):
                        to_enemy += 1
                        if to_enemy > 1: collided = True
                        break
                    elif obstacle.tags and virtual_point.colliderect(obstacle.rect):
                        collided = True
                        break





            if not collided:
                pg.draw.circle(surface, self.color if int(step/time_step)%2 == 0 else self.bright_color, draw_pos, 2)

            step += time_step
            max_points -= 1