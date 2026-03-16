from api.entity.Character import Character
from api.entity.Enemy import Enemy

import pygame as pg

from api.utils import Fonts
from api.UI.ProgressBar import EntityProgressBar

class Boss(Enemy):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] = (64, 64), health: int=500, name: str = "Boss"):
        super().__init__(pos, size, health)
        self.behavior: callable = None
        self.name = name
        self.enemy_progress_bar = EntityProgressBar((100, 100, 100), (255, 0, 0), progress_max=health, name=self.name)
        self.add_tag("boss")
        self.stages: dict[str, callable] = []
        self.stages_order: dict[str, int] = []

    def update(self, scene=None):
        Character.update(self, scene)


        self.stages_order = dict(sorted(self.stages_order.items(), key=lambda item: item[1], reverse=True))
        for stage_name, behavior in self.stages:
            if self.health <= self.stages_order[stage_name]:
                behavior(self, scene)
                break

        if self.enemy_progress_bar:
            if self.health > 0:
                self.enemy_progress_bar.show(scene)
            else:
                self.enemy_progress_bar.hide(scene)


            if self.health < self.original_health // 2:
                self.enemy_progress_bar.set_color((255, 255, 0))
            else:
                self.enemy_progress_bar.set_color((255, 0, 0))

            self.enemy_progress_bar.set_progress(self.health)

        if self.behavior:
            self.behavior(self, scene)



    def set_behavior(self, behavior: callable):
        self.behavior = behavior

    def add_stage(self, name: str, behavior: callable, life_threshold: int):
        self.stages.append((name, behavior))
        self.stages_order[name] = life_threshold
