import pygame as pg
from api.UI.GameUI import UIElement

from api.engine.Scene import Scene


class ProgressBar(UIElement):
    """A polished, modern UI progress bar with smooth transitions."""

    def __init__(self, pos, size, color_bg, color_fg, progress_max=100):
        super().__init__(pos, size)
        self.color_bg = color_bg
        self.color_fg = color_fg

        self.progress_max = progress_max
        self.current_value = 0.0  # The actual value (e.g., 50/100)
        self.visual_progress = 0.0  # The interpolated value for smooth animation

        # Style settings
        self.border_radius = size[1] // 2  # Fully rounded caps
        self.lerp_speed = 0.1  # How fast the bar "catches up" (0.0 to 1.0)

    def set_progress(self, value: float):
        """Update the target progress value."""
        self.current_value = max(0.0, min(self.progress_max, value))

    def update(self, scene: Scene = None):
        """Smoothly interpolate visual progress."""
        # This makes the bar slide smoothly rather than snapping
        diff = self.current_value - self.visual_progress
        self.visual_progress += diff * self.lerp_speed

    def set_color(self, color_fg: tuple[int, int, int] = None, color_bg: tuple[int, int, int] = None):
        """Update the colors of the progress bar."""
        if color_fg: self.color_fg = color_fg
        if color_bg: self.color_bg = color_bg

    def draw(self, surface: pg.Surface, scene: Scene = None):
        # 1. Update the interpolation logic
        self.update()

        # 2. Draw the Shadow/Background
        # Slightly offset to give depth
        bg_rect = pg.Rect(self.pos, self.size)
        pg.draw.rect(surface, self.color_bg, bg_rect, border_radius=self.border_radius)

        # 3. Calculate and Draw Foreground (The Fill)
        if self.visual_progress > 0:
            fill_ratio = self.visual_progress / self.progress_max
            fill_width = int(self.size[0] * fill_ratio)

            # Ensure the fill width doesn't look weird at very low values
            if fill_width > 0:
                fill_rect = pg.Rect(self.pos, (fill_width, self.size[1]))
                pg.draw.rect(surface, self.color_fg, fill_rect, border_radius=self.border_radius)

        # 5. Optional: Thin Border for definition
        pg.draw.rect(surface, (20, 20, 20), bg_rect, width=2, border_radius=self.border_radius)