"""Unified input handling for keyboard, mouse, and controller.

This module normalizes raw device states into game actions and provides both
continuous (`held`) and edge-triggered (`once`) input views.
"""

import os

import pygame as pg
from pygame._sdl2 import controller

MOUSE_SCROLL = 0
MOUSE_CLICKED = set()
PREVIOUS_INPUTS = None
PREVENTED_INPUTS = {}

#%%#################### INPUT MAP ########################
##########################################################

INPUTS = {
    "right": [pg.K_RIGHT, pg.K_d],
    "left": [pg.K_LEFT, pg.K_q],
    "jump": [pg.K_SPACE],
    "boost": [pg.K_LSHIFT, pg.K_RCTRL],
    "up": [pg.K_UP, pg.K_z],
    "down": [pg.K_DOWN, pg.K_s],
    "aim": ["MOUSE_RIGHT", pg.K_LALT],
    "aim_up": [],
    "aim_down": [],
    "shoot": ["MOUSE_LEFT"],
    "show_inventory": [pg.K_TAB],
    "select_weapon": ["MOUSE_LEFT"],
    "interact": [pg.K_e],
    "pause": [pg.K_ESCAPE],
    "menu_up": [],
    "menu_down": [],
    "menu_left": [],
    "menu_right": [],
    "menu_select": [pg.K_RETURN, "MOUSE_LEFT"]
}

CONTROLLER_INPUTS = {
    "right": [("axis", pg.CONTROLLER_AXIS_LEFTX, 16000)],
    "left": [("axis", pg.CONTROLLER_AXIS_LEFTX, -16000)],
    "up": [("axis", pg.CONTROLLER_AXIS_LEFTY, -16000)],
    "down": [("axis", pg.CONTROLLER_AXIS_LEFTY, 16000)],
    "jump": [("button", pg.CONTROLLER_BUTTON_A)],
    "boost": [("axis", pg.CONTROLLER_AXIS_TRIGGERRIGHT, 10000)],
    "interact": [("button", pg.CONTROLLER_BUTTON_A)],
    "aim": [("axis", pg.CONTROLLER_AXIS_TRIGGERLEFT, 10000)],
    "aim_up": [("button", pg.CONTROLLER_BUTTON_RIGHTSHOULDER)],
    "aim_down": [("button", pg.CONTROLLER_BUTTON_LEFTSHOULDER)],
    "shoot":  [("axis", pg.CONTROLLER_AXIS_TRIGGERRIGHT, 10000)],
    "pause": [("button", pg.CONTROLLER_BUTTON_START)],
    "menu_up": [("axis", pg.CONTROLLER_AXIS_LEFTY, -16000),
                ("button", pg.CONTROLLER_BUTTON_DPAD_UP),
                ("axis", pg.CONTROLLER_AXIS_RIGHTY, -16000)],
    "menu_down": [("axis", pg.CONTROLLER_AXIS_LEFTY, 16000),
                    ("button", pg.CONTROLLER_BUTTON_DPAD_DOWN),
                    ("axis", pg.CONTROLLER_AXIS_RIGHTY, 16000)],
    "menu_left": [("axis", pg.CONTROLLER_AXIS_LEFTX, -16000),
                    ("button", pg.CONTROLLER_BUTTON_DPAD_LEFT),
                    ("axis", pg.CONTROLLER_AXIS_RIGHTX, -16000)],
    "menu_right": [("axis", pg.CONTROLLER_AXIS_LEFTX, 16000),
                   ("button", pg.CONTROLLER_BUTTON_DPAD_RIGHT),
                    ("axis", pg.CONTROLLER_AXIS_RIGHTX, 16000)],
    "menu_select": [("button", pg.CONTROLLER_BUTTON_A)]
}

EDITOR_KEYS = {}
_controllers = {}


# Friendly name maps for UI
BRAND_MAPS = {
    "xbox": {
        pg.CONTROLLER_BUTTON_A: "A", pg.CONTROLLER_BUTTON_B: "B",
        pg.CONTROLLER_BUTTON_X: "X", pg.CONTROLLER_BUTTON_Y: "Y",
        pg.CONTROLLER_AXIS_TRIGGERRIGHT: "RT", pg.CONTROLLER_AXIS_TRIGGERLEFT: "LT",
        pg.CONTROLLER_BUTTON_RIGHTSHOULDER: "RB", pg.CONTROLLER_BUTTON_LEFTSHOULDER: "LB"
    },
    "ps": {
        pg.CONTROLLER_BUTTON_A: "\u2715", pg.CONTROLLER_BUTTON_B: "\u25cb",
        pg.CONTROLLER_BUTTON_X: "\u25fd", pg.CONTROLLER_BUTTON_Y: "\u25b3",
        pg.CONTROLLER_AXIS_TRIGGERRIGHT: "R2", pg.CONTROLLER_AXIS_TRIGGERLEFT: "L2",
        pg.CONTROLLER_BUTTON_RIGHTSHOULDER: "R1", pg.CONTROLLER_BUTTON_LEFTSHOULDER: "L1"
    }
}

#%%#################### INPUT LOGIC ########################
############################################################


#%%#################### Editor Input Overrides ########################
#######################################################################

#We have indeed to override because of TKinter (ask to Axel)

def editor_edit_key(key,value):
    """Override a key state when running through the editor layer.

    :param key: Key identifier.
    :param value: Forced pressed state.
    :return:
    """
    EDITOR_KEYS[key] = value

def editor_release_key():
    """Clear all temporary editor key overrides.

    :return:
    """
    global EDITOR_KEYS
    EDITOR_KEYS = {}


#%%#################### Console (XBOX & PS) #########################
#####################################################################
def is_controller_connected():
    """Return whether at least one controller is tracked.

    :return: `True` when a controller is available.
    """
    return len(_controllers) > 0

def get_controller_brand(joy):
    """Infer controller branding from device name.

    :param joy: Controller instance.
    :return: `"ps"` for PlayStation-like names, otherwise `"xbox"`.
    """
    name = joy.name.lower()
    if any(x in name for x in ["playstation", "dualshock", "dualsense", "ps4", "ps5"]):
        return "ps"
    return "xbox"

#### Moteur de calcul d'inputs, appelée dans update_input_state().
#Base de tous les inputs du jeu (ex: get_inputs(), get_once_inputs(), etc.)
def get_inputs():
    """Compute current action states from all connected input devices.

    Keyboard/mouse actions are computed first, then controller actions can
    override them when active.

    :return: Mapping of action names to pressed states.
    """
    current_state = {}
    pg_keys = {}
    if os.environ.get("EDITOR") == "1":
        pg_keys = EDITOR_KEYS
        current_state = {action: any(pg_keys.get(key, False) for key in keys if isinstance(key, int)) for action, keys in INPUTS.items()}
    else:
        pg_keys = pg.key.get_pressed()
        mouse_pressed = pg.mouse.get_pressed()
        current_state = {action: any(pg_keys[key] for key in keys if isinstance(key, int)) for action, keys in INPUTS.items()}
        for action, keys in INPUTS.items():
            is_active = False
            for key in keys:
                if key == "MOUSE_LEFT":
                    if mouse_pressed[0]:  # 0 is Left Click
                        is_active = True
                elif key == "MOUSE_RIGHT":
                    if mouse_pressed[2]:  # 2 is Right Click
                        is_active = True
                elif pg_keys[key]:  # Standard keyboard check
                    is_active = True
            current_state[action] = is_active


    if controller.get_count() > len(_controllers):
        for i in range(controller.get_count()):
            if i not in _controllers:
                _controllers[i] = controller.Controller(i)

    if controller.get_count() == 0:
        _controllers.clear()

    if _controllers:
        joy = _controllers[0]  # Focus on primary player
        for action, inputs in CONTROLLER_INPUTS.items():
            for input_data in inputs:
                input_type = input_data[0]

                if input_type == "button":
                    btn_index = input_data[1]
                    if joy.get_button(btn_index):
                        current_state[action] = True

                elif input_type == "axis":
                    axis_index, threshold = input_data[1], input_data[2]
                    val = joy.get_axis(axis_index)
                    if (0 > threshold > val) or (0 < threshold < val):
                        current_state[action] = True

    for key in list(PREVENTED_INPUTS):
        if not PREVENTED_INPUTS[key] and not current_state[key]:
            del PREVENTED_INPUTS[key]

    for key in current_state:  # Added list() here
        if key in PREVENTED_INPUTS:
            current_state[key] = False
            PREVENTED_INPUTS[key] = False



    return current_state


_cached_once_state = {}
_cached_current_state = {}
_cached_released_state = {}


###### Sauvegarde l'état précédent et calcule l'état actuel pour définir ce qui est maintenu, ce qui vient d'être pressé ou ce qui a été relâché
def update_input_state():
    """
    Refresh cached input snapshots for the current frame.

    Call this once at the beginning of each game-loop iteration. It computes:
    - held states for all actions
    - once states (`just pressed`) by comparing current and previous frames

    :return:
    """
    global _cached_once_state, _cached_current_state, _cached_released_state, PREVIOUS_INPUTS

    # 1. Get what is currently held down
    current_state = get_inputs()

    # 2. Get what was held last frame
    previous_inputs = PREVIOUS_INPUTS
    if previous_inputs is None:
        previous_inputs = {action: False for action in current_state}

    # 3. Calculate 'just pressed' (Once)
    _cached_once_state = {
        action: current_state[action] and not previous_inputs.get(action, False)
        for action in current_state
    }

    # 4. Calculate 'just released'
    _cached_released_state = {
        action: not current_state[action] and previous_inputs.get(action, False)
        for action in current_state
    }


    # 5. Save for the next frame

    _cached_current_state = current_state
    PREVIOUS_INPUTS = current_state




#%%#### Get the current input states (held, once, released & mouse/aim coordinates & controller inputs) #######
###############################################################################################################

def get_held_inputs():
    """
    Returns the mapping of actions that are CURRENTLY held down
    ==> Continously at each frame as long as the key/button is pressed

    ==> 'onkeypress', JavaScript

    :return: Mapping `{action: bool}` for currently held actions.
    """
    return _cached_current_state


def get_once_inputs():
    """
    Returns the mapping of actions that were pressed for the FIRST TIME in the current frame.
    ==> 'onKeyDown', JavaScript

    :return: Mapping `{action: bool}` for just-pressed actions.
    """
    return _cached_once_state

def get_released_inputs():
    """
    Returns the mapping of actions that were just RELEASED in the current frame.
    ==> 'onKeyUp', JavaScript

    :return: Mapping `{action: bool}` for just-released actions.
    """
    return _cached_released_state
    
def get_mouse_position(forced=False):
    """Return the current position of the mouse cursor.

    :return: Tuple (x, y) representing mouse coordinates.
    """
    if len(_controllers) == 0 or forced:
        return pg.mouse.get_pos()
    else:
        return None  #When controller
    
def get_player_aim_vector(forced=False):
    """Return a vector representing the player's aiming direction based on input.

    :return: Vector2 representing aim direction and intensity.
    """
    mouse_position = get_mouse_position(forced)
    if mouse_position is not None:
        return mouse_position
    else:
        axis_x = _controllers[0].get_axis(pg.CONTROLLER_AXIS_RIGHTX)
        axis_y = _controllers[0].get_axis(pg.CONTROLLER_AXIS_RIGHTY)
        deadzone = 0.2
        if abs(axis_x) < deadzone:
            axis_x = 0
        if abs(axis_y) < deadzone:
            axis_y = 0
        return pg.Vector2(axis_x, axis_y) * 1000  # Scale for
    

#%%#################### INPUT DISPLAY (ON SCREEN) ########################
##########################################################################

#Be sure that it's updated when controller is up
def get_str_input(selected_input: str) -> str:
    """
    Displays an adapted label according to the current input method (ex: "A" for Xbox, "X" for PS, "L-CLICK" for mouse, etc.)

    Returns a human-readable label for an action binding.

    :param selected_input: Action name.
    :return: Label adapted to controller/keyboard context.
    """
    if _controllers:
        joy = _controllers[0]
        brand = get_controller_brand(joy)
        mapping = BRAND_MAPS.get(brand, BRAND_MAPS["xbox"])

        if selected_input in CONTROLLER_INPUTS:
            input_data = CONTROLLER_INPUTS[selected_input][0]
            input_type, index = input_data[0], input_data[1]

            if input_type == "button":
                return mapping.get(index, f"Btn {index}")
            elif input_type == "axis":
                if index in [pg.CONTROLLER_AXIS_TRIGGERRIGHT, pg.CONTROLLER_AXIS_TRIGGERLEFT]:
                    return mapping.get(index, "Trigger")
                return "Stick"

        if selected_input in INPUTS:
            primary_key = INPUTS[selected_input][0]
            if primary_key == "MOUSE_LEFT":
                return "L-CLICK"
            if primary_key == "MOUSE_RIGHT":
                return "R-CLICK"
            return pg.key.name(primary_key).upper()

    # Fallback to Keyboard
    if selected_input in INPUTS:
        return pg.key.name(INPUTS[selected_input][0]).upper()

    return "None"

def get_hint_input(selected_input: str)->str:
    """
    Displays on screen an adapted hint label (ex: above an interactable object: [E] for PC, (A) for Xbox, etc.)

    Returns an on-screen hint wrapper for an action label, adapting to the current input method

    Uses `(X)` style on controller and `[X]` style on keyboard.

    :param selected_input: Action name.
    :return: Formatted hint string.
    """
    if len(_controllers) > 0:
        return "(" + get_str_input(selected_input) + ")"
    else:
        return "[" + get_str_input(selected_input) + "]"


def get_key_pressed(param):
    """Return the concrete key/button currently used for an action.

    :param param: Action name.
    :return: Key code or mouse token when pressed, else `None`.
    """
    if param in INPUTS:
        keys = INPUTS[param]
        for key in keys:
            if isinstance(key, int) and pg.key.get_pressed()[key]:
                return key
            elif key == "MOUSE_LEFT" and pg.mouse.get_pressed()[0]:
                return key
            elif key == "MOUSE_RIGHT" and pg.mouse.get_pressed()[2]:
                return key
    return None

def prevent_input(key):
    """
    Prevents the get_once_inputs ('onKeyDown') for the current frame

    Consume a just-pressed input for the current frame.

    :param key: Action key to clear from once-state.
    :return:
    """
    if _cached_once_state:
        _cached_once_state[key] = False

def prevent_once_key(param):
    """
    Prevents the get_once_inputs ('onKeyDown') WHILE the key is held down, not just for the current frame

    Clear the just-pressed state of an action to prevent it from triggering in the current frame.
    
    :param param:
    :return:
    """
    PREVENTED_INPUTS[param] = True

def is_mouse_clicked(number=0):
    """Return `True` while a mouse button is held down.

    :param number: Mouse button index.
    :return: Held click state.
    """
    mouse_pressed = pg.mouse.get_pressed()
    return number < len(mouse_pressed) and mouse_pressed[number]

def is_mouse_clicked_once(number=0):
    """Return `True` only on the frame where a mouse button starts pressing.

    :param number: Mouse button index.
    :return: Edge-triggered click state.
    """
    global MOUSE_CLICKED
    mouse_pressed = pg.mouse.get_pressed()
    if number < len(mouse_pressed) and mouse_pressed[number]:
        if number not in MOUSE_CLICKED:
            MOUSE_CLICKED.add(number)
            return True
    else:
        MOUSE_CLICKED.discard(number)
    return False
