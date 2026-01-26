from dataclasses import dataclass

from api.Utils.AssetPath import AssetPath


@dataclass
class Weapon:
    name: str
    damage: int
    range: float
    texture: AssetPath
