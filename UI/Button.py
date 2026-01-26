from dataclasses import dataclass

from api.Texture.Variant import Variant
from api.UI import UI
from api.Utils.Tag import Tag


@dataclass()
class Button(UI):
    label: str
    call: Tag
    variant: Variant
    def set_label(self, new_label: str):
        self.label = new_label
