import pygame

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
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
