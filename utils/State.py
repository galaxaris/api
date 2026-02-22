import os

state_elements = {
    "player_control": True,
}

def toggle(element: str):
    if element in state_elements:
        state_elements[element] = not state_elements[element]

def is_enabled(element: str):
    return state_elements.get(element, False)

