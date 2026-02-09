import pygame

from api.assets.Texture import Texture


class GameObject(pygame.sprite.Sprite):
    x: int
    y: int
    width: int
    height: int
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=(x, y))

    def set_texture(self, texture:Texture):
        self.image = pygame.transform.scale(texture.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def set_size(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def set_color(self, color: tuple[int, int, int]):
        self.image.fill(color)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
