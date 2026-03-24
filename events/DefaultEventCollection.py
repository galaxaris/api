"""
Default Event Collection dictionary associating event names with their corresponding callback functions.

PLEASE place the main associated event first, then the additional ones, for clarity.

==> Exemple: "player_jump": 1. Jump action, 2. SFX, Particles, etc.

Structure:

{
    "event_name": [lambda event: event.Instances.some_instance.some_method(), ...],
    ...
}
"""

DefaultEventCollection = {
    "QUIT": [lambda event: event.Instances.game.stop()],
    "player_jump": [lambda event: event.Instances.player.do_jump()],
}