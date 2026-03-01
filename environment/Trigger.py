from api.GameObject import GameObject
from api.utils.GlobalVariables import get_variable
import pygame as pg

class Trigger(GameObject):
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], 
                 target_tags: list[str], callbacks: list[callable], once: bool = False):
        super().__init__(pos, size)

        self.add_tag("trigger")
        self.target_tags = target_tags
        #"Callback" : fonction passée en paramètre d'une autre fonction, qui sera appelée plus tard.
        #Python : méthode classique (sans args) : "nom_fonction", SANS les "()". Sinon fonction exécutée immédiatement. Son return est passé en param.
        #Pour passer avec les arguments, on peut utiliser lambda ou partial : 
        #== Lambda ==
        # lambda: nom_fonction(arg1, arg2)
        #== Partial (considéré comme légèrement plus opti)==
        # from functools import partial
        # partial(nom_fonction, arg1, arg2)
        
        self.callbacks = callbacks  #Les callbacks (callbacks) doivent déjà inclure leurs arguments (via partial ou lambda)
        self.once = once
        self.objects_inside = set()  #Track objects already in trigger to avoid repeated activation

    def add_callback(self, callback):
        if not hasattr(self, "callbacks"):
            self.callbacks = []
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)
        else:
            print("== Warning: callback does not exists in trigger ==")

    def add_target_tag(self, tag):
        if not hasattr(self, "target_tags"):
            self.target_tags = []
        self.target_tags.append(tag)

    def remove_target_tag(self, tag):
        if tag in self.target_tags:
            self.target_tags.remove(tag)
        else:
            print("== Warning: target tag does not exists in trigger ==")

    def remove_trigger(self):
        self.remove_tag("trigger")
        self.callbacks = []

    def update(self):
        super().update()
        
        #Récupérer tous les objets de la scène
        game_objects = get_variable("game_objects")
        
        #Track current objects in trigger for this frame
        current_objects = set()
        
        for obj in game_objects:
            #Vérifier si l'objet a un des tags ciblés
            if any(tag in obj.tags for tag in self.target_tags):
                #Vérifier la collision réelle avec le trigger
                if self.rect.colliderect(obj.rect):
                    current_objects.add(obj.id)
                    
                    #Si l'objet vient d'entrer dans le trigger
                    if obj.id not in self.objects_inside:
                        #Exécuter toutes les callbacks (passer l'objet en paramètre)
                        for callback in self.callbacks:
                            try:
                                callback(obj)
                            except TypeError:
                                #Si les paramètres ont déjà été passés via lambda ou partial
                                callback()
                        
                        if self.once:
                            self.remove_trigger()
                            return
        
        #Track objects that have exited the trigger
        exited_objects = self.objects_inside - current_objects
        for obj_id in exited_objects:
            self.objects_inside.discard(obj_id)

        #Add new objects to the tracking set
        self.objects_inside.update(current_objects)


class Trigger_KillBox(Trigger):
    #TODO: WARNING: very long width GameObject are not well handled by the collision system... 
    #(see in debug mode, for x > 1000px, killbox disappears & collision doesn't work anymore)

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target_tags: list[str], game: object, once: bool = False):
        self.game = game
        
        #Définir le callback de kill dans le constructeur
        def kill_callback(obj):
            if hasattr(obj, "kill"):
                obj.kill(self.game)
            else:
                print(f"== Warning: object {obj} does not have a kill method ==")
        
        #Passer le callback au constructeur parent
        super().__init__(pos, size, target_tags, [kill_callback], once)