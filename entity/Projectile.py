import pygame

from api.entity.Entity import Entity
from api.utils import GlobalVariables


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int], gravity: float, shot_speed: int, angle_radians: float, size: tuple[int, int] = (8,8), effect: str = None, target: str = None):
        super().__init__(pos = pos, size = (8,8))
        self.pos = pygame.Vector2(pos)
        self.set_gravity(gravity)
        self.shot_speed = shot_speed
        self.angle_radians = angle_radians
        self.add_tag("projectile")
        self.image = pygame.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True

#FIXME: update doesn't do anything

    def update(self) :
        pass
        """super().update()

        print("shooting")

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.set_position((self.pos[0], self.pos[1]))

        print(f"Pos: {self.pos}, Vel: {self.vel}")

        if self.collided_objs:
            self.on_impact()"""




    def on_impact(self):
        print("ouch ça fait mal")
        # self.kill()


    def kill(self):
        print("go rejoindre papa Johnny")
        """game_objects = GlobalVariables.get_variable("game_objects")
        if self in game_objects:
                game_objects.remove(self)"""















