from api.UI.Button import Button
from api.UI.GameUI import UIElement
from api.UI.Modal import Modal
from api.UI.TextBox import TextBox
from api.assets.Texture import Texture
from api.utils import Fonts, Inputs
import pygame as pg

class Choice(UIElement):
    """Textbox with buttons for branching dialog or menu options."""

    def __init__(self, font=Fonts.DEFAULT_FONT, title: str = "Title", text: str = "text", texture: Texture = None):
        """Initialize a choice container.

        :param pos: Top-left position of the choice box.
        :param size: Size of the choice box.
        """
        super().__init__((0,0), (0,0))
        self.buttons: list[Button] = []
        self.font = font
        self.title = title
        self.text = text
        self.active_button_index_x = 0
        self.choice_index = -1
        self.choice_goal = None
        self.text_image = texture
        self.add_tag("ui_textbox")
        self.add_tag("ui_choice")
        self.add_tag("ui_block")


    def add_choice(self, text: str, goal: str = "continue", callback = lambda e: None):
        """Add a button to the choice container.

        :param callback:
        :param button: Button element representing a choice.
        :return:
        """
        button = Button((0, 0), (0, 0), text, font=self.font)
        button.set_text(text)
        button.text_color = (255, 255, 255)
        button.bg_color = (30, 30, 30, 220)
        button.bg_color_focus = (30, 30, 30, 170)
        button.bg_color_hover = (40, 40, 40, 200)
        button.goal = goal
        button.callback = lambda e: (setattr(self, "choice_index", self.active_button_index_x), setattr(self, "choice_goal", goal), callback(e))
        self.buttons.append(button)

    def update(self, scene=None):
        """Update choice state and handle button interactions.

        :return:
        """

        if self.buttons:
            actual_button = self.buttons[self.active_button_index_x]

            if Inputs.is_controller_connected():
                inputs = Inputs.get_once_inputs()

                for button in self.buttons:
                    if button != actual_button:
                        button.idle(button.bg_color)

                if inputs["menu_right"]:
                    self.active_button_index_x = (self.active_button_index_x + 1) % len(self.buttons)
                elif inputs["menu_left"]:
                    self.active_button_index_x = (self.active_button_index_x - 1) % len(self.buttons)

                actual_button.hover(actual_button.bg_color_hover)

                if inputs["menu_select"]:
                    print(scene.Time.get_ticks())
                    actual_button.click(actual_button.bg_color_focus)
                    self.choice_index = self.active_button_index_x
                    self.choice_goal = actual_button.goal
                    Inputs.prevent_once_key("jump")
                    if actual_button.callback:
                        actual_button.callback(actual_button)
            else:
                actual_button.idle(actual_button.bg_color)

        for button in self.buttons:
            button.update(scene)

    def draw(self, surface: pg.Surface, scene=None):

        margin = 15
        width = (surface.get_width() - (margin * 2)) // len(self.buttons) - margin//len(self.buttons) + margin//(len(self.buttons)*2)
        height = 30

        posx = margin
        posy = surface.get_height() - height - margin

        text_box = TextBox(self.title, self.text, self.font, closable=False, texture=self.text_image)
        text_box.margin = pg.Vector2(0, -height - margin//len(self.buttons))
        text_box.draw(surface, scene)


        for button in self.buttons:
            button.set_position((posx, posy))
            button.set_size((width, height))
            button.draw(surface, scene)
            posx += width + margin//len(self.buttons)
