"""Gameplay constants shared by multiple systems."""
import pygame

from api.physics.Trajectory import Trajectory


# Trajectory
OFFSET_X = 0
OFFSET_Y = 0

MIN_SHOT_SPEED = 1
MAX_SHOT_SPEED = 100
DEFAULT_SHOT_SPEED = 10


DEFAULT_GRAVITY = 0.1

# Weapon

from api.items.Catalog import Pistol

DEFAULT_WEAPON = Pistol(Trajectory(pygame.Vector2(0,0), DEFAULT_SHOT_SPEED, DEFAULT_GRAVITY, pygame.Vector2(0,0)))