"""UI orchestration surface for dialogs, menus, and overlays."""

from api.GameObject import GameObject
from api.utils import State
from api.utils.Inputs import get_once_inputs
import pygame as pg

class UIElement(GameObject):
    """Base class for UI objects managed by `GameUI`."""

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], is_blocking: bool = False):
        """Initialize a UI element.

        :param pos: Element position.
        :param size: Element size.
        :param is_blocking: Reserved flag for blocking behavior.
        """
        super().__init__(pos, size)
        self.goal = None
        self.add_tag("ui")

class GameUI(pg.Surface):
    """Manages UI elements visibility, interaction flow, and rendering."""

    elements: dict[str, UIElement]
    enabled_elements: list[str]
    size: pg.Vector2
    active_textbox: tuple[str, UIElement] | None

    # New tracking for Dialogs
    active_dialog: tuple[str, list, int] | None  # (key, list_of_boxes, current_index)
    active_menus: list[str]

    def __init__(self, size: tuple[int, int]):
        """Initialize the UI manager.

        :param size: Render size of the UI surface.
        """
        super().__init__(size, pg.SRCALPHA, 32)
        self.convert_alpha()
        self.elements = {}
        self.enabled_elements = []
        self.active_textbox = None
        self.active_dialog = None
        self.size = pg.Vector2(size)
        self.active_menus = []

    def add(self, key: str, element: UIElement):
        """Register a UI element under a key.

        :param key: Unique UI key.
        :param element: UI element instance.
        :return:
        """
        if key not in self.elements:
            self.elements[key] = element

    def show(self, key: str):
        """Enable a UI element and initialize related runtime state.

        Dialog entries are expanded into textboxes and the first one is made
        active. Menus are tracked in opening order to support stacked closing.

        :param key: Key of the element to show.
        :return:
        """
        if key in self.elements and key not in self.enabled_elements:
            element = self.elements[key]
            self.enabled_elements.append(key)

            # Handle Dialog Initialization
            if "ui_dialog" in element.tags:
                textboxes = element.get_dialogs()
                if textboxes:
                    self.active_dialog = (key, textboxes, 0)
                    # The first textbox of the dialog becomes the active visual element
                    self.active_textbox = (key, textboxes[0])

            # Handle Single Textbox Initialization
            if "ui_textbox" in element.tags:
                self.active_textbox = (key, element)

            if "ui_menu" in element.tags:
                self.active_menus.append(key)


    def hide(self, key: str):
        """Disable a UI element and clear active references tied to it.

        :param key: Key of the element to hide.
        :return:
        """
        if key in self.enabled_elements:
            self.enabled_elements.remove(key)
            if self.active_textbox and self.active_textbox[0] == key:
                self.active_textbox = None
            if self.active_dialog and self.active_dialog[0] == key:
                self.active_dialog = None
            if key in self.active_menus:
                self.active_menus.remove(key)

    def update(self):
        """Advance UI interaction state from one-shot player inputs.

        This method handles dialog progression, closable textboxes, and menu
        stack closing while synchronizing gameplay state flags.

        :return:
        """
        inputs = get_once_inputs()
        if inputs["interact"] and not State.is_enabled("in_menu"):
            if self.active_dialog:
                key, boxes, index = self.active_dialog
                if index < len(boxes) - 1:
                    # Move to next box in dialog
                    new_index = index + 1
                    self.active_dialog = (key, boxes, new_index)
                    self.active_textbox = (key, boxes[new_index])
                else:
                    # End of dialog reached
                    self.hide(key)
                    State.toggle("player_control", True)
            elif self.active_textbox:
                # Single Textbox Logic
                key, element = self.active_textbox
                if "ui_closable" in element.tags:
                    self.hide(key)
                    State.toggle("player_control", True)

        if inputs["pause"] and self.active_menus:
            # Close the most recently opened menu
            print("Closing menu:", self.active_menus[-1])
            last_menu_key = self.active_menus[-1]
            self.hide(last_menu_key)
            if len(self.active_menus) == 0:
                State.toggle("in_menu", False)
                State.toggle("player_control", True)

    def draw(self, surface: pg.Surface):
        """Render enabled UI elements onto the destination surface.

        The method also applies modal darkening for active menus and toggles
        player-control state when blocking UI is displayed.

        :param surface: Final destination surface.
        :return:
        """
        self.fill((0, 0, 0, 0))

        #PLAYER CONTROL: Reenable by default player control, but check if in future, other components will desactivate player control
        #Override : Prevent player control from being reenabled if "override_player_control" is active, allowing other systems to take full control when needed (e.g., cutscenes, special interactions)
        if not State.is_enabled("override_player_control"):
            if len(self.active_menus) == 0:
                State.toggle("player_control", True)

        for key in self.enabled_elements:
            element = self.elements[key]

            # If it's the active dialog/textbox, draw the specific current box
            if self.active_textbox and key == self.active_textbox[0]:
                self.active_textbox[1].draw(self)
                if "ui_block" in self.active_textbox[1].tags:
                    State.toggle("player_control", False)
                continue

            if len(self.active_menus) != 0:
                self.fill((0, 0, 0, 128))  # Semi-transparent overlay when a menu is open
                State.toggle("player_control", False)

            # Draw other non-dialog UI elements normally
            element.draw(self)

        surface.blit(self, (0, 0))