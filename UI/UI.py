from api.GameObject import GameObject
import pygame as pg

class UIElement(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.add_tag("ui")

class GameUI(pg.Surface):
    elements: list[UIElement]
    size: pg.Vector2
    def __init__(self, size: tuple[int, int]):
        super().__init__(size, pg.SRCALPHA, 32)
        self.convert_alpha()
        self.elements: list[UIElement] = []
        self.size = pg.Vector2(size)

    def add(self, element: UIElement):
        self.elements.append(element)

    def draw(self, surface: pg.Surface):
        self.fill((0, 0, 0, 0))
        for element in self.elements:
            element.draw(self)
        surface.blit(self, (0, 0))