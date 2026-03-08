import math

import pygame

from api.items.ActiveItem import ActiveItem
from api.items.Item import Item
from api.entity.Projectile import Projectile
from api.physics.Trajectory import Trajectory
from api.utils import GlobalVariables
from api.utils.Constants import DEFAULT_GRAVITY, DEFAULT_SHOT_SPEED


class HealthPotion(Item):
    """Base class for health potion."""
    quantity: int
    def __init__(self, name, item_type):
        """Initialize the health potion."""
        pass

class Grapple(ActiveItem):
    """Base class for grapple."""
    def __init__(self, name, item_type, is_equipped: bool):
        super().__init__(name, item_type, is_equipped)
        pass



class Pistol(ActiveItem):
    """Base class for pistol."""
    def __init__(self, active_trajectory: Trajectory, projectile_gravity = DEFAULT_GRAVITY, name: str = "gun", item_type: str = "active_gun", is_equipped: bool = True,
                is_shooting: bool = False):
        super().__init__(name, item_type, is_equipped)
        self.active_trajectory = active_trajectory
        self.shot_speed = self.active_trajectory.shot_speed
        self.angle_radians = self.active_trajectory.angle_radians
        self.is_shooting = is_shooting
        self.projectile = None
        self.projectile_gravity = projectile_gravity

    def shoot(self):
        self.projectile = Projectile(self.active_trajectory.entity_screen_pos, self.projectile_gravity, self.active_trajectory.initial_velocity, self.active_trajectory.angle_radians)
        GlobalVariables.get_variable("game_objects").append(self.projectile)
        self.projectile.update()




