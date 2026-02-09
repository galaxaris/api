import pygame

from api.assets.Animation import Animation
from api.assets.Texture import Texture

class GameObject(pygame.sprite.Sprite):
    x: int
    y: int
    width: int
    height: int
    rect: pygame.Rect
    image: pygame.Surface
    animation: Animation | None
    direction: str = "right"
    id: int
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation = None
        self.id = id(self)
        self.direction = "right"

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

    def set_animation(self, animation: Animation):
        self.animation = animation

    def update(self):
        if self.animation:
            self.image = pygame.transform.scale(self.animation.get_frame(self.direction), (self.width, self.height))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def set_direction(self, direction: str):
        if direction in ["left", "right"]:
            self.direction = direction

    def draw(self, surface: pygame.Surface):
        self.update()
        surface.blit(self.image, self.rect)
