from api.GameObject import GameObject


class UIElement(GameObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(pos, size)
        self.add_tag("ui")