from dataclasses import dataclass
from typing import override
from api.UI import UI
from api.UI.MenuUI import MenuUI

@dataclass()
class Menu(UI):
    title: str
    elements: list[MenuUI]