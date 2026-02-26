import pygame

from api.items.Item import Item
from api.engine import Scene
from api.entity.Interfaces import AimState
from api.physics.Trajectory import Trajectory

class Weapon(Item):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        pass
    def build_trajectory(self, aim_state: AimState, surface: pygame.Surface):
        # we need a way to get the surface everything should work but we dont have surface
        current_trajectory = Trajectory(aim_state, self.surface)
        current_trajectory.draw_trajectory()
         #self.active_trajectory.get_trajectory_coordinates(self.pos, self.shot_angle, self.shot_speed, self.gravity)

        #Trajectory(pos, shot_angle, shot_speed, gravity)
    def aim(self, aim_state: AimState, surface: pygame.Surface):
        self.build_trajectory(aim_state, surface)
    def shoot(self):
        print("shoot")
        #self.build_trajectory()
