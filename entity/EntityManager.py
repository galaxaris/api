import pygame as pg


class EntityManager:
    """
    Manages all entities in the game, including their creation, updating, and rendering.
    """
    def __init__(self, scene):

        self.entities = []

    def add_entity(self, entity):
        """
        Adds an entity to the manager.

        :param entity: The entity to add
        """
        self.entities.append(entity)

    def update(self, dt):
        """
        Updates all entities.

        :param dt: Time delta since last update
        """
        for entity in self.entities:
            entity.update(dt)

    def render(self, surface: pg.Surface):
        """
        Renders all entities onto the given surface.

        :param surface: The surface to render on
        """
        for entity in self.entities:
            entity.render(surface)
