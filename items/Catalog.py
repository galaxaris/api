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

    def consume(self):
        pass

class Grapple(ActiveItem):
    """Base class for grapple."""
    def __init__(self, name, item_type):
        pass

class Pistol(ActiveItem):
    """Base class for pistol."""
    def __init__(self, name: str, item_type: str, is_active: bool,
                 projectile_gravity: float):
        super().__init__(name, item_type, is_active)
        self.projectile_gravity = DEFAULT_GRAVITY
        pass

    def activate(self):
        projectile = Projectile(projectile_type="mud", gravity=DEFAULT_GRAVITY)
        self.projectile_gravity = projectile.gravity
