from dataclasses import dataclass
from typing import override

from api.GameObject import GameObject


@dataclass()

class UI(GameObject):
    visible: bool
    super().properties.FIXED_POSITION = True
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False