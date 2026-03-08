import pygame

from api.entity.Entity import Entity
from api.utils import GlobalVariables


class Projectile(Entity):
    def __init__(self, pos: tuple[int, int], gravity: float, velocity: pygame.Vector2, angle_radians: float, size: tuple[int, int] = (8,8), effect: str = None, target: str = None):
        super().__init__(pos = pos, size = (8,8))
        self.pos = pygame.Vector2(pos)
        self.set_gravity(gravity)
        self.velocity = velocity
        self.angle_radians = angle_radians
        self.add_tag("projectile")
        self.image = pygame.Surface((8, 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.fall = True



    """def update(self) :
        super().update()

        print("shooting")

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.set_position((self.pos[0], self.pos[1]))

        print(f"Pos: {self.pos}, Vel: {self.vel}")

        if self.collided_objs:
            self.on_impact()"""

    def update(self):
        # Calculer la nouvelle destination
        new_x = self.pos.x + self.vel.x
        new_y = self.pos.y + self.vel.y

        # Utiliser la méthode du parent pour tout mettre à jour d'un coup
        self.set_position((new_x, new_y))

        # Appeler le parent pour la gravité et les collisions
        super().update()


    def on_impact(self) :
        self.kill()


    def kill(self):
        game_objects = GlobalVariables.get_variable("game_objects")
        if self in game_objects:
                game_objects.remove(self)















