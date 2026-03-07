import math

import pygame

from api.items.ActiveItem import ActiveItem
from api.items.Item import Item
from api.physics.Projectile import Projectile
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
    def __init__(self, mouse_pos: pygame.Vector2, active_trajectory: Trajectory, name: str = "gun", item_type: str = "active_gun", is_equipped: bool = True,
                 ammo_gravity: float = DEFAULT_GRAVITY, shot_speed: float = DEFAULT_SHOT_SPEED, is_shooting: bool = False):
        super().__init__(name, item_type, is_equipped)
        self.ammo_gravity = ammo_gravity
        self.shot_speed = shot_speed
        self.mouse_pos = mouse_pos
        self.active_trajectory = active_trajectory
        self.projectile = None
        self.is_shooting = is_shooting

        dx, dy = self.mouse_pos / GlobalVariables.get_variable("scale_ratio") - self.active_trajectory.entity_screen_pos
        self.angle_radians = math.atan2(-dy, dx)

        if self.mouse_pos == (0, 0):
            self.angle_radians = 1

    def shoot(self):
        self.projectile = Projectile(self.active_trajectory.entity_screen_pos, (10,10), self.shot_speed, self.angle_radians, self.ammo_gravity)




