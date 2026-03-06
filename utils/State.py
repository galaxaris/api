"""Global gameplay state toggles."""

state_elements = {
    "player_control": True,
    "override_player_control": False,
    "in_menu": False
}

def toggle(element: str, state = None):
    """Toggle or set a named state flag.

    :param element: State key.
    :param state: Explicit value to set. When `None`, value is toggled.
    :return:
    """
    if element in state_elements:
        if state is not None:
            state_elements[element] = state
        else:
            state_elements[element] = not state_elements[element]

def is_enabled(element: str):
    """Return whether a named state flag is enabled.

    :param element: State key.
    :return: `True` when enabled.
    """
    return state_elements.get(element, False)

