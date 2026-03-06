"""Base item abstractions for gameplay objects."""

class Item:
    """Minimal base class for items."""

    def __init__(self, name: str, item_type: str):
        """Initialize the base item.

        :return:
        """
        self.name = name
        self.item_type = item_type

