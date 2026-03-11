from api.UI.ProgressBar import ProgressBar
from api.entity.Character import Character
import pygame as pg

class Enemy(Character):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], health: int = 100, speed: float = 0.2):
        super().__init__(pos, size, health)
        self.speed = speed
        self.add_tag("enemy")

    def update(self, scene=None):
        super().update(scene)
        layer = "_#enemy_health_bar"
        if self.health < self.original_health:
            color_bar = (255, 0, 0) if self.health > self.original_health//2 else (255, 255, 0)
            enemy_progress_bar = ProgressBar((self.pos.x, self.pos.y - 10) - scene.camera.position, (self.size.x, 5), (100, 100, 100), color_bar, progress_max=100)
            enemy_progress_bar.current_value = self.health*10
            enemy_progress_bar.draw(scene.default_surface, scene)
