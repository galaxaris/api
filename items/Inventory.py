import pygame as pg
import math

from api.GameObject import GameObject
from api.utils import InputManager


class Inventory(GameObject):
    def __init__(self):
        super().__init__(pos=(0,0), size=(0,0))
        self.weapons = []  # Liste de Pistol
        self.active_index = 0
        self.radius = 60
        self.player_rect = None
        self.mouse_angle_radians = 0
        self.player_pos = pg.Vector2(0,0)
        self.player_size = pg.Vector2(0,0)
        self.mouse = pg.Vector2(0, 0)
        self.all_inventory_slots = []
        self.index_to_switch = 0

    def add_weapon(self, pistol):
        self.weapons.append(pistol)

    def get_current(self):
        return self.weapons[self.active_index] if self.weapons else None

    def switch_weapon(self):
        self.active_index = self.index_to_switch

    def update(self, scene=None):
        super().update(self)


    def draw(self, surface, scene=None):

        if not self.weapons or not self.player_rect:
            return

        else:

            self.mouse = pg.Vector2(InputManager.get_player_aim_vector(InputManager.get_key_pressed("show_inventory")))

            cam_pos = scene.camera.position
            player_screen_pos = self.player_pos - cam_pos + self.player_size / 2
            self.mouse_angle_radians = self.mouse / scene.scale_ratio - player_screen_pos
            self.mouse_angle_radians.x = math.radians(self.mouse_angle_radians.x)
            self.mouse_angle_radians.y = math.radians(self.mouse_angle_radians.y)

            player_center = pg.Vector2(self.player_rect.center)

            angle_step = math.pi / 4


            for i, weapon in enumerate(self.weapons):

                angle = -math.pi / 2 + (i * angle_step)

                # this offset is the distance between circles
                offset_x = math.cos(angle) * self.radius
                offset_y = math.sin(angle) * self.radius

                circle_pos = pg.Vector2(
                    player_center.x + offset_x,
                    player_center.y + offset_y
                )

                self.all_inventory_slots.append([i,circle_pos])

                if i == self.active_index:
                    colour = "red"

                else:
                    colour = "blue"

                if angle - 0.3 <= - math.atan2(self.mouse_angle_radians.x, self.mouse_angle_radians.y) + math.pi/2 <= angle + 0.3:
                    self.index_to_switch = i
                    colour = "green"


                camera_offset = scene.camera.position if scene else pg.Vector2(0, 0)
                pg.draw.circle(surface, colour, circle_pos - camera_offset, 10  )


            super().draw(surface)

