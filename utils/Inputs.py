import os

import pygame as pg
from pygame._sdl2 import controller

MOUSE_SCROLL = 0

INPUTS = {
    "right": [pg.K_RIGHT, pg.K_d],
    "left": [pg.K_LEFT, pg.K_q],
    "jump": [pg.K_SPACE],
    "boost": [pg.K_LSHIFT, pg.K_RCTRL],
    "up": [pg.K_UP, pg.K_z],
    "down": [pg.K_DOWN, pg.K_s],
    "shoot": [pg.K_f],
    "interact": [pg.K_e]
}

CONTROLLER_INPUTS = {
    "right": [("axis", pg.CONTROLLER_AXIS_LEFTX, 16000)],
    "left": [("axis", pg.CONTROLLER_AXIS_LEFTX, -16000)],
    "up": [("axis", pg.CONTROLLER_AXIS_LEFTY, -16000)],
    "down": [("axis", pg.CONTROLLER_AXIS_LEFTY, 16000)],
    "jump": [("button", pg.CONTROLLER_BUTTON_A)],
    "boost": [("axis", pg.CONTROLLER_AXIS_TRIGGERRIGHT, 10000)],
    "interact": [("button", pg.CONTROLLER_BUTTON_B)],
    "shoot": [("button", pg.CONTROLLER_BUTTON_RIGHTSHOULDER, 10000)]
}

_EDITOR_KEYS = {}
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
    _EDITOR_KEYS[key] = value

def editor_release_key():
    _EDITOR_KEYS = {}

def get_controller_brand(joy):
    name = joy.name.lower()
    if any(x in name for x in ["playstation", "dualshock", "dualsense", "ps4", "ps5"]):
        return "ps"
    return "xbox"


def get_inputs():
    current_state = {}
    pg_keys = {}
    if os.environ.get("EDITOR") == "1":
        pg_keys = _EDITOR_KEYS
        current_state = {action: any(pg_keys.get(key, False) for key in keys) for action, keys in INPUTS.items()}
    else:
        pg_keys = pg.key.get_pressed()
        current_state = {action: any(pg_keys[key] for key in keys) for action, keys in INPUTS.items()}


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

def get_once_inputs():
    current_state = get_inputs()
    if not hasattr(get_once_inputs, "previous_state"):
        get_once_inputs.previous_state = {action: False for action in current_state}

    once_state = {action: current_state[action] and not get_once_inputs.previous_state[action] for action in current_state}
    get_once_inputs.previous_state = current_state
    return once_state

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

    # Fallback to Keyboard
    if selected_input in INPUTS:
        return pg.key.name(INPUTS[selected_input][0]).upper()

    return "None"

def get_hint_input(selected_input: str)->str:
   if len(_controllers) > 0:
        return "(" + get_str_input(selected_input) + ")"
   else:
        return "[" + get_str_input(selected_input) + "]"
