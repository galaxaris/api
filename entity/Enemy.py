from api.UI.ProgressBar import ProgressBar
from api.entity.Character import Character
import pygame as pg

from api.utils import Debug


class Enemy(Character):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], health: int = 100, speed: float = 2, mode: str = "patrol", range: int = 100):
        super().__init__(pos, size, health)
        self.speed = speed
        self.range = range
        self.mode = mode

        color_bar = (255, 0, 0) if self.health > self.original_health // 2 else (255, 255, 0)
        self.enemy_progress_bar = ProgressBar((self.pos.x, self.pos.y - 10), (self.size.x, 5), (100, 100, 100), color_bar, progress_max=100)
        self.add_tag("enemy")

    def update(self, scene=None):
        super().update(scene)
        layer = "#enemyHealthBar"
        if self.health < self.original_health:
            if self.health < self.original_health // 2:
                self.enemy_progress_bar.set_color((255, 255, 0))
            else:
                self.enemy_progress_bar.set_color((255, 0, 0))
            self.enemy_progress_bar.set_progress(self.health)
            self.enemy_progress_bar.set_position((self.pos.x, self.pos.y - 10) - scene.camera.position)
            scene.add(self.enemy_progress_bar, layer)
        else:
            scene.remove(self.enemy_progress_bar, layer)

        if self.mode == "patrol":
            self.do_patrol(scene)
        elif self.mode == "chase":
            self.do_chase(scene)

    def do_patrol(self, scene):
        if Debug.is_enabled("colliders"):
            red_line = pg.Surface((self.range, 1))
            red_line.fill((255, 0, 0))
            scene.blit(red_line, (self.start_pos.x - scene.camera.position.x + self.size.x//2, self.pos.y - scene.camera.position.y + self.size.y // 2))

        if not self.collided_objs:
            return
        self.vel.x = self.speed * scene.Time.deltaTime

        if self.pos.x > self.start_pos.x + self.range:
            self.speed = -abs(self.speed)
            self.set_direction("left")
        elif self.pos.x < self.start_pos.x:
            self.speed = abs(self.speed)
            self.set_direction("right")

    def do_chase(self, scene):
        pass
