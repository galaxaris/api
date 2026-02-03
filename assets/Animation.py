import pygame as pg

from api.assets.Texture import Texture

class Animation:
    def __init__(self, texture: Texture, frame_count: int):
        self.texture = texture
        self.frame_count = frame_count

        self.animation_count = 0

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

    def get_frame(self, direction: str = "right") -> pg.Surface:
        frames = self.frames_left if direction == "left" else self.frames_right

        # Calculate which frame to show
        current_sprite = frames[self.animation_count]

        # Update counter for next time
        self.animation_count += 1
        if self.animation_count == self.frame_count:
            self.animation_count = 0

        return current_sprite