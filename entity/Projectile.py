from api.entity.Entity import Entity


class Projectile(Entity):
    def __init__(self, projectile_type: str, gravity: float):
        self.projectile_type = projectile_type
        self.gravity = gravity


