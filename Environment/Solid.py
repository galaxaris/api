from dataclasses import dataclass
from typing import override

from api.GameObject import GameObject

@dataclass()
class Solid(GameObject):
    hitbox: tuple[float, float]
    @override
    def __post_init__(self):
        super().__post_init__()
        self.properties.SOLID = True