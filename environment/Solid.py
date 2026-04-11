"""Solid world colliders used for physics interactions."""

from api.GameObject import GameObject
import pygame as pg

class Solid(GameObject):
    """Static collider object tagged as solid."""

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2):
        """Initialize a solid collider.

        :param pos: Collider position.
        :param size: Collider size.
        """
        super().__init__(pos, size)
        self.add_tag("solid")

    def update(self, scene=None):
        """Update the solid object.

        :return:
        """
        super().update(scene)

    def set_state(self, state):
        if(state):
            self.add_tag("solid")
        else:
            self.remove_tag("solid")

    def get_state(self):
        return "solid" in self.tags

    def toggle(self):
        self.set_state(not self.get_state())
