"""Solid world colliders used for physics interactions."""

from api.GameObject import GameObject
import pygame as pg

class Solid(GameObject):
    """Static collider object tagged as solid."""

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        """Initialize a solid collider.

        :param pos: Collider position.
        :param size: Collider size.
        """
        super().__init__(pos, size)
        self.add_tag("solid")

    def update(self):
        """Update the solid object.

        :return:
        """
        super().update()
