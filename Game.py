import pygame as pg

from api.Scene import Scene
from pygame._sdl2.video import Window

class Game:
    width: int
    height: int
    name: str
    clock: pg.time.Clock
    screen: pg.Surface
    running: bool
    icon: pg.Surface
    FPS: int
    window: Window
    def __init__(self, width, height, name, fps=60):
        pg.init()
        pg.mixer.init()
        self.render = pg.display.set_mode((width, height), pg.SCALED | pg.RESIZABLE)
        self.screen = Scene(width, height)
        pg.display.set_caption(name)
        self.clock = pg.time.Clock()
        self.running = True
        self.width = width
        self.height = height
        self.FPS = fps
        self.window = Window.from_display_module()

    def run(self, game):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        pg.display.toggle_fullscreen()

            self.screen.fill((0, 0, 0))
            game()

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

    def stop(self):
        self.running = False