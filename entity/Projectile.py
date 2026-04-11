import pygame as pg
import math

from api.entity.Entity import Entity
from api.physics.Collision import get_collided_objects


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, gravity: float, shot_speed: float, angle_radians: float,
                 effect : str = "damage",  target: str="enemy", size: tuple[int, int] | pg.Vector2 = (8,8), damage: int = 10, projectile_speed: int = 0.8, colour = "white", range : int = 1):

        """
        :param pos: the projectile position
        :param gravity: the projectile gravity, the greater it is, the faster the projectile falls
        :param shot_speed: projectile speed
        :param angle_radians: projectile angle
        :param effect: currently ineffective, tags are used instead
        :param target: currently ineffective
        :param size: projectile size
        :param damage: damage dealt to the collided objects
        :param colour: projectile colour
        """

        super().__init__(pos, size)
        self.pos = pg.Vector2(pos) - self.size/2
        self.add_tag("projectile")
        self.image = pg.Surface((8, 8))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft=pos)
        self.range = range
        self.range_reached = False

        self.fall = True
        self.to_kill = False

        self.resistance = 0
        self.damage = damage

        self.projectile_speed = projectile_speed
        adjusted_speed = shot_speed * projectile_speed
        self.vel = pg.Vector2(
            math.cos(angle_radians) * adjusted_speed,
            -math.sin(angle_radians) * adjusted_speed
        )

        self.set_gravity(gravity * (projectile_speed ** 2))
        self.add_tag(effect)
        self.target = target


    def update(self, scene=None):
        # Update every projectile speed to reduce speed
        super().update(scene)
        enemies_collisions = get_collided_objects(self, self.target, scene.game_objects, self.vel.x, self.vel.y)

        if enemies_collisions:
            for obj in enemies_collisions:
                obj[0].take_damage(self.damage)
            self.collided_objs += enemies_collisions

        if self.collided_objs:
            if "bouncy" in self.tags:
                pass

            if "grappling" in self.tags:  # projectile of grappling hook
                for collided_obj in self.collided_objs:
                    if "anchor" in collided_obj[0].tags:  # a block that the player can grapple to move towards it
                        self.gravity = 0
                        self.vel = pg.Vector2(0, 0)
                        self.add_tag("anchored")

                    else:
                        self.on_impact()
            else:
                self.on_impact()

    def on_impact(self):
        self.to_kill = True















