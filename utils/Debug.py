import os

debug_elements = {
    "colliders": False,
    "debug_info": False,
    "freecam": False
}

def set_active(enabled: bool):
    os.environ["DEBUG"] = "1" if enabled else "0"

def toggle(element: str):
    if element in debug_elements:
        debug_elements[element] = not debug_elements[element]

def is_element_enabled(element: str):
    return debug_elements.get(element, False)

