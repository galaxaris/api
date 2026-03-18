from api.GameObject import GameObject


class Inventory(GameObject):
    def __init__(self):
        self.weapons = []  # Liste de Pistol
        self.active_index = 0

    def add_weapon(self, pistol):
        self.weapons.append(pistol)

    def get_current(self):
        return self.weapons[self.active_index] if self.weapons else None

    #utilise les propriétés des gameobject pour dessiner l'ui

