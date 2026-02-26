from api.GameObject import GameObject
import pygame as pg

from api.utils import State
from api.utils.Inputs import get_once_inputs


class UIElement(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], is_blocking: bool = False):
        super().__init__(pos, size)
        self.goal = None
        self.add_tag("ui")

class GameUI(pg.Surface):
    elements: dict[str,UIElement]
    enabled_elements = list[str]
    size: pg.Vector2
    active_textbox: tuple[str, UIElement] | None
    def __init__(self, size: tuple[int, int]):
        super().__init__(size, pg.SRCALPHA, 32)
        self.convert_alpha()
        self.elements: dict[str,UIElement] = {}
        self.enabled_elements = []
        self.active_textbox = None
        self.size = pg.Vector2(size)

    def add(self, key: str, element: UIElement):
        if key not in self.elements:
            self.elements[key] = element

    def remove(self, key: str):
        if key in self.elements:
            del self.elements[key]
            if key in self.enabled_elements:
                self.enabled_elements.remove(key)

    def show(self, key: str):
        if key in self.elements and key not in self.enabled_elements:
            self.enabled_elements.append(key)
            if "ui_textbox" in self.elements[key].tags:
                self.active_textbox = (key,self.elements[key])

    def hide(self, key: str):
        if key in self.enabled_elements:
            self.enabled_elements.remove(key)
            
    def update(self):
        inputs = get_once_inputs()
        if inputs["interact"] and self.active_textbox and "ui_closable" in self.active_textbox[1].tags and not State.is_enabled("in_menu"):
            self.hide(self.active_textbox[0])
            self.active_textbox = None
            State.toggle("player_control", True)


    def draw(self, surface: pg.Surface):
        self.fill((0, 0, 0, 0))
        for key in self.enabled_elements:
            element = self.elements[key]
            if "ui_block" in element.tags:
                State.toggle("player_control", False)
            if "ui_textbox" in element.tags and self.active_textbox[1].id != element.id:
                continue
            element.draw(self)
        surface.blit(self, (0, 0))