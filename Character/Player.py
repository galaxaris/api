from dataclasses import dataclass
from typing import override

from api.Character import Character


@dataclass()
class Player(Character):
    super().playable = True
    def jump(self):
        pass
    def attack(self):
        pass
    def interact(self):
        pass
    def move(self, direction: tuple[float, float]):
        pass
