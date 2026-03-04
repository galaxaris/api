import pygame as pg

from api.UI.GameUI import UIElement


class Modal(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int] = (50, 50, 50)):
        super().__init__(pos, size)
        self.elements: list[UIElement] = []
        self.menu_surface = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.color = color
        self.add_tag("ui_menu")
        self.add_tag("ui_block")

    def add_element(self, element: UIElement):
        self.elements.append(element)

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self, surface: pg.Surface, offset=pg.Vector2(0, 0)):
        super().draw(surface, offset)
        # Add a margin for the elements to avoid drawing them right at the edge of the modal
        self.menu_surface.fill((0,0,0,0))
        self.set_color(self.color)
        for element in self.elements:
            element.draw(self.menu_surface, offset)

        self.image.blit(self.menu_surface, (10, 10))


