"""Modal menu container with keyboard/controller navigation."""

import pygame as pg

from api.UI.GameUI import UIElement
from api.utils import Inputs
from api.utils.Inputs import prevent_input


class Modal(UIElement):
    """Blocking UI container that can host navigable button grids."""

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int, int] = (30, 30, 30, 220), border_radius: int = 10):
        """Initialize a modal container.

        :param pos: Modal position.
        :param size: Modal size.
        :param color: Background color of the modal panel.
        """
        super().__init__(pos, size)
        self.elements: list[UIElement] = []
        self.buttons = [[]]  # 2D list to store buttons in a grid
        self.active_button_index_y = 0
        self.active_button_index_x = 0
        self.menu_surface = pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        self.color = color
        self.margin = pg.Vector2(10, 10)
        self.border_radius = border_radius
        self.add_tag("ui_menu")
        self.add_tag("ui_block")
        self.add_tag("ui_bypassdebug")

    def add_element(self, element: UIElement, x: int = 0):
        """Add an element and optionally register it in a button column.

        :param element: UI element to add.
        :param x: Column index for button navigation grouping.
        :return:
        """
        self.elements.append(element)
        if "ui_button" in element.tags:
            element.idle()
            element.set_global_margin(self.margin + self.pos)
            while len(self.buttons) <= x:
                self.buttons.append([])
            self.buttons[x].append(element)


    def update(self, scene=None):
        """Update modal content and handle controller button navigation.

        When a controller is connected, directional inputs move within the
        button grid and selection triggers the focused button callback.

        :return:
        """

        if self.buttons:
            actual_button = self.buttons[self.active_button_index_x][self.active_button_index_y%len(self.buttons[self.active_button_index_x])]

            if Inputs.is_controller_connected():
                inputs = Inputs.get_once_inputs()

                for lines in self.buttons:
                    for button in lines:
                        if button != actual_button:
                            button.idle(button.bg_color)

                if inputs["menu_down"]:
                    self.active_button_index_y = (self.active_button_index_y + 1) % len(self.buttons[self.active_button_index_x])
                elif inputs["menu_up"]:
                    self.active_button_index_y = (self.active_button_index_y - 1) % len(self.buttons[self.active_button_index_x])
                elif inputs["menu_right"]:
                    if self.active_button_index_x + 1 < len(self.buttons) and len(self.buttons[self.active_button_index_x + 1]) > 0:
                        self.active_button_index_x = (self.active_button_index_x + 1) % len(self.buttons)
                elif inputs["menu_left"]:
                    if self.active_button_index_x - 1 >= 0 and len(self.buttons[self.active_button_index_x - 1]) > 0:
                        self.active_button_index_x = (self.active_button_index_x - 1) % len(self.buttons)

                actual_button.hover(actual_button.bg_color_hover)

                if inputs["menu_select"]:
                    actual_button.click(actual_button.bg_color_focus)
                    Inputs.prevent_once_key("jump")
                    if actual_button.callback:
                        actual_button.callback(actual_button)
            else:
                actual_button.idle(actual_button.bg_color)

        for element in self.elements:
            element.update(scene)

    def draw(self, surface: pg.Surface, offset=None, scene=None):
        """Render modal and all child elements.

        :param scene:
        :param surface: Destination surface.
        :param offset: Draw offset.
        :return:
        """
        super().draw(surface, offset)
        # Add a margin for the elements to avoid drawing them right at the edge of the modal

        self.menu_surface.fill((0,0,0,0))

        menu_background = pg.Rect(0,0,self.size.x, self.size.y)
        pg.draw.rect(self.image, self.color, menu_background, border_radius=self.border_radius)

        for element in self.elements:
            element.draw(self.menu_surface, offset)

        self.image.blit(self.menu_surface, self.margin)


