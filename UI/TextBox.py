from typing import Optional

import pygame as pg
from pygame.surface import Surface

from api.UI.UI import UIElement
from api.assets.Texture import Texture
from api.utils.Fonts import get_font
from api.utils import Inputs


#Color process [COLOR(R,V,B)][/COLOR]
def process_text(font, args) -> list[Surface]:
    text_content = []
    for line in args:
        if line:
            text_surface = get_font(font, 14).render(line, False, (255, 255, 255))
            text_content.append(text_surface)
    return text_content

def process_title(title: str, font: str) -> Surface:
    return get_font(font, 32).render(title, False, (255, 255, 255))

class TextBox(UIElement):
    title : Surface
    text : list[Surface]
    image : Optional[Surface]
    image_side : str
    closable : bool
    font : str
    def __init__(self, title: str, text: str = "", font: str = "aptos", image_side: str = "left", texture: Texture = None, closable: bool = True, goal = "fermer"):
        super().__init__((0, 0), (0, 0))
        self.title = process_title(title, font)
        self.font = font
        self.text = process_text(self.font, text)
        self.image_side = image_side
        self.closable = closable
        self.goal = goal
        self.image = None
        self.set_image(texture, image_side)
        self.add_tag("ui_textbox")
        self.add_tag("ui_block")
        self.add_tag("ui_closable")

    def set_text(self, font , *text):
        self.text = process_text(font, text)

    def set_image(self, texture: Texture, image_side: str = "left"):
        if texture:
            self.image = texture.image
            self.image_side = image_side
        else:
            self.image = None

    def set_title(self, title: str, font: str):
        self.title = process_title(title, font)

    def draw(self, surface: pg.Surface, offset = (0,0), game_objects = None):
        margin = 10
        width = surface.get_width() - margin*2
        height = surface.get_height()//3

        text_box = pg.Surface((width, height), pg.SRCALPHA, 32).convert_alpha()
        IMAGE_SIZE = (height - margin*2, height - margin*2)
        if self.image.get_size() != IMAGE_SIZE:
            self.image = pg.transform.scale(self.image, IMAGE_SIZE)
        text_box.fill((0, 0, 0, 200))

        text_surface = pg.Surface((width - margin*2, height - margin*2), pg.SRCALPHA, 32).convert_alpha()
        text_surface.fill((0, 0, 0, 0))

        text_surface.blit(self.title, (0, 0))
        line_y = self.title.get_height() + 5


        for line in self.text:
            text_surface.blit(line, (0, line_y))
            line_y += line.get_height() + 5

        close_text = f"Appuyer sur {Inputs.get_hint_input("interact").upper()} pour {self.goal}"
        close_surface = get_font(self.font, 14).render(close_text, False, (177, 177, 177))
        text_surface.blit(close_surface, (0, line_y))


        if self.image:
            if self.image_side == "left":
                text_box.blit(text_surface, (self.image.get_width() + margin*2, margin))
                text_box.blit(self.image, (margin, margin))
            else:
                text_box.blit(text_surface, (margin, margin))
                text_box.blit(self.image, (width - self.image.get_width() - margin, margin))
        else:
            text_box.blit(text_surface, (margin, margin))

        surface.blit(text_box, (self.pos.x + margin, surface.get_height() - height - margin))
