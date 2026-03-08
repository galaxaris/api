"""
Global variables for the game.

Useful for storing variables that need to be accessed across multiple modules, (camera position, scale ratio, game objects list, AudioManager...),
whithout having to pass them as parameters to every function that needs them.
"""


import pygame as pg

global_vars = {
    "cam_pos": pg.Vector2(0, 0),
    "scale_ratio": 1,
    "game_objects": [],
    "previous_inputs": None,
    "audio_manager": None,
    "default_font": "arial",
    "current_menu": None,
    "camera_limit_topleft": int,
    "camera_limit_bottomright": int,
    "offset": tuple[int],
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
    return global_vars[key]