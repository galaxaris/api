import pygame as pg
from api.assets.Texture import Texture

class Animation:
    def __init__(self, texture: Texture, frame_count: int, delay: int = 100):
        self.texture = texture
        self.frame_count = frame_count
        self.delay = delay # On stocke le délai (ex: 100ms)

        self.animation_count = 0
        self.last_update = pg.time.get_ticks() # On lance le chrono ici

        self.width = texture.image.get_width() // frame_count
        self.height = texture.image.get_height()

        self.frames_right = self._extract_frames(texture.image)
        self.frames_left = [pg.transform.flip(f, True, False) for f in self.frames_right]

    def _extract_frames(self, sheet: pg.Surface):
        frames = []
        for i in range(self.frame_count):
            surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * self.width, 0, self.width, self.height)
            surface.blit(sheet, (0, 0), rect)
            frames.append(surface)
        return frames

    def reset(self):
        self.animation_count = 0
        self.last_update = pg.time.get_ticks()

    def get_frame(self, direction: str = "right") -> pg.Surface:

        now = pg.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now # On reset le chrono
            self.animation_count += 1
            if self.animation_count == self.frame_count:
                self.animation_count = 0

        frames = self.frames_left if direction == "left" else self.frames_right
        return frames[self.animation_count]