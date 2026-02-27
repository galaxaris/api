from api.UI.TextBox import TextBox
from api.UI.GameUI import UIElement
from api.assets.Texture import Texture


class Dialog(UIElement):
    def __init__(self, font = "aptos"):
        super().__init__((0,0), (0,0), False)
        self.characters: list[tuple[str, Texture, str]] = []
        self.dialogs: list[tuple[str, str]] = []
        self.font = font
        self.add_tag("ui_dialog")

    def add_character(self, name: str, texture: Texture, side: str = "left"):
        self.characters.append((name, texture, side))

    def add_message(self, character_name: str, dialog: str):
        self.dialogs.append((character_name, dialog))

    def get_dialogs(self):
        dialogs = []
        for character_name, dialog in self.dialogs:
            character_texture = None
            character_side = "left"
            for name, texture, side in self.characters:
                if name == character_name:
                    character_texture = texture
                    character_side = side
                    break
            goal_dialog = "continuer" if self.dialogs.index((character_name, dialog)) < len(self.dialogs) - 1 else "fermer"
            textbox = TextBox(character_name, dialog, texture=character_texture, image_side=character_side, goal=goal_dialog, font=self.font)
            dialogs.append(textbox)
        return dialogs

