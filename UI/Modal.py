from api.UI.GameUI import UIElement


class Menu(UIElement):
    def __init__(self, name, items, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.name = name
        self.items = items
        self.pos = pos
        self.size = size

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)