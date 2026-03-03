"""
API's Triggers definition, collection & implementation
"""

from api.GameObject import GameObject
from api.utils.GlobalVariables import get_variable
import pygame as pg

class Trigger(GameObject):
    """
    Trigger class, based on GameObject class. Contains all the trigger's attributes and methods.
    """
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], 
                 target_tags: list[str], callbacks: list[callable], once: bool = False):
        """
        Initializes the trigger with the given attributes.

        :param pos: Trigger position
        :param size: Trigger size
        :param target_tags: Tags of the objects (usually entities) that will trigger the trigger
        :param callbacks: Callbacks (actions, functions) to execute when the trigger is activated
        :param once: If True, the trigger will be removed after the first activation
        """
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
        """
        Adds a callback to the trigger.

        :param callback: Callback function to be executed when the trigger is activated
        :return:
        """
        if not hasattr(self, "callbacks"):
            self.callbacks = []
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        """
        Removes a callback from the trigger. If the callback does not exist, a warning is printed.

        :param callback: Callback function to be removed
        :return:
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)
        else:
            print("== Warning: callback does not exists in trigger ==")

    def add_target_tag(self, tag):
        """
        Adds a target tag to the trigger.

        :param tag: Entity tag to be targeted
        :return:
        """
        if not hasattr(self, "target_tags"):
            self.target_tags = []
        self.target_tags.append(tag)

    def remove_target_tag(self, tag):
        """
        Removes a target tag from the trigger. If the tag does not exist, a warning is printed.

        :param tag:  Entity tag to be removed
        :return:
        """
        if tag in self.target_tags:
            self.target_tags.remove(tag)
        else:
            print("== Warning: target tag does not exists in trigger ==")

    def remove_trigger(self):
        """
        Removes the trigger from the game. (TODO: for now, it's just a tag removal and callbacks reset, but it should be removed from the scene's game objects list to free memory)
        
        :return:
        """
        self.remove_tag("trigger")
        self.callbacks = []

    def update(self):
        """
        Checks for collisions with target objects (tags) and executes callbacks if the trigger is activated.

        Also tracks objects currently inside the trigger to avoid repeated activations.

        :return:
        """
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
    """
    A specific class for creating a killBox.

    A killBox is a trigger that kills the targeted object when activated.

    Usage: kill the player when falling too much, traps, lava...
    
    Uses a predefined callback (obj.kill())
    """
    #TODO: WARNING: very long width GameObject are not well handled by the collision system... 
    #(see in debug mode, for x > 1000px, killbox disappears & collision doesn't work anymore)

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target_tags: list[str], once: bool = False):
        """
        Initializes the trigger with the given attributes.

        :param pos: killBox position
        :param size: killBox size
        :param target_tags: killbox's target tags (usually "player"). Warning: the tags's entities must have a "kill()" method
        :param once: whether the killbox should be activated only once
        """
        
        #Définir le callback de kill dans le constructeur
        def kill_callback(obj):
            """
            Calls the kill() method of the object if it has one, otherwise prints a warning.
            
            :param obj: Object to be killed
            :return:
            """
            if hasattr(obj, "kill"):
                obj.kill()
            else:
                print(f"== Warning: object {obj} does not have a kill method ==")
        
        #Passer le callback au constructeur parent
        super().__init__(pos, size, target_tags, [kill_callback], once)