import math

from api.UI.ProgressBar import ProgressBar
from api.entity.Character import Character
import pygame as pg

from api.items.Catalog import Pistol
from api.physics.Collision import get_collided_objects
from api.physics.Trajectory import Trajectory, free_fall, calculate_required_speed_from_freefall, apply_accuracy
from api.utils import Debug
from api.utils.Constants import DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY, MAX_SHOT_SPEED, MIN_SHOT_SPEED


class Enemy(Character):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], health: int = 100, speed: float|int = 2, mode: str = "patrol", range: int = 100, accuracy: float = 0.8):
        super().__init__(pos, size, health)
        self.speed = speed
        self.range = range
        self.mode = mode

        color_bar = (255, 0, 0) if self.health > self.original_health // 2 else (255, 255, 0)
        self.enemy_progress_bar = ProgressBar((self.pos.x, self.pos.y - 10), (self.size.x, 5), (100, 100, 100), color_bar, progress_max=100)
        self.equipped_weapon = Pistol(Trajectory(free_fall, self.size // 2, DEFAULT_SHOT_SPEED, 0, DEFAULT_GRAVITY, color=(220, 10, 10)), target="player", cooldown=1000)
        self.accuracy = accuracy
        self.add_tag("enemy")

    def update(self, scene=None):
        super().update(scene)
        layer = "#enemyHealthBar"
        if self.health < self.original_health:
            if self.health < self.original_health // 2:
                self.enemy_progress_bar.set_color((255, 255, 0))
            else:
                self.enemy_progress_bar.set_color((255, 0, 0))
            self.enemy_progress_bar.set_progress(self.health)
            self.enemy_progress_bar.set_position((self.pos.x, self.pos.y - 10) - scene.camera.position)
            scene.add(self.enemy_progress_bar, layer)
        else:
            scene.remove(self.enemy_progress_bar, layer)


        if self.mode != "turret":
            self.equipped_weapon.is_aiming = False

        if self.mode == "patrol":
            self.do_patrol(scene)
        elif self.mode == "chase":
            self.do_chase(scene)
        elif self.mode == "turret":
            self.do_turret(scene)

    def do_patrol(self, scene):
        if Debug.is_enabled("colliders"):
            red_line = pg.Surface((self.range, 1))
            red_line.fill((255, 0, 0))
            scene.blit(red_line, (self.start_pos.x - scene.camera.position.x + self.size.x//2, self.pos.y - scene.camera.position.y + self.size.y // 2))

        if not self.collided_objs:
            return
        self.vel.x = self.speed * scene.Time.deltaTime

        if self.pos.x > self.start_pos.x + self.range:
            self.speed = -abs(self.speed)
            self.set_direction("left")
        elif self.pos.x < self.start_pos.x:
            self.speed = abs(self.speed)
            self.set_direction("right")

    def do_chase(self, scene):
        # 1. Calculs logiques dans l'ESPACE MONDE (indépendant de la caméra)
        range_box_world = pg.Rect(
            self.pos.x - (self.range // 2) + (self.size.x // 2),
            self.pos.y - self.range + self.size.y,
            self.range,
            self.range
        )

        # 2. Affichage Debug dans l'ESPACE ÉCRAN (en appliquant l'offset de la caméra)
        if Debug.is_enabled("colliders"):
            # On décale le rectangle du monde vers l'écran pour le dessiner
            range_box_screen = range_box_world.move(-scene.camera.position.x, -scene.camera.position.y)
            pg.draw.rect(scene, (255, 255, 0), range_box_screen, width=1)

        # 3. Recherche du joueur et logique de poursuite
        for obj in scene.game_objects:
            if "player" in obj.tags:
                player = obj
                # Centre du joueur dans l'espace monde
                player_center = (player.pos.x + player.size.x // 2, player.pos.y + player.size.y // 2)

                # Si le joueur entre dans la zone de détection
                if range_box_world.collidepoint(player_center):

                    # Déterminer la direction (gauche ou droite)
                    diff_x = player.pos.x - self.pos.x

                    # Deadzone : Évite que l'ennemi ne "vibre" s'il est exactement sur le même pixel que le joueur
                    if abs(diff_x) > 2:
                        if diff_x > 0:
                            # Le joueur est à droite
                            self.vel.x = abs(self.speed) * scene.Time.deltaTime
                            self.set_direction("right")
                        else:
                            # Le joueur est à gauche
                            self.vel.x = -abs(self.speed) * scene.Time.deltaTime
                            self.set_direction("left")
                    else:
                        # L'ennemi a atteint le joueur sur l'axe X
                        self.vel.x = 0

                break  # On arrête la boucle après avoir géré le joueur

    def do_turret(self, scene):
        # 1. Calculs logiques dans l'ESPACE MONDE (indépendant de la caméra)
        range_box_world = pg.Rect(
            self.pos.x - (self.range // 2) + (self.size.x // 2),
            self.pos.y - self.range//2 + self.size.y//2,
            self.range,
            self.range
        )

        # 2. Affichage Debug dans l'ESPACE ÉCRAN (en appliquant l'offset de la caméra)
        if Debug.is_enabled("colliders"):
            # On décale le rectangle du monde vers l'écran pour le dessiner
            range_box_screen = range_box_world.move(-scene.camera.position.x, -scene.camera.position.y)
            pg.draw.rect(scene, (255, 255, 0), range_box_screen, width=1)

        # 3. Recherche du joueur et logique de tir
        for obj in scene.game_objects:
            if "player" in obj.tags:
                player = obj
                # Centre du joueur dans l'espace monde
                player_center = (player.pos.x + player.size.x // 2, player.pos.y + player.size.y // 2)

                # Si le joueur entre dans la zone de détection
                if range_box_world.collidepoint(player_center):
                   self.equipped_weapon.is_aiming = True
                   dx = player_center[0] - (self.pos.x + self.size.x // 2)
                   dy = (self.pos.y + self.size.y // 2) - player_center[1]  # Inversé pour que Y+ soit vers le haut

                   # 2. On fixe un angle (ex: 45 degrés vers la cible)
                   angle = math.radians(45) if dx > 0 else math.radians(135)
                   self.equipped_weapon.trajectory.angle_radians = apply_accuracy(angle, self.accuracy)

                   # 3. Calcul de la vitesse avec la hauteur
                   self.equipped_weapon.trajectory.ini_speed = calculate_required_speed_from_freefall(
                       self.equipped_weapon.gravity,
                       abs(dx),
                       angle if dx > 0 else math.pi - angle,  # Ajustement du cos/tan selon la direction
                       dy
                   )

                   # Accuracy malus : on ajoute une variabilité aléatoire à la trajectoire pour simuler une précision imparfaite


                   self.equipped_weapon.shoot(self.pos + self.size//2)
                else:
                    self.equipped_weapon.is_aiming = False
                break  # On arrête la boucle après avoir géré le joueur

