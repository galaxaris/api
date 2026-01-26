from dataclasses import dataclass

from api.Character.Weapon import Weapon
from api.GameObject import GameObject
from api.Texture.Animation import Animation


class AnimationCollection:
    WALK: Animation
    ATTACK: Animation
    DIE: Animation
    IDLE: Animation
    JUMP: Animation
    SHOOT: Animation


@dataclass()
class Character(GameObject):
    health: int
    animation: AnimationCollection
    weapon: Weapon
    playable: bool
