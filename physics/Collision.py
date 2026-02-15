import pygame as pg

from api.GameObject import GameObject

def check_collide(a: GameObject, b: GameObject) -> bool:
    if a.mask and b.mask:
       if pg.sprite.collide_mask(a,b):
              return True
    return False

def get_collided_objects(obj: GameObject, tag: str)-> list[GameObject]:
    collided_objects = []
    return []
