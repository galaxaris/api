import pygame as pg

global_vars = {
    "cam_pos": pg.Vector2(0, 0),
    "scale_ratio": 1,
    "game_objects": [],
    "previous_inputs": None,
}

def set_variable(key, value):
    global_vars[key] = value

def get_variable(key):
    return global_vars[key]