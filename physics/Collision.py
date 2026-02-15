import pygame as pg
from pygame import Rect

from api.GameObject import GameObject


def get_collided_objects(obj: GameObject, tag: str, others: list[GameObject], dx: float, dy: float) -> list[tuple[GameObject, str]]:
    collided_objects = []


    future_rect = obj.rect.move(dx, dy)

    for other in others:
        if obj.id != other.id and (tag is None or tag in other.tags):
            if future_rect.colliderect(other.rect):
                direction = get_collision_direction(future_rect, other.rect)
                collided_objects.append((other, direction))

    return collided_objects

def get_collision_direction(subject: Rect, target: Rect):

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