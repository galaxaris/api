from api.UI.GameUI import UIElement
from api.assets.Texture import Texture
import pygame as pg

from api.utils import Inputs, GlobalVariables
from api.utils.Fonts import get_font


class Button(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str = None, font: str = "arial"):
        super().__init__(pos, size)
        self.text = text
        self.font = font
        self.default_texture = None
        self.hover_texture = None
        self.click_texture = None
        self.callback = None
        self.color_text = (0,0,0)
        self.menu_offset = (0, 0)
        self.state = "default"
        self.add_tag("ui_button")

    def define_texture(self, default: Texture, hover: Texture, click: Texture):
        self.default_texture = default
        self.hover_texture = hover
        self.click_texture = click
        self.image = self.default_texture.image
        self.rect = self.image.get_rect(topleft=self.pos)

    def click(self, color: tuple[int, int, int] = (255, 0, 0)):
        self.state = "click"
        if self.click_texture:
            self.image = self.click_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a red border if no click texture is defined
            pg.draw.rect(self.image, color, self.image.get_rect(), 2)

            self.draw_text(color)
        if self.callback:
            self.callback(self)

    def idle(self, color: tuple[int, int, int] = (255, 255, 255)):
        self.state = "default"
        if self.default_texture:
            self.image = self.default_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a white border if no default texture is defined
            self.draw_text(color)


    def focus(self, color: tuple[int, int, int] = (188, 188, 188)):
        self.state = "hover"
        if self.hover_texture:
            self.image = self.hover_texture.image
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            #Mark a red border if no hover texture is defined
            pg.draw.rect(self.image, color, self.image.get_rect(), 2)
            self.draw_text(color)

    def draw_text(self, color):
        self.image.fill(color)
        text = get_font(self.font, 20).render(self.text, False, self.color_text)
        text_rect = text.get_rect(center=(self.size.x // 2, self.size.y // 2))
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_callback(self, callback):
        self.callback = callback

    def set_global_margin(self, margin):
        self.menu_offset = margin

    def update(self):
        super().update()

        if Inputs.is_controller_connected():
            return

        raw_mouse = Inputs.get_mouse() - self.menu_offset
        ratio = GlobalVariables.get_variable("scale_ratio")
        mouse_pos = (raw_mouse[0] // ratio, raw_mouse[1] // ratio)
        self.rect.topleft = self.pos + self.menu_offset//2

        if self.rect.collidepoint(mouse_pos):
            if Inputs.is_mouse_clicked_once():
                self.click()
            else:
                self.focus()
        else:
            self.idle()

