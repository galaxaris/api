"""
=== OMICRONDE API - GALAXARIS ===

This module contains the main Game class of the Omicronde API.

Authors : Galaxaris & Associates

v. Beta (in development) -
03/03/2026

Copyright (c) 2026 Galaxaris & Associates. All rights reserved.
"""

### TODO: should we pass all the API instances to the Game class? (Could make it easier to access everything from one class)

import pygame as pg

from api.assets.AudioManager import AudioManager
from api.engine import Scene

from typing import Callable, List, Dict

from api.engine.Scene import Scene
from pygame._sdl2.video import Window
from pygame._sdl2 import controller
from api.utils import Debug, GlobalVariables, Inputs
from api.utils.DebugElement import DebugElement



class Game:
    """
    Main class of the Omicronde API, responsible for managing the game loop, rendering, and window management.
    """
    window_width: int
    window_height: int
    width: int
    height: int
    name: str
    clock: pg.time.Clock
    screen: Scene
    running: bool
    icon: pg.Surface
    fps: int
    flags: int
    window: Window
    bound_functions: Dict[int, List[Callable]]
    debug_list: List[tuple[str, str, int]]
    debug_font: str

    def __init__(self, size: tuple[int, int] | pg.Vector2, render_size: tuple[int, int] | pg.Vector2, name: str, flags: int, fps: int=60, debug_font: str="**/assets/Fonts/m6x11.ttf"):
        """
        Initializes the game, creating the window and setting up the rendering surface and the scene

        :param size: Size of the window, in pixels (width, height)
        :param render_size: Size of the rendering surface, in pixels (render_width, render_height) -
        this allows to scale the game to a certain resolution (intended for pixel art)
        :param name: Name of the window
        :param flags: Flags for the window, such as fullscreen, resizable, etc.
        :param fps: Max Frame/sec rate (60fps is the default val)
        """
        pg.init()
        pg.mixer.init()
        pg.font.init()
        pg.joystick.init()
        controller.init()
        self.render = pg.display.set_mode(size, flags)
        self.scene = Scene(size if render_size is None else render_size)
        pg.display.set_caption(name)
        self.Window = Window.from_display_module()
        self.clock = pg.time.Clock()
        self.running = True
        self.locked_fps = True
        self.fps = fps
        self.flags = flags
        self.debug_list : list[tuple[str, str, str, int]] = []
        self.window = Window.from_display_module()
        self.bound_functions = {}
        self.audio_manager = AudioManager()
        GlobalVariables.set_variable("audio_manager", self.audio_manager)
        self.debug_font = debug_font

    def run(self, game):
        """
        Runs the game loop, handling events, updating the scene, and rendering the game.

        :param game: pg function to be called at each frame ==> should update the game state
        :return:
        """
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F10:
                        self.locked_fps = not self.locked_fps

                    if event.key == pg.K_F11:
                        self.toggle_fullscreen()

                    if event.key == pg.K_F12:
                        self.enable_debug()

                    if event.key == pg.K_F8:
                        if self.scene:
                            if self.scene.camera:
                                Debug.toggle("freecam")

                if event.type == pg.MOUSEWHEEL:
                    Inputs.MOUSE_SCROLL += event.y

                for func in self.bound_functions.get(event.type, []):
                    func(event)

            self.register_debug()
            Inputs.update_input_state()
            game()

            self.scene.draw(self.render)

            self.render.fill((0, 0, 0))

            pg.transform.scale(self.scene, self.render.get_size(), self.render)

            GlobalVariables.set_variable("scale_ratio", self.render.get_size()[0] / self.scene.get_size()[0])

            self.launch_debug()

            pg.display.update()
            if self.locked_fps:
                self.clock.tick(self.fps)
            else:
                self.clock.tick()
        pg.quit()

    def get_current_monitor_size(self):
        """
        Returns the current monitor size

        :return: the current monitor size
        """
        index = self.window.display_index
        modes = pg.display.list_modes(display=index)
        return modes[0]

    def set_icon(self, path: str):
        """
        Defines an icon for the game window

        :param path: Path to the icon file
        :return:
        """
        if path.endswith(".png") or path.endswith(".jpg"):
            self.icon = pg.image.load(path)
            pg.display.set_icon(self.icon)

    def move_window(self, position: tuple[int,int] | pg.Vector2):
        """
        Moves the game window to a new position on the device screen

        :param position: New position of the window (x, y)
        :return:
        """
        self.window.position = position

    def resize_window(self, size: tuple[int, int] | pg.Vector2):
        """
        Changes the size of the game window

        :param size: New size of the window (width, height)
        :return:
        """
        self.render = pg.display.set_mode(size, self.flags)

    def bind(self, event_type: int, func: Callable[[pg.event.Event], None]):
        """
        Binds a function to an event type. Very useful for handling events in the game loop.

        :param event_type: Event type to bind the function to.
        :param func: Function to be called when the event is triggered.
        :return:
        """
        if event_type not in self.bound_functions:
            self.bound_functions[event_type] = []
        self.bound_functions[event_type].append(func)

    def debug(self, param, side: str = "left", font = "arial", size = 32):
        """
        Adds a debug information to be displayed on the screen.

        :param param: The parameter to be displayed.
        :param side: The screen side where it's displayed: "left" or "right".
        :param font: The font to be used
        :param size: Font size
        :return:
        """
        self.debug_list.append((str(param), side, font, size))

    def enable_debug(self):
        """
        Enabling debug mode.

        :return:
        """
        Debug.toggle("debug_info")
        Debug.toggle("colliders")
        self.debug_list = []

    def stop(self):
        """
        Stops the game loop: the window then closes and the program finishes.

        :return:
        """
        self.running = False

    def launch_debug(self):
        """
        Launches the debug mode

        :return:
        """

        if Debug.is_enabled("debug_info"):
            debug_y_left = 5
            debug_y_right = 5

            for debug_info in self.debug_list:
                debug_y = debug_y_left if debug_info[1] == "left" else debug_y_right

                debug_el = DebugElement((0, 0), debug_info[3], debug_info[0], debug_info[2])

                debug_x = 5 if debug_info[1] == "left" else self.render.get_width() - debug_el.size[0] - 5
                debug_el.set_position((debug_x, debug_y))
                debug_el.draw(self.render)

                if debug_info[1] == "left":
                    debug_y_left += debug_el.size[1] + 5
                else:
                    debug_y_right += debug_el.size[1] + 5
            self.debug_list.clear()

    def toggle_fullscreen(self, mode: bool=None):
        """
        Toggles fullscreen mode on or off

        :param mode: True for on, False or None for off
        :return:
        """
        if mode is None: #we just want to switch the screen mode
            pg.display.toggle_fullscreen()
            self.window = Window.from_display_module()

        elif pg.display.is_fullscreen() != mode: #we want to switch it only if it is not in the same state as the one we want
            pg.display.toggle_fullscreen()
            self.window = Window.from_display_module()

    def register_debug(self):
        """
        Registers debug information, and updates the debug information

        :return:
        """

        self.debug("Omicronde API - Galaxaris", "left", self.debug_font, 36)
        self.debug(f"FPS : {int(self.clock.get_fps())} | Render t : {self.clock.get_rawtime()} ms", "left", self.debug_font, 32)

        if self.scene:
            screen = self.scene
            if screen.camera:
                self.debug(f"Camera : {int(screen.camera.position.x)} | {int(screen.camera.position.y)} - {screen.camera.camera_mode}", "left", self.debug_font, 32)
        
        keys_pressed = pg.key.get_pressed()
        active_keys = [pg.key.name(i) for i in range(len(keys_pressed)) if keys_pressed[i]]
        self.debug("Keys : " + ", ".join(active_keys), "left", self.debug_font, 32)

        if self.scene:
            screen = self.scene
            self.debug(f"GameObjects : {int(len(screen.game_objects))}", "left", self.debug_font, 32)

            if screen.layer_order:
                self.debug(f"Layers :", "left", self.debug_font, 32)
                for i, layer in enumerate(screen.layer_order):
                    if "_" not in layer:
                        self.debug(f"{i} : {layer} - Object : {len(screen.layers[layer])}", "left", self.debug_font, 16)
                    else:
                        self.debug(f"{i} : {layer}", "left", self.debug_font, 16)

    def register_debug_entity(self, entity):
        """
        Registers debug information for an entity
        
        :param entity: the target entity
        :return:
        """
        self.debug(f"Entity : {entity.__class__.__name__}", "right", self.debug_font, 32)
        self.debug(f"Position : {int(entity.pos.x)} | {int(entity.pos.y)}", "right", self.debug_font, 32)

        if entity:
            self.debug("Jump : " + ("True" if entity.jump else "False"), "right", self.debug_font, 32)
            self.debug("Fall : " + ("True" if entity.fall else "False"), "right", self.debug_font, 32)
            self.debug("Boost : " + ("True" if entity.boost else "False"), "right", self.debug_font, 32)
            self.debug(f"Velocity : {entity.vel.x:.1f} | {entity.vel.y:.1f}", "right", self.debug_font, 32)

            if hasattr(entity, "active_trajectory") and entity.active_trajectory:
                self.debug(f"Trajectory : Angle {round(entity.active_trajectory.angle_radians, 2)} rad | Speed {entity.active_trajectory.shot_speed}", "right", self.debug_font, 32)

        if entity.collided_objs:
            self.debug("Collisions :", "right", self.debug_font, 32)
            for collision in entity.collided_objs:
                self.debug(f"{collision[0].__class__.__name__} | {collision[1]}", "right", self.debug_font, 16)