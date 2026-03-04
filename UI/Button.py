from api.UI.GameUI import UIElement
from api.assets.Texture import Texture


class Button(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str = None, font: str = "arial"):
        super().__init__(pos, size)
        self.text = text
        self.font = font
        self.default_texture = None
        self.hover_texture = None
        self.click_texture = None
        self.callback = None
        self.state = "default"

    def define_texture(self, default: Texture, hover: Texture, click: Texture):
        self.default_texture = default
        self.hover_texture = hover
        self.click_texture = click
        self.image = self.default_texture.image
        self.rect = self.image.get_rect(topleft=self.pos)

    def set_callback(self, callback):
        self.callback = callback

    def update(self):
        pass