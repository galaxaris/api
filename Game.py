import pygame as pg

from api.engine import Scene

from typing import Callable, List, Dict

from api.engine.Scene import Scene
from pygame._sdl2.video import Window
from pygame._sdl2 import controller
from api.utils import Debug
from api.utils.DebugElement import DebugElement


class Game:
    window_width: int
    window_height: int
    width: int
    height: int
    name: str
    clock: pg.time.Clock
    screen: Scene
    running: bool
    icon: pg.Surface
    FPS: int
    flags: int
    window: Window
    bound_functions: Dict[int, List[Callable]]
    debug_list: List[tuple[str, str, int]]
    def __init__(self, size: tuple[int, int] | pg.Vector2, render_size: tuple[int, int] | pg.Vector2, name: str, flags: int, fps: int=60):
        pg.init()
        pg.mixer.init()
        pg.font.init()
        pg.joystick.init()
        controller.init()
        self.render = pg.display.set_mode(size, flags)
        self.screen = Scene(size if render_size is None else render_size)
        pg.display.set_caption(name)
        self.Window = Window.from_display_module()
        self.clock = pg.time.Clock()
        self.running = True
        self.FPS = fps
        self.flags = flags
        self.debug_list : list[tuple[str, str, int]] = []
        self.window = Window.from_display_module()
        self.bound_functions = {}

    def run(self, game):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        pg.display.toggle_fullscreen()
                        self.window = Window.from_display_module()

                    if event.key == pg.K_F12:
                        self.enable_debug()

                    if event.key == pg.K_F8:
                        if self.screen:
                            if self.screen.camera:
                                Debug.toggle("freecam")

                for func in self.bound_functions.get(event.type, []):
                    func(event)

            self.register_debug()

            game()

            self.screen.draw(self.render)

            self.render.fill((0, 0, 0))

            pg.transform.scale(self.screen, self.render.get_size(), self.render)

            self.launch_debug()

            pg.display.update()
            self.clock.tick(self.FPS)
        pg.quit()

    def get_current_monitor_size(self):
        index = self.window.display_index
        modes = pg.display.list_modes(display=index)
        return modes[0]

    def set_icon(self, path: str):
        if path.endswith(".png") or path.endswith(".jpg"):
            self.icon = pg.image.load(path)
            pg.display.set_icon(self.icon)

    def move_window(self, position: tuple[int,int] | pg.Vector2):
        self.window.position = position

    def resize_window(self, size: tuple[int, int] | pg.Vector2):
        self.render = pg.display.set_mode(size, self.flags)

    def bind(self, event_type: int, func: Callable[[pg.event.Event], None]):
        if event_type not in self.bound_functions:
            self.bound_functions[event_type] = []
        self.bound_functions[event_type].append(func)

    def debug(self, param, side: str = "left", size = 32):
        self.debug_list.append((str(param), side, size))

    def enable_debug(self):
        Debug.toggle("debug_info")
        Debug.toggle("colliders")
        self.debug_list = []

    def stop(self):
        self.running = False

    def launch_debug(self):

        if Debug.is_enabled("debug_info"):
            debug_y_left = 5
            debug_y_right = 5

            for debug_info in self.debug_list:
                debug_y = debug_y_left if debug_info[1] == "left" else debug_y_right

                debug_el = DebugElement((0, 0), debug_info[2], debug_info[0], "aptos")

                debug_x = 5 if debug_info[1] == "left" else self.render.get_width() - debug_el.size[0] - 5
                debug_el.set_position((debug_x, debug_y))
                debug_el.draw(self.render)

                if debug_info[1] == "left":
                    debug_y_left += debug_el.size[1] + 5
                else:
                    debug_y_right += debug_el.size[1] + 5
            self.debug_list.clear()

    def register_debug(self):
        self.debug("Omicronde API - Galaxaris", "left", 32)
        self.debug(f"FPS : {int(self.clock.get_fps())}", "left")

        if self.screen:
            screen = self.screen
            if screen.camera:
                self.debug(f"Camera : {int(screen.camera.position.x)} | {int(screen.camera.position.y)} - {screen.camera.camera_mode}", "left")
        
        keys_pressed = pg.key.get_pressed()
        active_keys = [pg.key.name(i) for i in range(len(keys_pressed)) if keys_pressed[i]]
        self.debug("Keys : " + ", ".join(active_keys), "left", 22)

        if self.screen:
            screen = self.screen
            self.debug(f"GameObjects : {int(len(screen.game_objects))}", "left", 22)

            if screen.layer_order:
                self.debug(f"Layers :", "left", 22)
                for i, layer in enumerate(screen.layer_order):
                    if "_" not in layer:
                        self.debug(f"{i} : {layer} - Object : {len(screen.layers[layer])}", "left", 22)
                    else:
                        self.debug(f"{i} : {layer}", "left", 22)

    def register_debug_entity(self, entity):
        self.debug(f"Entity : {entity.__class__.__name__}", "right")
        self.debug(f"Position : {int(entity.pos.x)} | {int(entity.pos.y)}", "right")

        if entity:
            self.debug("Jump : " + ("True" if entity.jump else "False"), "right")
            self.debug("Fall : " + ("True" if entity.fall else "False"), "right")
            self.debug("Boost : " + ("True" if entity.boost else "False"), "right")
            self.debug(f"Velocity : {entity.vel.x:.1f} | {entity.vel.y:.1f}", "right")

        if entity.collided_objs:
            self.debug("Collisions :", "right")
            for collision in entity.collided_objs:
                self.debug(f"{collision[0].__class__.__name__} | {collision[1]}", "right", 22)