from api.entity.Entity import Entity
import pygame as pg

from api.items.Catalog import Pistol
from api.items.Inventory import Inventory
from api.physics.Trajectory import Trajectory, free_fall
from api.utils.Constants import DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY


class Character(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] = (32, 32), health: int=100):
        super().__init__(pos, size)
        self.add_tag("character")
        self.original_health = health
        self.health = health
        self.invincible = False
        self.damage_force = 10
        self.damage_resistance = 0
        self.hit_cooldown = 0
        self.hit_cooldown_time = 20
        self.equipped_weapon = Pistol(Trajectory(free_fall, self.size // 2, DEFAULT_SHOT_SPEED, 0, DEFAULT_GRAVITY))
        self.inventory = Inventory()

    def take_damage(self, damage: int):
        if self.invincible or self.hit_cooldown > 0:
            return
        self.health -= (damage - self.damage_resistance)
        self.hit_cooldown = self.hit_cooldown_time
        if self.health <= 0:
            if "player" not in self.tags:
                self.kill()
            else:
                self.respawn()

    def update(self, scene=None):
        super().update(scene)
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1 * scene.Time.deltaTime

    def respawn(self):
        self.health = self.original_health
        super().respawn()