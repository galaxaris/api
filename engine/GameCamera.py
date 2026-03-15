"""Camera system used to navigate and focus the scene."""

from typing import Optional

import pygame as pg

from api.GameObject import GameObject
from api.utils import Debug
from api.utils.Inputs import get_inputs


class GameCamera:
    """
    GameCamera class. Handles the camera's position, movement, and focus on game objects.
    """
    def __init__(self, position: tuple[int, int]):
        """
        Initializes the GameCamera with a starting position.

        :param position: Starting position of the camera
        """

        self.limit_bottomright : Optional[pg.Vector2] = None
        self.limit_topleft : Optional[pg.Vector2] = None
        self.position : pg.Vector2 = pg.Vector2(position)
        self.offset : pg.Vector2  = pg.Vector2(0, 0)
        self.focused_object : Optional[GameObject] = None
        self.freecam_old = self.position.copy()
        self.camera_mode = "Free"

    def move(self, dx: float, dy: float):
        """
        Move the camera by a delta.

        :param dx: Horizontal delta.
        :param dy: Vertical delta.
        :return:
        """
        self.position.x += dx
        self.position.y += dy

    def focus(self, game_object: GameObject):
        """
        Focus the camera on a specific game object.

        :param game_object: Target object to track.
        :return:
        """
        self.focused_object = game_object

    def set_offset(self, offset: tuple[int, int] | tuple[float, float] | pg.Vector2):
        """
        Set camera offset relative to the focused object.

        :param offset: Offset applied to focused object position.
        :return:
        """
        self.offset = pg.Vector2(offset)

    def set_limits(self, topleft: tuple[int , int], bottomright: tuple[int , int]):
        """
        Sets the field of view limits

        :param topleft: Top left corner of the field of view
        :param bottomright: Bottom right corner of the field of view
        """
        self.limit_topleft = pg.Vector2(topleft)
        self.limit_bottomright = pg.Vector2(bottomright)

    def set_position(self, position: tuple[int, int] | tuple[float, float] | pg.Vector2):
        """
        Teleport the camera to an absolute position.

        :param position: New absolute camera position.
        :return:
        """
        self.position = pg.Vector2(position)


    def update(self):
        """
        Update camera mode and position for the current frame.

        In freecam mode, movement follows live directional inputs. Otherwise,
        the camera follows the focused object and optionally clamps to configured
        boundaries.

        :return:
        """

        if Debug.is_enabled("freecam"):
            self.camera_mode = "Freecam"
            if not self.freecam_old:
                self.freecam_old = self.position.copy()


            inputs = get_inputs()
            boost = 5 if inputs["boost"] else 0

            if inputs["right"]:
                self.move(5+boost, 0)
            if inputs["left"]:
                self.move(-5-boost, 0)
            if inputs["down"]:
                self.move(0, 5+boost)
            if inputs["up"]:
                self.move(0, -5-boost)

        elif self.focused_object and hasattr(self.focused_object, 'pos'):
            if self.limit_topleft and self.limit_bottomright:
                target_x = max(self.limit_topleft.x, min(self.focused_object.pos.x - self.offset.x, self.limit_bottomright.x))
                target_y = max(self.limit_topleft.y, min(self.focused_object.pos.y - self.offset.y, self.limit_bottomright.y))
            else:
                target_x = self.focused_object.pos.x - self.offset.x
                target_y = self.focused_object.pos.y - self.offset.y

            self.camera_mode = self.focused_object.__class__.__name__
            self.position.x = int(target_x)
            self.position.y = int(target_y)
        else:
            if self.freecam_old:
                self.position = self.freecam_old.copy()
                self.freecam_old = None
            self.camera_mode = "Free"
