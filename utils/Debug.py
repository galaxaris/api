"""Debug flag management utilities."""

import os

debug_elements = {
    "colliders": False,
    "debug_info": False,
    "freecam": False
}

def set_active(enabled: bool):
    """Enable or disable global debug mode.

    :param enabled: Target debug state.
    :return:
    """
    os.environ["DEBUG"] = "1" if enabled else "0"

def toggle(element: str):
    """Toggle a named debug channel.

    :param element: Debug channel key.
    :return:
    """
    if element in debug_elements:
        debug_elements[element] = not debug_elements[element]

def is_enabled(element: str):
    """Return whether a debug channel is enabled.

    :param element: Debug channel key.
    :return: `True` when enabled.
    """
    return debug_elements.get(element, False)

