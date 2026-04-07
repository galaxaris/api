from api.entity.Entity import Entity
import pygame as pg

from api.items.Pistols import WaterPistol, EarthPistol, GrapplingPistol
from api.items.Inventory import Inventory
from api.physics.Trajectory import Trajectory, free_fall
from api.utils.Constants import DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY, DEFAULT_GRAPPLING_SPEED
from api.utils.Console import print_warning


class Character(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] = (32, 32),
                  health: int=100, damage_resistance: int=0, damage_force: int=10, max_velocity: float|int = 2, 
                  acceleration: float|int = 0.5, resistance:float|int = 0.2, force:float|int = 20):
        
        super().__init__(pos, size, max_velocity=max_velocity, acceleration=acceleration, resistance=resistance, force=force)
        self.add_tag("character")
        self.original_health = health
        self.health = health
        self.invincible = False
        self.damage_force = damage_force
        self.damage_resistance = damage_resistance
        self.hit_cooldown = 0
        self.hit_cooldown_time = 20
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
    
    def equip_weapon(self, name: str, cooldown: int = None, damage: int = None):
        if name == "WaterPistol":
            if cooldown is None: cooldown = 200
            if damage is None: damage = 15
            self.inventory.weapons.append(WaterPistol(Trajectory(free_fall, self.size // 2, DEFAULT_SHOT_SPEED, 0, 
                DEFAULT_GRAVITY), cooldown=cooldown, projectile_damage=damage))
            
        elif name == "EarthPistol":
            if cooldown is None: cooldown = 200
            if damage is None: damage = 15
            self.inventory.weapons.append(EarthPistol(Trajectory(free_fall, self.size // 2, DEFAULT_SHOT_SPEED, 0, DEFAULT_GRAVITY), 
                cooldown=cooldown, projectile_damage=damage))
            
        elif name=="GrapplingPistol":
            if cooldown is None: cooldown = 500
            if damage is None: damage = 15
            self.inventory.weapons.append(
                GrapplingPistol(Trajectory(free_fall, self.size // 2, DEFAULT_GRAPPLING_SPEED, 0, DEFAULT_GRAVITY), projectile_damage=damage))
            
        else:
            print_warning(f"Failed to equip '{name}' to Character: this weapon doesn't exist.")

        self.equipped_weapon = self.inventory.weapons[self.inventory.active_index]
