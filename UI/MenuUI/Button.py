from dataclasses import dataclass

from api.UI.MenuUI import MenuUI


@dataclass()
class Button(MenuUI):
    label: str

    def set_label(self, new_label: str):
        self.label = new_label