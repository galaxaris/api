"""
Default Event Collection dictionary associating event names with their corresponding callback functions.

PLEASE place the main associated event first, then the additional ones, for clarity.

==> Exemple: "player_jump": 1. Jump action, 2. SFX, Particles, etc.

Structure:

{
    "event_name": ([lambda event: event.Instances.some_instance.some_method(), ...], [condition1, condition2, ...]) (optional)
    ...
}
"""

"""
Default Event Collection dictionary...
"""

def get_default_events(manager):
    """
    Generates the default event collection for the EventManager.

    :param manager: The EventManager instance to which the events will be registered.

    :return: A dictionary containing the default events and their associated callback functions, with optional conditions.
    """
    return {
        #manager = the EventManager instance
        #e = the event (ex: mouse click) passed by triggerEvent
        "QUIT": ([lambda e=None: manager.Instances.game.stop()], None),
        "player_jump": ([lambda e=None: manager.Instances.player.do_jump()], [False]),
    }