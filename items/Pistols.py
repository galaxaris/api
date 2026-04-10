import math

import pygame as pg

from api.entity.Projectile import Projectile
from api.physics.Trajectory import Trajectory

class WaterPistol:
    """Base class for a pistol whose projectile is water."""
    def __init__(self, trajectory: Trajectory, target = "enemy", cooldown = 500, projectile_damage = 10):
        self.name = "water gun"
        self.target = "enemy" #dirty
        self.cooldown = cooldown
        self.show_trajectory = True
        self.projectiles = []
        self.trajectory = trajectory
        self.is_aiming = False
        self.gravity = 0.5
        self.Time = None
        self.last = - self.cooldown
        self.projectile_damage = projectile_damage
        self.max_points = 300

    def shoot(self, shoot_pos: pg.Vector2)->bool:
        game_projectiles = self.projectiles
        now = pg.time.get_ticks()

        if now - self.last >= self.cooldown:
            self.last = now
            projectile = Projectile(shoot_pos, self.gravity, self.trajectory.ini_speed, self.trajectory.angle_radians, target=self.target, damage=self.projectile_damage, colour = "blue")
            game_projectiles.append(projectile)
            return True
        return False

    def update(self, scene=None):
        self.Time = scene.Time
        projectiles = self.projectiles
        length = len(projectiles) - 1
        for i in range(length, -1, -1):
            if not projectiles[i].to_kill:
                scene.add(projectiles[i], "#projectile")
            else:
                scene.remove(projectiles[i], "#projectile")
                projectiles.remove(projectiles[i])



class EarthPistol:
    """Base class for a pistol whose projectile is dirt."""

    def __init__(self, trajectory: Trajectory, target = "enemy", cooldown = 500, projectile_damage = 10):
        self.name = "earth gun"
        self.target = "enemy"
        self.cooldown = cooldown
        self.show_trajectory = True
        self.projectiles = []
        self.trajectory = trajectory
        self.is_aiming = False
        self.gravity = 1
        self.Time = None
        self.last = - self.cooldown
        self.projectile_damage = projectile_damage
        self.max_points = 300


    def shoot(self, shoot_pos: pg.Vector2) -> bool:
        game_projectiles = self.projectiles
        now = pg.time.get_ticks()

        if now - self.last >= self.cooldown:
            self.last = now
            projectile = Projectile(shoot_pos, self.gravity, self.trajectory.ini_speed, self.trajectory.angle_radians,
                                    target=self.target, damage=self.projectile_damage, colour = "red")
            game_projectiles.append(projectile)
            return True
        return False

    def update(self, scene=None):
        self.Time = scene.Time
        projectiles = self.projectiles
        length = len(projectiles) - 1
        for i in range(length, -1, -1):
            if not projectiles[i].to_kill:
                scene.add(projectiles[i], "#projectile")
            else:
                scene.remove(projectiles[i], "#projectile")
                projectiles.remove(projectiles[i])

# FIXME: the grappling projectile is destroyed when it comes back to the player, however you cannot shoot another one

class GrapplingPistol:
    """Base class for a grappling hook."""

    def __init__(self, trajectory: Trajectory, projectile_damage = 0):
        self.name = "grappling gun"
        self.show_trajectory = True
        self.projectile_damage = projectile_damage
        self.trajectory = trajectory
        self.is_aiming = False
        self.projectile = None # no list, instead only one projectile can be shot at once
        self.current_trajectory_ini_speed = 0
        self.current_trajectory_angle_radians = 0
        self.max_points = 10
        self.range = 500 # max distance to be traveled before deletion
        self.range_reached = False # checks if the range is reached to delete upon comeback and not init

    def shoot(self, shoot_pos: pg.Vector2) -> bool:
        # no cooldown contrary to other guns, max distance is used instead

        if not self.projectile:
            projectile = Projectile(shoot_pos, 0, self.trajectory.ini_speed, self.trajectory.angle_radians,
                                    damage=self.projectile_damage, colour = "green", effect = "grappling", range = self.range)

            self.current_trajectory_ini_speed = self.trajectory.ini_speed
            self.current_trajectory_angle_radians = self.trajectory.angle_radians
            self.projectile = projectile
            return True
        return False

    def update(self, scene=None):
        if self.projectile:
            projectile = self.projectile
            if not projectile.to_kill:
                scene.add(projectile, "#projectile")
            else:
                scene.remove(projectile, "#projectile")
                self.projectile = None





