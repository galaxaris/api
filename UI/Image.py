from api.UI.GameUI import UIElement
from api.assets.Texture import Texture

class Image(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], texture: Texture):
        super().__init__(pos, size)
        self.texture = texture
        self.image = self.texture.image
        self.rect = self.image.get_rect(topleft=self.pos)