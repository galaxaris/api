import math

import pygame as pg

from api.GameObject import GameObject
from api.items.ActiveItem import ActiveItem
from api.items.Item import Item
from api.entity.Projectile import Projectile
from api.physics.Trajectory import Trajectory
from api.utils import GlobalVariables
from api.utils.Constants import DEFAULT_GRAVITY, DEFAULT_SHOT_SPEED, DEFAULT_PROJECTILE_GRAVITY

print
class HealthPotion(Item):
    """Base class for health potion."""
    quantity: int
    def __init__(self, name, item_type):
        """Initialize the health potion."""
        super().__init__(name, item_type)

class Grapple(ActiveItem):
    """Base class for grapple."""
    def __init__(self, name, item_type, is_equipped: bool):
        super().__init__(name, item_type, is_equipped)
        pass



class Pistol(ActiveItem):
    """Base class for pistol."""
    def __init__(self, trajectory: Trajectory, projectile_gravity: float = DEFAULT_GRAVITY, name: str = "gun", item_type: str = "active_gun", is_equipped: bool = True):
        super().__init__(name, item_type, is_equipped)
        self.trajectory = trajectory
        self.is_aiming = False
        self.projectile_gravity = projectile_gravity
        self.cooldown = 3000
        self.last = - self.cooldown

    def shoot(self, shoot_pos: pg.Vector2):
        game_projectiles = GlobalVariables.get_variable("projectiles")
        self.last = -self.cooldown
        now = pg.time.get_ticks()

        if now - self.last >= self.cooldown:
            self.last = now
            projectile = Projectile(shoot_pos, self.projectile_gravity, self.trajectory.ini_speed, self.trajectory.angle_radians)
            game_projectiles.append(projectile)



