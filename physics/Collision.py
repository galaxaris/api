"""Collision helper functions for game objects."""
import math

import pygame as pg
from pygame import Rect

from api.GameObject import GameObject


def get_collided_objects(obj: GameObject, tag: str, others: list[GameObject], dx: float, dy: float) -> list[tuple[GameObject, str]]:
    """Return objects that would collide with `obj` after movement.

    The function predicts collisions using a translated copy of `obj.rect`
    without mutating the real object.

    :param obj: Object being tested.
    :param tag: Optional tag required on potential colliders.
    :param others: Candidate objects to test against.
    :param dx: Horizontal movement applied for prediction.
    :param dy: Vertical movement applied for prediction.
    :return: List of `(collider, direction)` tuples.
    """
    collided_objects = []

    # Correction du "piège des entiers" : on force un mouvement d'au moins 1 pixel
    # ou -1 pixel dans la hitbox prédictive si une vélocité existe.
    move_x = math.ceil(dx) if dx > 0 else math.floor(dx)
    move_y = math.ceil(dy) if dy > 0 else math.floor(dy)

    future_rect = obj.rect.move(move_x, move_y)

    targets = [o for o in others if o.id != obj.id and (tag is None or tag in o.tags)]

    for other in targets:
        if future_rect.colliderect(other.rect):
            direction = get_collision_direction(future_rect, other.rect)
            collided_objects.append((other, direction))

    return collided_objects

def get_collision_direction(subject: Rect, target: Rect):
    """Determine the side of `target` touched by `subject`.

    :param subject: Moving rectangle.
    :param target: Hit rectangle.
    :return: Collision side (`"top"`, `"bottom"`, `"left"`, `"right"`) or `None`.
    """

    dr = subject.right - target.left
    dl = target.right - subject.left
    db = subject.bottom - target.top
    dt = target.bottom - subject.top

    min_overlap = min(dr, dl, db, dt)

    if min_overlap == db: return "top"    # Subject hit top of target
    if min_overlap == dt: return "bottom" # Subject hit bottom of target
    if min_overlap == dr: return "left"   # Subject hit left of target
    if min_overlap == dl: return "right"  # Subject hit right of target
    return None