import pygame as pg
from pygame._sdl2 import controller

# Standard mapping for keys
INPUTS = {
    "right": [pg.K_RIGHT, pg.K_d],
    "left": [pg.K_LEFT, pg.K_q],
    "jump": [pg.K_SPACE],
    "boost": [pg.K_LSHIFT, pg.K_RCTRL],
    "up": [pg.K_UP, pg.K_z],
    "down": [pg.K_DOWN, pg.K_s]
}

_controllers = {}

def get_inputs():
    pg_keys = pg.key.get_pressed()
    current_state = {action: any(pg_keys[key] for key in keys) for action, keys in INPUTS.items()}

    for i in range(controller.get_count()):
        if i not in _controllers:
            con = controller.Controller(i)
            _controllers[i] = con

    if _controllers:
        joy = _controllers[0]
        if joy.get_axis(0) > 16000: current_state["right"] = True
        elif joy.get_axis(0) < -16000: current_state["left"] = True

        if joy.get_axis(1) < -16000: current_state["up"] = True
        elif joy.get_axis(1) > 16000: current_state["down"] = True

        if joy.get_button(0): current_state["jump"] = True
        if joy.get_axis(5) > 10000: current_state["boost"] = True

    return current_state