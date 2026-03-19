"""Dialog container that converts scripted lines into text boxes."""
from api.UI.Choice import Choice
from api.UI.TextBox import TextBox
from api.UI.GameUI import UIElement
from api.assets.Resource import ResourceType, Resource
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

    def go_to(self, key_point: str):
        """Append a go-to marker to the dialog sequence.

        Go-to markers are invisible and non-interactive, but can be used to jump to a specific key point in the dialog.

        :param key_point: Key point identifier to jump to.
        :return:
        """
        self.dialogs.append((None, None, key_point))

    def add_stop(self):
        """Append a stop marker to the dialog sequence.

        Stop markers are invisible and non-interactive, but can be used to split the dialog into sections.

        :return:
        """
        self.dialogs.append((None, None, "stop"))

    def add_choice(self, character_name: str, text: str, choices: list, key_point: str = None):
        """Append a choice message to the dialog sequence.

        Choice messages are rendered with a different style and close the dialog after interaction.

        :param character_name: Speaker identifier.
        :param text: The prompt/question text shown to the player.
        :param choices: List of choice tuples (text, goal, [optional callback]).
        :param key_point: Optional marker to jump to.
        :return:
        """
        character_texture = None
        for name, texture, side in self.characters:
            if name == character_name:
                character_texture = texture
                break

        choice = Choice(font=self.font, title=character_name, text=text, texture=character_texture)

        # Safely unpack the choices list, handling optional callbacks
        for choice_data in choices:
            c_text = choice_data[0]
            c_goal = choice_data[1]
            c_callback = choice_data[2] if len(choice_data) > 2 else None

            choice.add_choice(c_text, c_goal, c_callback)

        self.dialogs.append((character_name, choice, key_point))

    def setup(self, dialog_data: dict, resource: Resource = None):
        """Build the dialog sequence from a dictionary structure."""
        characters = dialog_data.get("characters", [])
        for char in characters:
            # Fallback check for both "texture" and "icon" keys
            texture = char.get("texture") or char.get("icon")

            if isinstance(texture, str):
                if resource:
                    texture = Texture(texture, resource)
                else:
                    texture = None
            self.add_character(char["name"], texture, char.get("side", "left"))

        for entry in dialog_data.get("messages", []):
            # Prevent crashes if someone types ("STOP") instead of ("STOP",)
            if isinstance(entry, str):
                entry = (entry,)

            length = len(entry)

            if length == 4:
                # Format: ("Name", "Question?", [choices], "key_point")
                self.add_choice(entry[0], entry[1], entry[2], entry[3])

            elif length == 3:
                if isinstance(entry[2], list):
                    # Format: ("Name", "Question?", [choices])
                    self.add_choice(entry[0], entry[1], entry[2])
                else:
                    # Format: ("Name", "Message text", "key_point")
                    self.add_message(entry[0], entry[1], entry[2])

            elif length == 2:
                if entry[0] == "GOTO":
                    # Format: ("GOTO", "key_point")
                    self.go_to(entry[1])
                else:
                    # Format: ("Name", "Message text")
                    self.add_message(entry[0], entry[1])

            elif length == 1:
                if entry[0] == "STOP":
                    # Format: ("STOP",)
                    self.add_stop()
                else:
                    print(f"[Dialog.setup] Warning: Unrecognized 1-length command: {entry}")
            else:
                print(f"[Dialog.setup] Warning: Invalid dialog entry format: {entry}")


    def get_dialogs(self):
        """Build concrete textbox instances for the whole dialog sequence.

        Each line resolves speaker texture/side and sets a goal marker that
        indicates whether the next interaction should continue or close.

        :return: Ordered list of `TextBox` objects.
        """
        dialogs = []
        print(self.dialogs)
        for character_name, dialog, key_point in self.dialogs:
            if character_name is None:
                if key_point == "stop":
                    dialogs.append(None)
                elif key_point is not None:
                    marker = TextBox("", "", font=self.font)
                    marker.key_point = key_point
                    marker.add_tag("ui_dialog_goto")
                    dialogs.append(marker)
                continue
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

