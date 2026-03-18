"""Dialog container that converts scripted lines into text boxes."""
from api.UI.Choice import Choice
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
        self.dialogs: list[tuple[str, str | Choice, str]] = []
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

    def add_message(self, character_name: str, dialog: str, key_point: str= None):
        """Append a message to the dialog sequence.

        :param key_point:
        :param character_name: Speaker identifier.
        :param dialog: Message content.
        :return:
        """
        self.dialogs.append((character_name, dialog, key_point))

    def add_choice(self, character_name: str, choice: Choice, key_point: str= None):
        """Append a choice message to the dialog sequence.

        Choice messages are rendered with a different style and close the dialog after interaction.

        :param choice:
        :param key_point:
        :param character_name: Speaker identifier.
        :return:
        """
        self.dialogs.append((character_name, choice, key_point))

    def add_stop(self):
        """Append a stop marker to the dialog sequence.

        Stop markers are invisible and non-interactive, but can be used to split the dialog into sections.

        :return:
        """
        self.dialogs.append((None, None, "stop"))

    def get_dialogs(self):
        """Build concrete textbox instances for the whole dialog sequence.

        Each line resolves speaker texture/side and sets a goal marker that
        indicates whether the next interaction should continue or close.

        :return: Ordered list of `TextBox` objects.
        """
        dialogs = []
        for character_name, dialog, key_point in self.dialogs:
            if character_name is None:
                dialogs.append(None)
            if isinstance(dialog, Choice):
                setattr(dialog, "key_point", key_point)
                dialogs.append(dialog)
                continue
            character_texture = None
            character_side = "left"
            for name, texture, side in self.characters:
                if name == character_name:
                    character_texture = texture
                    character_side = side
                    break
            textbox = TextBox(character_name, dialog, texture=character_texture, image_side=character_side, font=self.font, closable=True)
            textbox.key_point = key_point
            dialogs.append(textbox)
        return dialogs

