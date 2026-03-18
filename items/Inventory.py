import pygame as pg
import math

from pygame import Vector2

from api.GameObject import GameObject
from api.utils import Inputs


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

    def add_weapon(self, pistol):
        self.weapons.append(pistol)

    def get_current(self):
        return self.weapons[self.active_index] if self.weapons else None

    def update(self, scene=None):
        super().update(self)


    def draw(self, surface, scene=None):

        if not self.weapons or not self.player_rect:
            return

        else:

            self.mouse = pg.Vector2(Inputs.get_mouse(Inputs.get_key_pressed("show_inventory")))

            cam_pos = scene.camera.position
            player_screen_pos = self.player_pos - cam_pos + self.player_size / 2
            self.mouse_angle_radians = self.mouse / scene.scale_ratio - player_screen_pos
            math.radians(self.mouse_angle_radians.x)
            math.radians(self.mouse_angle_radians.y)

            player_center = pg.Vector2(self.player_rect.center)

            angle_step = math.pi / 4

            all_circle_pos = []

            for i, weapon in enumerate(self.weapons):

                angle = -math.pi / 2 + (i * angle_step)

                # this offset is the distance between circles
                offset_x = math.cos(angle) * self.radius
                offset_y = math.sin(angle) * self.radius

                circle_pos = pg.Vector2(
                    player_center.x + offset_x,
                    player_center.y + offset_y
                )

                all_circle_pos.append(circle_pos)


                if i == self.active_index:
                    colour = "red"

                else:
                    colour = "blue"

                # FIXME: the mouse angle and the circle position angle don't match, making weapon selection impossible
                if angle - math.radians(10) <= math.atan2(self.mouse_angle_radians.x, self.mouse_angle_radians.y) <= angle + math.radians(10):
                    colour = "green"
                    print(angle)
                    print(self.mouse_angle_radians)



                camera_offset = scene.camera.position if scene else pg.Vector2(0, 0)
                pg.draw.circle(surface, colour, circle_pos - camera_offset, 10  )


            super().draw(surface)

        #utilise les propriétés des gameobject pour dessiner l'ui

