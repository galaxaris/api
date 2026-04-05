"""Font loading helpers with in-memory caching."""

import pygame as pg
from pygame.font import Font
from api.utils.Console import print_warning

#Since loading fonts are costly, we cache them, avoiding loading same font again
font_generated : dict[tuple[str, int], Font] = {}

DEFAULT_FONT = "arial"

def get_font(name: str, size: int, custom: bool = False) -> Font:
    """Return a cached font instance for the requested name and size.

    Names containing `"**/"` are resolved as explicit file paths after the
    marker. Other names are resolved through `pygame.font.SysFont`.

    :param name: Font family name or marked file path.
    :param size: Font size in pixels.
    :param custom: Reserved compatibility parameter.
    :return: Loaded font instance.
    """

    if (name, size) in font_generated:
        return font_generated[(name, size)]
    else:
        if "**/" in name:
            path = name.split("**/")[1]
            try:
                font_generated[(name, size)] = pg.font.Font(path, size)
            except Exception as e:
                print_warning(f"Error loading font from path '{path}': {e}. Falling back to default font.")
                font_generated[(name, size)] = pg.font.SysFont(DEFAULT_FONT, size)
        else:
            try:
                font_generated[(name, size)] = pg.font.SysFont(name, size)
            except Exception as e:
                print_warning(f"Error loading font from system: {e}. Falling back to default font.")
                font_generated[(name, size)] = pg.font.SysFont(DEFAULT_FONT, size)
                
        return font_generated[(name, size)]
