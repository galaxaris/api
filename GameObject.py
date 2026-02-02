import uuid
from dataclasses import dataclass, field
from pygame import Vector2

from api.Event import Event
from api.Texture import Texture
from api.Utils.Tag import Tag


@dataclass()
class GameObjectProperties:
    SOLID: bool = False
    FIXED_POSITION: bool = False
    BREAKABLE: bool = False

'''
:param id: Unique identifier for the game object
:param name: Name of the game object
:param type: Type/category of the game object (e.g., 'enemy', 'player', 'item')
:param position: 2D position of the game object in the game world
:param rotation: Rotation angle of the game object in degrees
:param scale: Scale factors of the game object along x, y, and z axes
:param is_active: Boolean indicating if the game object is active
:param texture: Texture object associated with the game object
:param properties: GameObjectProperties defining specific attributes of the game object
:param tags: List of tags associated with the game object
'''
@dataclass()
class GameObject:
    _id: int = field(default=uuid.uuid4().int, init=False)
    name: str
    type: str
    position: Vector2
    rotation: int
    is_active: bool
    texture: Texture
    tags: list[Tag]
    properties: GameObjectProperties
    events: list[Event]
    def activate(self):
        self.is_active = True
    def deactivate(self):
        self.is_active = False
    def move(self, new_position: Vector2):
        self.position = new_position
    def rotate(self, new_rotation: int):
        self.rotation = new_rotation


