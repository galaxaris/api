import pygame as pg

from api.engine import Scene

from typing import Callable, List, Dict

from api.engine.Scene import Scene
from pygame._sdl2.video import Window

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
    def __init__(self, size: tuple[int, int] | pg.Vector2, render_size: tuple[int, int] | pg.Vector2, name: str, flags: int, fps: int=60):
        pg.init()
        pg.mixer.init()
        self.render = pg.display.set_mode(size, flags)
        self.screen = Scene(size if render_size is None else render_size)
        pg.display.set_caption(name)
        self.Window = Window.from_display_module()
        self.clock = pg.time.Clock()
        self.running = True
        self.FPS = fps
        self.flags = flags
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

                for func in self.bound_functions.get(event.type, []):
                    func(event)

            #Double access to the same class !Not recommended
            game()
            self.screen.draw(self.render)

            self.render.fill((0, 0, 0))
            pg.transform.scale(self.screen, self.render.get_size(), self.render)
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

    def stop(self):
        self.running = False