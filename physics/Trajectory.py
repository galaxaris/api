"""Projectile trajectory preview utilities."""

import math
import pygame


from api.utils import GlobalVariables



class Trajectory:
    """Builds and renders a predicted ballistic path."""

    def __init__(self, player_pos: pygame.Vector2, shot_speed: int, gravity: float, mouse_pos: pygame.Vector2):
        """Initialize a trajectory computation context.

        :param player_pos: Shooter world position.
        :param shot_speed: Initial projectile speed.
        :param gravity: Gravity increment applied per simulation step.
        :param mouse_pos: Cursor position used to compute shoot angle.
        """
        self.angle_radians = None
        self.entity_pos = player_pos
        self.shot_speed = shot_speed
        self.gravity = gravity
        self.trajectory_coordinates = []
        self.mouse_pos = mouse_pos
        self.entity_screen_pos = pygame.Vector2(0,0)
        self.test_collision = []
        self.trajectory_colour = "blue"

    def build_trajectory_coordinates(self):
        """Compute trajectory points until max steps or collision.

        The preview is generated in screen space relative to the current camera.
        Simulation stops early when a predicted point intersects a solid object
        or leaves the screen limits.
        """
        self.trajectory_coordinates.clear()
        cam_pos = GlobalVariables.get_variable("cam_pos")
        self.entity_screen_pos = self.entity_pos - cam_pos

        # Calcul de l'angle par rapport à la position de la souris
        dx, dy = self.mouse_pos / GlobalVariables.get_variable("scale_ratio") - self.entity_screen_pos

        self.angle_radians = math.atan2(-dy, dx)

        if self.mouse_pos == (0, 0):
            self.angle_radians = 1

        # Vitesses initiales
        vx = self.shot_speed * math.cos(self.angle_radians)
        vy = -self.shot_speed * math.sin(self.angle_radians)

        # FIX : Correction des index (0 = width, 1 = height)
        render_size = GlobalVariables.get_variable("render_size")
        render_width = render_size[0]
        render_height = render_size[1]

        # Récupération optimisée des obstacles
        obstacles = [
            obj for obj in GlobalVariables.get_variable("game_objects")
            if "solid" in obj.tags
        ]

        hit = False
        i = 0
        max_steps = 300  # Sécurité pour éviter les boucles infinies (lag)
        dot_spacing = 3

        # Simulation pas-à-pas (Intégration d'Euler)
        current_pos = pygame.Vector2(self.entity_screen_pos)

        while not hit and i < max_steps:
            # Application de la gravité et mise à jour de la position
            vy += self.gravity
            current_pos.x += vx
            current_pos.y += vy

            virtual_traj = pygame.Vector2(current_pos.x, current_pos.y)

            # FIX : Utilisation de "or" pour arrêter la ligne dès qu'elle sort d'un des 4 bords
            if (virtual_traj.x < 0 or virtual_traj.y < 0 or
                    virtual_traj.x > render_width or virtual_traj.y > render_height):
                hit = True
                break

            # Vérification des collisions avec le décor
            virtual_point = pygame.Rect(virtual_traj.x + cam_pos.x, virtual_traj.y + cam_pos.y, 4, 4)
            for obstacle in obstacles:
                if virtual_point.colliderect(obstacle.rect):
                    hit = True
                    break

            if not hit:
                if i % dot_spacing == 0:
                    self.trajectory_coordinates.append(virtual_traj)

            i += 1


    def draw_trajectory(self, surface):
        """Draw previously computed trajectory points.

        :param surface: Destination surface.
        :return:
        """

        trajectory_coordinates = self.trajectory_coordinates
        for point in trajectory_coordinates:
            pygame.draw.circle(surface, self.trajectory_colour, (int(point[0]), int(point[1])), 2)


