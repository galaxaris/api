"""Dialog container that converts scripted lines into text boxes."""

from api.UI.TextBox import TextBox
from api.UI.GameUI import UIElement
from api.assets.Texture import Texture


class Dialog(UIElement):
    """Defines a multi-line dialog sequence with character metadata."""

    def __init__(self, font: str = "aptos"):
        """Initialize an empty dialog sequence.

        :param font: Font used when creating text boxes.
        """
        super().__init__((0,0), (0,0), False)
        self.characters: list[tuple[str, Texture, str]] = []
        self.dialogs: list[tuple[str, str]] = []
        self.font = font
        self.add_tag("ui_dialog")
        self.add_tag("ui_bypassdebug")

    def add_character(self, name: str, texture: Texture, side: str = "left"):
        """Register a character entry for dialog rendering.

        :param name: Character identifier.
        :param texture: Portrait texture.
        :param side: Portrait side (`"left"` or `"right"`).
        :return:
        """
        self.characters.append((name, texture, side))

    def add_message(self, character_name: str, dialog: str):
        """Append a message to the dialog sequence.

        :param character_name: Speaker identifier.
        :param dialog: Message content.
        :return:
        """
        self.dialogs.append((character_name, dialog))

    def get_dialogs(self):
        """Build concrete textbox instances for the whole dialog sequence.

        Each line resolves speaker texture/side and sets a goal marker that
        indicates whether the next interaction should continue or close.

        :return: Ordered list of `TextBox` objects.
        """
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
            textbox = TextBox(character_name, dialog, texture=character_texture, image_side=character_side, goal=goal_dialog, font=self.font, closable=True)
            dialogs.append(textbox)
        return dialogs

