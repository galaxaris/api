from dataclasses import dataclass
from api.UI import UI



@dataclass()
class Menu(UI):
    title: str
    elements: list[UI]
    def open(self):
        pass
    def close(self):
        pass