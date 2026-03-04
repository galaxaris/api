state_elements = {
    "player_control": True,
    "override_player_control": False,
    "in_menu": False
}

def toggle(element: str, state = None):
    if element in state_elements:
        if state is not None:
            state_elements[element] = state
        else:
            state_elements[element] = not state_elements[element]

def is_enabled(element: str):
    return state_elements.get(element, False)

