import pygame as pg
from api.UI.GameUI import UIElement
from api.UI.Text import Text

from api.engine.Scene import Scene
from api.utils import Fonts


class ProgressBar(UIElement):
    """A polished, modern UI progress bar with smooth transitions."""

    def __init__(self, pos: tuple[int, int]|pg.Vector2, size: tuple[int, int]|pg.Vector2, color_bg: tuple[int, int, int], color_fg: tuple[int, int, int], progress_max: int=100, vertical: bool=False):
        super().__init__(pos, size)
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.vertical = vertical

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

    def set_position(self, pos: tuple[int, int] | tuple[float, float] | pg.Vector2):
        """Set the position of the progress bar."""
        super().set_position(pos)

    def set_size(self, size: tuple[int, int] | tuple[float, float] | pg.Vector2):
        """Set the size of the progress bar."""
        super().set_size(size)
        self.border_radius = size[1] // 2  # Update border radius for new height

    def set_color(self, color_fg: tuple[int, int, int] = None, color_bg: tuple[int, int, int] = None):
        """Update the colors of the progress bar."""
        if color_fg: self.color_fg = color_fg
        if color_bg: self.color_bg = color_bg

    def draw(self, surface: pg.Surface, scene: Scene = None):
        # 1. Update logic
        self.update()

        # 2. Draw Background
        bg_rect = pg.Rect(self.pos, self.size)
        pg.draw.rect(surface, self.color_bg, bg_rect, border_radius=self.border_radius)

        # 3. Calculate and Draw Foreground
        if self.visual_progress > 0:
            fill_ratio = self.visual_progress / self.progress_max

            if self.vertical:
                # Calcul pour la verticale (remplissage du bas vers le haut)
                fill_height = int(self.size[1] * fill_ratio)
                # On ajuste la position Y pour que ça monte
                fill_rect = pg.Rect(
                    self.pos[0],
                    self.pos[1] + (self.size[1] - fill_height),
                    self.size[0],
                    fill_height
                )
            else:
                # Calcul pour l'horizontale (gauche vers droite)
                fill_width = int(self.size[0] * fill_ratio)
                fill_rect = pg.Rect(self.pos, (fill_width, self.size[1]))

            # Dessin du remplissage
            if (self.vertical and fill_rect.height > 2) or (not self.vertical and fill_rect.width > 2):
                pg.draw.rect(surface, self.color_fg, fill_rect, border_radius=self.border_radius)

        # 4. Border
        pg.draw.rect(surface, (20, 20, 20), bg_rect, width=2, border_radius=self.border_radius)


class EntityProgressBar(ProgressBar):
    def __init__(self, color_bg: tuple[int, int, int], color_fg: tuple[int, int, int], name: str = "Boss", progress_max: int=100):
        super().__init__((0, 0), (0, 0), color_bg, color_fg, progress_max)
        self.name = name
        self.enemy_text = Text((0, 0), 24, self.name, font=Fonts.DEFAULT_FONT, color=(255, 255, 255))


    def update(self, scene = None):
        super().update(scene)
        if not scene:
            return
        self.set_position(((scene.size.x - self.size.x) // 2, 10))
        self.set_size(((scene.size.x - scene.size.x * 0.5), 10))
        self.border_radius = 20
        self.enemy_text.set_position(
            (scene.size.x // 2 - self.enemy_text.size.x // 2, 15 + self.size.y))

    def show(self, scene: Scene):
        self.update(scene)
        scene.UI.add(self.id, self)
        scene.UI.add(self.enemy_text.id, self.enemy_text)
        scene.UI.show(self.id)
        scene.UI.show(self.enemy_text.id)

    def hide(self, scene: Scene):
        scene.UI.hide(self.id)
        scene.UI.hide(self.enemy_text.id)