"""
=== OMICRONDE API - GALAXARIS ===

This module contains the main Game class of the Omicronde API.

Authors : Galaxaris & Associates

v.0.1 (in development) -
07/04/2026

Copyright (c) 2026 Galaxaris & Associates. All rights reserved.
"""

import pygame as pg

from api.assets.AudioManager import AudioManager
from api.engine import Scene

from typing import Callable, List, Dict

from api.engine.Scene import Scene
from pygame._sdl2.video import Window
from pygame._sdl2 import controller
from api.events.EventManager import EventManager
from api.utils import Debug, InputManager
from api.utils.DebugElement import DebugElement
from api.physics.Time import Time
from api.utils.Console import *
from api.assets.Texture import Texture

from api.utils.InputManager import get_inputs, onKeyDown, onKeyPress, onKeyUp


class Game:
    """
    Main class of the Omicronde API, responsible for managing the game loop, rendering, and window management.
    """
    window_width: int
    window_height: int
    width: int
    height: int
    name: str
    clock: pg.time.Clock #Time
    screen: Scene
    running: bool
    icon: pg.Surface
    fps: int #Time
    flags: int
    window: Window
    bound_functions: Dict[int, List[Callable]]

    def __init__(self, size: tuple[int, int] | pg.Vector2, render_size: tuple[int, int] | pg.Vector2, name: str, flags: int, fps: int=120, register_default_events: bool=True):
        """
        Initializes the game, creating the window and setting up the rendering surface and the scene

        :param size: Size of the window, in pixels (width, height)
        :param render_size: Size of the rendering surface, in pixels (render_width, render_height) -
        this allows to scale the game to a certain resolution (intended for pixel art)
        :param name: Name of the window
        :param flags: Flags for the window, such as fullscreen, resizable, etc.
        :param fps: Max Frame/sec rate (120fps is the default val)
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
        self.Time = Time(fps)
        self.running = True
        self.flags = flags
        self.window = Window.from_display_module()
        self.bound_functions = {}
        self.audio_manager = AudioManager()
        self.event_manager = EventManager()

        #WARNING NOTE: register_default_events should be set to True. Otherwise, the default events may not work properly, and then the player, scene, game, menu
        #May not work as expected (but remind there is always a 'hard coded' equivalent if not registered...)
        self.event_manager.registerDefaultEventCollection() if register_default_events else None

    def debug_keys(self):
        """
        Function to centralize the debug keys
         
        :return:
        """

        if onKeyDown(pg.K_F10):
            self.Time.lockedFPS = not self.Time.lockedFPS #Time
        if onKeyDown(pg.K_F11):
            self.toggle_fullscreen()
        if onKeyDown(pg.K_F12):
            self.enable_debug()
        if onKeyDown(pg.K_F8):
            if self.scene and self.scene.camera:
                Debug.toggle("freecam")
        if onKeyDown(pg.K_F9):
            if self.audio_manager:
                self.audio_manager.toggle_audio()
        


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

                if event.type == pg.MOUSEWHEEL:
                    InputManager.MOUSE_SCROLL += event.y

                for func in self.bound_functions.get(event.type, []):
                    func(event)

            Debug.register_debug(self)
            InputManager.update_input_state()

            #Debug keys, to be called after update_input_state
            #NOTE: to be removed in production
            self.debug_keys() 

            game()

            self.scene.assign_game_instances(self.Time, self.audio_manager)
            self.scene.draw(self.render)


            self.render.fill((0, 0, 0))

            pg.transform.scale(self.scene, self.render.get_size(), self.render)

            self.scene.scale_ratio = self.render.get_size()[0] / self.scene.get_size()[0]

            Debug.launch_debug(self)

            pg.display.update()

            InputManager.MOUSE_SCROLL = 0 #we need to reset mouse scroll at each frame
            Time.update(self.Time) #Time    


        print_success("Window closed successfully. Hoping see you soon for more adventures with the Omicronde API!")
        pg.quit()

    def get_current_monitor_size(self):
        """
        Returns the current monitor size

        :return: the current monitor size
        """
        index = self.window.display_index
        modes = pg.display.list_modes(display=index)
        return modes[0]

    def set_icon(self, icon: str | Texture | pg.Surface):
        """
        Defines an icon for the game window

        :param icon: Path to the icon file or a Texture or a pg.Surface to use as the icon
        :return:
        """

        if isinstance(icon, str):
            if icon.endswith(".png") or icon.endswith(".jpg"):
                try:
                    self.icon = pg.image.load(icon)
                    pg.display.set_icon(self.icon)
                except Exception as e:
                    print_error(f"Error loading game icon from {icon}: {e}")
        elif isinstance(icon, Texture):
            self.icon = icon.image
            pg.display.set_icon(self.icon) #Texture.image is a pg.Surface
        elif isinstance(icon, pg.Surface):
            self.icon = icon
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

    def enable_debug(self):
        """
        Enabling debug mode.

        :return:
        """
        Debug.debug_list = []
        Debug.toggle("debug_info")
        Debug.toggle("colliders")

    def stop(self):
        """
        Stops the game loop: the window then closes and the program finishes.

        :return:
        """
        self.running = False


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

