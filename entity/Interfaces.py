from dataclasses import dataclass
import pygame

@dataclass
class AimState:
    origin: pygame.Vector2
    shot_angle: float
    shot_speed: float
    gravity: float