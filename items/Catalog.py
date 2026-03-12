import math

import pygame as pg

from api.GameObject import GameObject
from api.items.ActiveItem import ActiveItem
from api.items.Item import Item
from api.entity.Projectile import Projectile
from api.physics.Trajectory import Trajectory
from api.utils.Constants import DEFAULT_GRAVITY

class HealthPotion(Item):
    """Base class for health potion."""
    quantity: int
    def __init__(self, name, item_type):
        """Initialize the health potion."""
        super().__init__(name, item_type)

class Pistol(ActiveItem):
    """Base class for pistol."""
    def __init__(self, trajectory: Trajectory, gravity: float = DEFAULT_GRAVITY, name: str = "gun", item_type: str = "active_gun", is_equipped: bool = True):
        super().__init__(name, item_type, is_equipped)
        self.projectiles = []
        self.trajectory = trajectory
        self.is_aiming = False
        self.gravity = gravity
        self.cooldown = 3000
        self.Time = None
        self.last = - self.cooldown

    def shoot(self, shoot_pos: pg.Vector2):
        game_projectiles = self.projectiles
        self.last = -self.cooldown
        now = pg.time.get_ticks()

        if now - self.last >= self.cooldown:
            self.last = now
            projectile = Projectile(shoot_pos, self.gravity, self.trajectory.ini_speed, self.trajectory.angle_radians)
            game_projectiles.append(projectile)

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

