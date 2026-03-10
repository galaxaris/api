import pygame

from api.entity.Entity import Entity
from api.physics.Collision import get_collided_objects
from api.utils import GlobalVariables


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int], gravity: float, shot_speed: int, angle_radians: float, size: tuple[int, int] = (8,8), effect: str = None, target: str = None, offset=pygame.Vector2(0, 0)):
        super().__init__(pos = pos, size = (8,8))
        self.pos = pygame.Vector2(pos)

        self.shot_speed = shot_speed
        self.angle_radians = angle_radians
        self.add_tag("projectile")
        self.image = pygame.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True
        self.to_kill = False
        self.offset = None
        self.set_gravity(gravity)


    def update(self) :
        super().update()

        if self.collided_objs:
            print(self.collided_objs[0][0].pos)
            self.on_impact()




    def on_impact(self):
        self.to_kill = True















