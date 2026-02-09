import pygame as pg
from typing import Callable, List, Dict, Any

from api.Scene import Scene
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
    def __init__(self, window_width, window_height, width, height, name, flags, fps=60):
        pg.init()
        pg.mixer.init()
        self.render = pg.display.set_mode((window_width, window_height), flags)
        self.screen = Scene(width, height)
        pg.display.set_caption(name)
        self.clock = pg.time.Clock()
        self.running = True
        self.width = width
        self.height = height
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

                for func in self.bound_functions.get(event.type, []):
                    func(event)



            #Double access to the same class !Not recommended
            game(self)

            self.screen.draw(self.render)
            pg.transform.scale(self.screen, self.render.get_size(), self.render)
            pg.display.update()
            self.clock.tick(self.FPS)
        pg.quit()

    def set_icon(self, path: str):
        if path.endswith(".png") or path.endswith(".jpg"):
            self.icon = pg.image.load(path)
            pg.display.set_icon(self.icon)

    def move_window(self, position: tuple[int,int]):
        self.window.position = position

    def resize_window(self, size: tuple[int, int]):
        self.render = pg.display.set_mode(size, self.flags)

    def bind(self, event_type: int, func: Callable[[pg.event.Event], None]):
        if event_type not in self.bound_functions:
            self.bound_functions[event_type] = []
        self.bound_functions[event_type].append(func)

    def stop(self):
        self.running = False