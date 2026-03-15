from api.GameObject import GameObject
from api.physics.Collision import get_collided_objects
import pygame as pg

class Trap(GameObject):
    """Base class for trap."""
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2, target: str="player", damage: int = 10, cooldown: int = 2000):
        super().__init__(pos, size)
        self.collided_objs = None
        self.add_tag("trap")
        self.target = target
        self.damage = damage
        self.cooldown = cooldown
        self.last_triggered = 0
        
    def update(self, scene=None) :
        # Update every projectile speed to reduce speed
        super().update(scene)
        enemies_collisions = get_collided_objects(self, self.target, scene.game_objects, 0, 0)

        now = pg.time.get_ticks()

        if now - self.last_triggered < self.cooldown:
            self.set_texture_bound("idle", rescale=True)
            return

        self.set_texture_bound("active", rescale=True)
        if enemies_collisions:
            self.last_triggered = now
            for obj in enemies_collisions:
                obj[0].take_damage(self.damage)
