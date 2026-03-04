import os

import pygame as pg
from pygame._sdl2 import controller

from api.utils import GlobalVariables

MOUSE_SCROLL = 0

INPUTS = {
    "right": [pg.K_RIGHT, pg.K_d],
    "left": [pg.K_LEFT, pg.K_q],
    "jump": [pg.K_SPACE],
    "boost": [pg.K_LSHIFT, pg.K_RCTRL],
    "up": [pg.K_UP, pg.K_z],
    "down": [pg.K_DOWN, pg.K_s],
    "aim": ["MOUSE_RIGHT"],
    "shoot": ["MOUSE_LEFT"],
    "interact": [pg.K_e],
    "pause": [pg.K_ESCAPE],
    "menu_up": [],
    "menu_down": [],
    "menu_left": [],
    "menu_right": [],
    "menu_select": [pg.K_RETURN]
}

CONTROLLER_INPUTS = {
    "right": [("axis", pg.CONTROLLER_AXIS_LEFTX, 16000)],
    "left": [("axis", pg.CONTROLLER_AXIS_LEFTX, -16000)],
    "up": [("axis", pg.CONTROLLER_AXIS_LEFTY, -16000)],
    "down": [("axis", pg.CONTROLLER_AXIS_LEFTY, 16000)],
    "jump": [("button", pg.CONTROLLER_BUTTON_A)],
    "boost": [("axis", pg.CONTROLLER_AXIS_TRIGGERRIGHT, 10000)],
    "interact": [("button", pg.CONTROLLER_BUTTON_B)],
    "aim": [("axis", pg.CONTROLLER_AXIS_TRIGGERLEFT, 10000)],
    "shoot": [("button", pg.CONTROLLER_BUTTON_RIGHTSHOULDER)],
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
        pg.CONTROLLER_BUTTON_A: "Cross", pg.CONTROLLER_BUTTON_B: "Circle",
        pg.CONTROLLER_BUTTON_X: "Square", pg.CONTROLLER_BUTTON_Y: "Triangle",
        pg.CONTROLLER_AXIS_TRIGGERRIGHT: "R2", pg.CONTROLLER_AXIS_TRIGGERLEFT: "L2",
        pg.CONTROLLER_BUTTON_RIGHTSHOULDER: "R1", pg.CONTROLLER_BUTTON_LEFTSHOULDER: "L1"
    }
}

def editor_edit_key(key,value):
    EDITOR_KEYS[key] = value

def editor_release_key():
    global EDITOR_KEYS
    EDITOR_KEYS = {}

def get_controller_brand(joy):
    name = joy.name.lower()
    if any(x in name for x in ["playstation", "dualshock", "dualsense", "ps4", "ps5"]):
        return "ps"
    return "xbox"


def get_inputs():
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
    return current_state


_cached_once_state = {}
_cached_current_state = {}


def update_input_state():
    """
    Call this ONCE at the beginning of your game loop.
    It calculates the state for the entire frame.
    """
    global _cached_once_state, _cached_current_state

    # 1. Get what is currently held down
    current_state = get_inputs()

    # 2. Get what was held last frame
    previous_inputs = GlobalVariables.get_variable("previous_inputs")
    if previous_inputs is None:
        previous_inputs = {action: False for action in current_state}

    # 3. Calculate 'just pressed' (Once)
    _cached_once_state = {
        action: current_state[action] and not previous_inputs.get(action, False)
        for action in current_state
    }

    # 4. Save for the next frame
    _cached_current_state = current_state
    GlobalVariables.set_variable("previous_inputs", current_state)


def get_once_inputs():
    """Returns the cached 'just pressed' states for this frame."""
    return _cached_once_state


def get_held_inputs():
    """Returns the cached 'currently held' states for this frame."""
    return _cached_current_state

def get_str_input(selected_input: str) -> str:
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
   if len(_controllers) > 0:
        return "(" + get_str_input(selected_input) + ")"
   else:
        return "[" + get_str_input(selected_input) + "]"


def get_mouse(forced=False):
    if len(_controllers) == 0 or forced:
        return pg.mouse.get_pos()
    else:
        axis_x = _controllers[0].get_axis(pg.CONTROLLER_AXIS_RIGHTX)
        axis_y = _controllers[0].get_axis(pg.CONTROLLER_AXIS_RIGHTY)
        deadzone = 0.2
        if abs(axis_x) < deadzone:
            axis_x = 0
        if abs(axis_y) < deadzone:
            axis_y = 0
        return pg.Vector2(axis_x, axis_y) * 1000  # Scale for


def get_key_pressed(param):
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


def is_controller_connected():
    return len(_controllers) > 0

def prevent_input(key):
    if _cached_once_state:
        _cached_once_state[key] = False