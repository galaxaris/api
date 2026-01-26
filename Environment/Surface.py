from dataclasses import dataclass

from api.Environment.Solid import Solid
from api.Utils.Music import Music


@dataclass()
class Surface(Solid):
    friction: float
    sfx: Music
    def set_friction(self, friction: float):
        self.friction = friction