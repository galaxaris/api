from api.items.Item import Item


class ActiveItem(Item):
    """Minimal base class for active items."""

    def __init__(self, name: str, item_type: str, is_active: bool ):
        """Initialize the base active item.

        :return:
        """
        super().__init__(name, item_type)
        self.is_active = False
        pass

    def activate(self):
        pass

