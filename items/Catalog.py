from api.entity.Projectile import Projectile
from api.items.ActiveItem import ActiveItem
from api.items.Item import Item
from api.utils.Constants import DEFAULT_GRAVITY


class HealthPotion(Item):
    """Base class for health potion."""
    quantity: int
    def __init__(self, name, item_type):
        """Initialize the health potion."""
        pass

class Grapple(ActiveItem):
    """Base class for grapple."""
    def __init__(self, name, item_type, is_equipped: bool):
        super().__init__(name, item_type, is_equipped)
        pass



class Pistol(ActiveItem):
    """Base class for pistol."""
    def __init__(self, name: str, item_type: str, is_equipped: bool,
                 ammo_gravity: float = DEFAULT_GRAVITY):
        super().__init__(name, item_type, is_equipped)
        self.ammo_gravity = ammo_gravity


    def activate(self):
        pass

