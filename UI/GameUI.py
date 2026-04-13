"""UI orchestration surface for dialogs, menus, and overlays."""

from api.GameObject import GameObject
from api.utils import InputManager, Debug
from api.utils.InputManager import onKeyUp
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
        self.add_tag("ui")

    def draw(self, surface: pg.Surface, scene=None):
        super().draw(surface, scene=scene)

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
        self.active_menus = []

        self.size = pg.Vector2(size)


    def add(self, key: str, element: UIElement):
        """Register a UI element under a key.

        :param key: Unique UI key.
        :param element: UI element instance.
        :return:
        """
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

    def update(self, scene):
        """Advance UI interaction state from one-shot player inputs."""

        #consume=False is essential because several cases are checked in the same time.
        release_menu_select = onKeyUp("menu_select", consume=False)
        release_interact = onKeyUp("interact", consume=False)
        confirm_released = release_menu_select or release_interact

        # Helper to DRY up repetitive UI closing and state restoration
        def close_ui(ui_key):
            self.hide(ui_key)
            scene.global_state["player_control"] = True

        #Consumes effectively after the choice.
        def consume_confirm_release():
            if release_menu_select:
                InputManager.prevent_released_key("menu_select")
            if release_interact:
                InputManager.prevent_released_key("interact")

        # 1. Dialog and Textbox Progression
        if confirm_released and not scene.global_state.get("in_menu"):
            if self.active_dialog:
                key, boxes, index = self.active_dialog
                is_waiting_for_choice = hasattr(self.active_textbox[1], "choice_goal")

                if not is_waiting_for_choice:
                    consume_confirm_release()
                    if index < len(boxes) - 1:
                        new_index = index + 1
                        self.active_dialog = (key, boxes, new_index)
                        next_box = boxes[new_index]

                        if next_box and "ui_dialog_goto" in next_box.tags:
                            target_index = next(
                                (i for i, box in enumerate(boxes)
                                 # ADD THE CONDITION BELOW: ignore other goto markers
                                 if box and getattr(box, "key_point",
                                                    None) == next_box.key_point and "ui_dialog_goto" not in box.tags),None
                            )
                            if target_index is not None:
                                next_box = boxes[target_index]
                                self.active_dialog = (key, boxes, target_index)  # Update the actual index!
                            else:
                                next_box = None
                        if next_box is not None:
                            self.active_textbox = (key, next_box)
                            InputManager.prevent_input("menu_select")
                        else:
                            #Do not forget to consume input, otherwise the first key press after closing the dialog will be lost
                            InputManager.prevent_input("menu_select")
                            close_ui(key)
                            
                    else:
                        InputManager.prevent_input("menu_select")
                        close_ui(key)
                        

            elif self.active_textbox:
                key, element = self.active_textbox
                is_waiting_for_choice = hasattr(element, "choice_goal")

                if not is_waiting_for_choice and "ui_closable" in element.tags:
                    consume_confirm_release()
                    close_ui(key)

        # 2. Choice Handling
        if self.active_textbox and "ui_choice" in self.active_textbox[1].tags:
            _, element = self.active_textbox
            choice_target = getattr(element, "choice_goal", None)

            if choice_target is not None and self.active_dialog:
                key, boxes, index = self.active_dialog
                element.choice_goal = None  # Consume the choice

                # Safely find the target index, avoiding IndexError if not found
                target_index = next(
                    (i for i, box in enumerate(boxes)
                     if box and getattr(box, "key_point", None) == choice_target),
                    None
                )
                InputManager.prevent_input("menu_select")

                if target_index is not None and target_index != index:
                    self.active_dialog = (key, boxes, target_index)
                    if boxes[target_index] is not None:
                        self.active_textbox = (key, boxes[target_index])
                    else:
                        if index + 1 < len(boxes):
                            self.active_textbox = (key, boxes[index + 1])
                        else:
                            InputManager.prevent_input("menu_select")
                            close_ui(key)
                else:
                    if index + 1 < len(boxes):
                        self.active_textbox = (key, boxes[index + 1])
                    else:
                        InputManager.prevent_input("menu_select")
                        close_ui(key)

        # 3. Menu Interactions
        #if self.active_menus and onKeyUp("pause"):
        #    # Close the most recently opened menu
        #    self.hide(self.active_menus[-1])

        # 4. Global State Synchronization
        # Evaluated AFTER inputs so state is accurate on the current frame
        in_menu = len(self.active_menus) > 0
        scene.global_state["in_menu"] = in_menu
        scene.global_state["player_control"] = not in_menu

        # 5. Update Elements
        for key in self.enabled_elements:
            self.elements[key].update(scene)

    def draw(self, surface: pg.Surface, scene=None):
        """Render enabled UI elements onto the destination surface.

        The method also applies modal darkening for active menus and toggles
        player-control state when blocking UI is displayed.

        :param scene:
        :param surface: Final destination surface.
        :return:
        """
        self.fill((0, 0, 0, 0))

        #PLAYER CONTROL: Reenable by default player control, but check if in future, other components will desactivate player control
        #Override : Prevent player control from being reenabled if "override_player_control" is active, allowing other systems to take full control when needed (e.g., cutscenes, special interactions)
        if not scene.global_state["override_player_control"]:
            if len(self.active_menus) == 0:
                scene.global_state["player_control"] = True

        for key in self.enabled_elements:
            element = self.elements[key]

            if Debug.is_enabled("debug_info") and "ui_bypassdebug" not in element.tags:
                continue

            # If it's the active dialog/textbox, draw the specific current box
            if self.active_textbox and key == self.active_textbox[0]:
                self.active_textbox[1].draw(self)
                self.active_textbox[1].update(scene)
                if "ui_block" in self.active_textbox[1].tags:
                    scene.global_state["player_control"] = False
                continue

            if len(self.active_menus) != 0:
                self.fill((0, 0, 0, 128))  # Semi-transparent overlay when a menu is open
                scene.global_state["player_control"] = False  # Disable player control when any menu is active

            # Draw other non-dialog UI elements normally
            element.draw(self)

        surface.blit(self, (0, 0))