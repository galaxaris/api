import pygame as pg

from api.UI.GameUI import UIElement
from api.utils import Inputs


class Modal(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int] = (50, 50, 50)):
        super().__init__(pos, size)
        self.elements: list[UIElement] = []
        self.buttons = [[]]  # 2D list to store buttons in a grid
        self.active_button_index_y = 0
        self.active_button_index_x = 0
        self.menu_surface = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.color = color
        self.margin = pg.Vector2(10, 10)
        self.add_tag("ui_menu")
        self.add_tag("ui_block")

    def add_element(self, element: UIElement, x: int = 0):
        self.elements.append(element)
        if "ui_button" in element.tags:
            element.idle()
            element.set_global_margin(self.margin + self.pos)
            while len(self.buttons) <= x:
                self.buttons.append([])
            self.buttons[x].append(element)


    def update(self):

        if self.buttons:
            actual_button = self.buttons[self.active_button_index_x][self.active_button_index_y%len(self.buttons[self.active_button_index_x])]

            if Inputs.is_controller_connected():
                inputs = Inputs.get_once_inputs()

                for lines in self.buttons:
                    for button in lines:
                        if button != actual_button:
                            button.idle()

                if inputs["menu_down"]:
                    self.active_button_index_y = (self.active_button_index_y + 1) % len(self.buttons[self.active_button_index_x])
                elif inputs["menu_up"]:
                    self.active_button_index_y = (self.active_button_index_y - 1) % len(self.buttons[self.active_button_index_x])
                elif inputs["menu_right"]:
                    self.active_button_index_x = (self.active_button_index_x + 1) % len(self.buttons)
                elif inputs["menu_left"]:
                    self.active_button_index_x = (self.active_button_index_x - 1) % len(self.buttons)

                actual_button.focus()

                if inputs["menu_select"]:
                    actual_button.click()
            else:
                actual_button.idle()

        for element in self.elements:
            element.update()

    def draw(self, surface: pg.Surface, offset=pg.Vector2(0, 0)):
        super().draw(surface, offset)
        # Add a margin for the elements to avoid drawing them right at the edge of the modal
        self.menu_surface.fill((0,0,0,0))
        self.set_color(self.color)
        for element in self.elements:
            element.draw(self.menu_surface, offset)

        self.image.blit(self.menu_surface, self.margin)


