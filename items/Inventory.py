from api.UI.GameUI import UIElement, GameUI


class Inventory(UIElement):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.items = []
        self.UI = GameUI(size)
