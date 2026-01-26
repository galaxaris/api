from dataclasses import dataclass
from typing import override

from api.GameObject import GameObject

@dataclass()
class Solid(GameObject):
    hitbox: tuple[float, float]
    super().properties.SOLID = True