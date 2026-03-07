from api.items.Item import Item


class ActiveItem(Item):
    """Minimal base class for active items."""

    def __init__(self, name: str, item_type: str, is_equipped: bool ):
        """Initialize the base active item.

        :return:
        """
        super().__init__(name, item_type)
        self.is_equipped = False
        pass

    def unequip(self):
        pass

    def equip(self):
        pass



