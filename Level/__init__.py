from dataclasses import dataclass

from api.Environment.Biome import Biome
from api.GameObject import GameObject
from api.Level.Grid import Grid
from api.Utils.Data import Data
from api.Utils.Music import Music


@dataclass()
class Level(Data):
    name: str
    description: str
    author: str
    size: tuple[int, int]
    definition: list[tuple[str,GameObject]]
    grid: Grid
    background: Biome
    music: Music