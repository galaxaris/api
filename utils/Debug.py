"""Debug flag management utilities."""

import os

from api.utils import Fonts
from api.utils.DebugElement import DebugElement
import pygame as pg

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

debug_list : list[tuple[str, str, str, int]]  = []
debug_font = Fonts.DEFAULT_FONT

def debug(text: str, side: str = "left", font: str = debug_font, size: int = 32):
    global debug_list
    """Add a debug text element to the render queue.

    :param text: Text content.
    :param side: Render side, either `"left"` or `"right"`.
    :param font: Font name or path marker.
    :param size: Font size in pixels.
    :return:
    """
    debug_list.append((text, side, font, size))


def register_debug(self):
    """
    Registers debug information, and updates the debug information

    :return:
    """

    debug("Omicronde API - Galaxaris", "left", debug_font, 36)
    debug(f"FPS : {int(self.Time.clock.get_fps())} | Render t : {self.Time.clock.get_rawtime()} ms", "left",
               debug_font, 32)

    if self.scene:
        screen = self.scene
        if screen.camera:
            debug(
                f"Camera : {int(screen.camera.position.x)} | {int(screen.camera.position.y)} - {screen.camera.camera_mode}",
                "left", debug_font, 32)

    keys_pressed = pg.key.get_pressed()
    active_keys = [pg.key.name(i) for i in range(len(keys_pressed)) if keys_pressed[i]]

    if self.scene:
        screen = self.scene
        debug(f"GameObjects : {int(len(screen.game_objects))}", "left", debug_font, 32)

        if screen.layer_order:
            debug(f"Layers :", "left", debug_font, 32)
            for i, layer in enumerate(screen.layer_order):
                if "_" not in layer:
                    debug(f"{i} : {layer} - Object : {len(screen.layers[layer])}", "left", debug_font, 16)
                else:
                    debug(f"{i} : {layer}", "left", debug_font, 16)

    # SFX part

    if len(active_keys) > 0:
        debug("Keys : " + ", ".join(active_keys), "left", debug_font, 20)

    if self.audio_manager:
        audio_manager = self.audio_manager
        if audio_manager.current_music():
            debug(f"Music :", "left", debug_font, 32)
            debug(
                f"{audio_manager.current_music()} - {'Playing' if audio_manager.is_music_playing() else 'Paused'}",
                "left", debug_font, 16)

        if audio_manager.current_sfx():
            debug(f"SFX :", "left", debug_font, 32)

            sfx_debug_str = ""
            for sfx in audio_manager.current_sfx():
                sfx_debug_str += f"{sfx} - {'Playing' if audio_manager.is_sfx_playing(sfx) else 'Paused'} | "
            debug(sfx_debug_str[:-3], "left", debug_font, 16)  # -3 allows to remove the last " | "

def register_debug_entity(self, entity):
    """
    Registers debug information for an entity

    :param entity: the target entity
    :return:
    """
    debug(f"Entity : {entity.__class__.__name__}", "right", debug_font, 32)

    if entity:
        debug(f"Position : {int(entity.pos.x)} | {int(entity.pos.y)}", "right", debug_font, 32)
        debug(f"Velocity : {entity.vel.x:.1f} | {entity.vel.y:.1f}", "right", debug_font, 32)
        debug("Jump : " + ("True" if entity.jump else "False"), "right", debug_font, 16)
        debug("Fall : " + ("True" if entity.fall else "False"), "right", debug_font, 16)
        debug("Boost : " + ("True" if entity.boost else "False"), "right", debug_font, 16)
        debug(f"Gravity : {entity.gravity:.2f}", "right", debug_font, 16)

        if hasattr(entity,
                   "equipped_weapon") and entity.equipped_weapon.trajectory and entity.equipped_weapon.is_aiming:
            angle = entity.equipped_weapon.trajectory.angle_radians if entity.equipped_weapon.trajectory.angle_radians else 0
            ini_speed = entity.equipped_weapon.trajectory.ini_speed if entity.equipped_weapon.trajectory.ini_speed else 0
            debug(f"Trajectory : Angle {round(angle, 2)} rad | Speed {ini_speed}", "right", debug_font,
                       32)

        if hasattr(entity, "health"):
            debug(f"Health : {entity.health}", "right", debug_font, 32)

        if entity.collided_objs:
            debug("Collisions :", "right", debug_font, 32)
            for collision in entity.collided_objs:
                debug(f"{collision[0].__class__.__name__} | {collision[1]}", "right", debug_font, 16)

def launch_debug(self):
    global debug_list
    """
    Launches the debug mode

    :return:
    """

    if is_enabled("debug_info"):

        debug_y_left = 5
        debug_y_right = 5

        for debug_info in debug_list:
            debug_y = debug_y_left if debug_info[1] == "left" else debug_y_right

            debug_el = DebugElement((0, 0), debug_info[3], debug_info[0], debug_info[2])

            debug_x = 5 if debug_info[1] == "left" else self.render.get_width() - debug_el.size[0] - 5
            debug_el.set_position((debug_x, debug_y))
            debug_el.draw(self.render)

            if debug_info[1] == "left":
                debug_y_left += debug_el.size[1] + 5
            else:
                debug_y_right += debug_el.size[1] + 5
        debug_list.clear()