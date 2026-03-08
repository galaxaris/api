"""
Global variables for the game.

Useful for storing variables that need to be accessed across multiple modules, (camera position, scale ratio, game objects list, AudioManager...),
whithout having to pass them as parameters to every function that needs them.
"""


import pygame as pg

from api.utils.Console import print_warning

global_vars = {
    "cam_pos": pg.Vector2(0, 0),
    "cam_limits": (pg.Vector2(0,0), pg.Vector2(0,0)),
    "cam_offset": pg.Vector2(0, 0),
    "scale_ratio": 1,
    "game_objects": [],
    "previous_inputs": None,
    "audio_manager": None,
    "default_font": "arial",
    "current_menu": None,
    "offset": tuple[int],
    "render_size": tuple[int, int],
    "default_surface": None,
}

def set_variable(key, value):
    """
    Sets a new global variable.
    """
    global_vars[key] = value

def get_variable(key):
    """
    Gets the value of a global variable.
    """
    if key not in global_vars:
        print_warning('Warning: trying to access a global variable that does not exist: ' + key)
        return None
    return global_vars[key]