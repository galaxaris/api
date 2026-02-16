import pygame as pg
from pygame.font import Font

font_generated : dict[tuple[str, int], Font] = {}

def get_font(name: str, size: int, custom: bool = False) -> Font:
    if (name, size) in font_generated:
        return font_generated[(name, size)]
    else:
        print("Add font", name, size)
        if custom:
            font_generated[(name, size)] = Font(name, size)
        else:
            font_generated[(name, size)] = pg.font.SysFont(name, size)
        return font_generated[(name, size)]
