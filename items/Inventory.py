from api.UI.GameUI import UIElement, GameUI


class Inventory(UIElement):
    def __init__(self, pos=(0,0), size=(0,0)):
        super().__init__(pos, size)
        self.items = []
        self.UI = GameUI(size)
