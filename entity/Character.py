from api.entity.Entity import Entity
import pygame as pg

from api.items.Pistols import WaterPistol
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
        self.equipped_weapon = WaterPistol(Trajectory(free_fall, self.size // 2, DEFAULT_SHOT_SPEED, 0, DEFAULT_GRAVITY))
        # self.inventory = Inventory()

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

        self.equipped_weapon.update(scene)
        if self.equipped_weapon.is_aiming:
            self.set_direction(
                "left" if 3.14 >= self.equipped_weapon.trajectory.angle_radians >= 3.14 / 2 or -3.14 <= self.equipped_weapon.trajectory.angle_radians <= -3.14 / 2 else "right")
            if self.equipped_weapon.show_trajectory:
                surface_trajectory = pg.Surface((scene.get_width(), scene.get_height()), pg.SRCALPHA).convert_alpha()
                self.equipped_weapon.trajectory.draw(surface_trajectory, scene, self.pos)
                scene.add_surface(surface_trajectory, "_trajectory")

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1 * scene.Time.deltaTime

    def respawn(self):
        self.health = self.original_health
        super().respawn()

    def update_sprite(self):
        if self.hit_cooldown > 0:
            self.set_sprite("hit")
        else:
            super().update_sprite()