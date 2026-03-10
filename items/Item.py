"""Base item abstractions for gameplay objects."""
from api.GameObject import GameObject


class Item(GameObject):
    """Minimal base class for items."""

    def __init__(self, name: str, item_type: str):
        """Initialize the base item.

        :return:
        """
        super().__init__((0,0), (1,1))
        self.name = name
        self.item_type = item_type

