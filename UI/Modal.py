from api.UI.GameUI import UIElement


class Modal(UIElement):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.elements: list[UIElement] = []

    def add_element(self, element: UIElement):
        self.elements.append(element)

    def update(self):
        for element in self.elements:
            element.update()
