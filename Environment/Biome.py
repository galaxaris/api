from dataclasses import dataclass

from api.Environment.Background import ParallaxBackground, Background
from api.Utils.Music import Music


@dataclass
class Biome:
    name: str
    background: ParallaxBackground | Background
    effects: list[str]
    ambient_sound: Music