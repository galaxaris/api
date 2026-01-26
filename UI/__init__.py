from dataclasses import dataclass
from typing import override

from api.GameObject import GameObject


@dataclass()

class UI(GameObject):
    visible: bool
    @override
    def __post_init__(self):
        super().__post_init__()
        self.properties.FIXED_POSITION = True
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False