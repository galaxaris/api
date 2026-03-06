"""Animation helpers for sprite sheets.

This module provides the `Animation` class used to split horizontal sprite
sheets into frames and retrieve time-based animation frames.
"""

import pygame as pg
from api.assets.Texture import Texture

class Animation:
    """Represents a frame-based animation extracted from a sprite sheet."""

    def __init__(self, texture: Texture, frame_count: int, delay: int = 100):
        """Initialize an animation from a texture.

        :param texture: Texture containing frames arranged horizontally.
        :param frame_count: Total number of frames in the sheet.
        :param delay: Delay in milliseconds between frame switches.
        """
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
        """Extract all animation frames from the sprite sheet.

        :param sheet: Source sheet to split.
        :return: Ordered list of extracted frame surfaces.
        """
        frames = []
        for i in range(self.frame_count):
            surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * self.width, 0, self.width, self.height)
            surface.blit(sheet, (0, 0), rect)
            frames.append(surface)
        return frames

    def reset(self):
        """Reset animation playback to the first frame.

        :return:
        """
        self.animation_count = 0
        self.last_update = pg.time.get_ticks()

    def get_frame(self, direction: str = "right") -> pg.Surface:
        """Return the current frame and advance when the delay elapsed.

        :param direction: Visual direction (`"right"` or `"left"`).
        :return: Current frame surface for the selected direction.
        """

        now = pg.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now # On reset le chrono
            self.animation_count += 1
            if self.animation_count == self.frame_count:
                self.animation_count = 0

        frames = self.frames_left if direction == "left" else self.frames_right
        return frames[self.animation_count]

    def calculate_frame_size(self, size: tuple[int, int] | pg.Vector2):
        """Resize already extracted frames to match a target render size.

        :param size: Target frame size `(width, height)`.
        :return:
        """
        self.width = size[0] // self.frame_count
        self.height = size[1]
        self.frames_right = [pg.transform.scale(frame_right, size) for frame_right in self.frames_right]
        self.frames_left = [pg.transform.scale(frame_left, size) for frame_left in self.frames_left]