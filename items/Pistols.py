import math

import pygame as pg
from dataclasses import dataclass


from api.items.Item import Item
from api.entity.Projectile import Projectile
from api.physics.Trajectory import Trajectory
from api.utils.Constants import DEFAULT_GRAVITY

class Pistol(Item):
    """Base class for pistol."""
    def __init__(self, trajectory: Trajectory, gravity: float|int = DEFAULT_GRAVITY, name: str = "gun", item_type: str = "active_gun", target: str = "enemy", cooldown: int = 500):
        super().__init__(name, item_type)
        self.show_trajectory = True
        self.projectiles = []
        self.trajectory = trajectory
        self.is_aiming = False
        self.gravity = gravity
        self.cooldown = cooldown
        self.Time = None
        self.last = - self.cooldown
        self.target = target

    def shoot(self, shoot_pos: pg.Vector2)->bool:
        game_projectiles = self.projectiles
        now = pg.time.get_ticks()

        if now - self.last >= self.cooldown:
            self.last = now
            projectile = Projectile(shoot_pos, self.gravity, self.trajectory.ini_speed, self.trajectory.angle_radians, target=self.target)
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

class ProjectileEssence(Item):
    """Base class for projectile essence, it is what will give a projectile its gravity, effect, target, sprite"""
    def __init__(self, name, item_type, gravity, effect, target, sprite):
        super().__init__(name, item_type)
        self.gravity = gravity
        self.effect = effect
        self.target = target
        self.sprite = sprite






