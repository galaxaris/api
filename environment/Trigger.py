"""
API's Triggers definition, collection & implementation
"""

import random as rd

from api.GameObject import GameObject
from api.utils import InputManager, Fonts
from api.utils.Console import *
import pygame as pg

class Trigger(GameObject):
    """
    Trigger class, based on GameObject class. Contains all the trigger's attributes and methods.
    """
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], 
                 target_tags: set[str], callbacks: list[callable], once: bool = False):
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

        self.track_object = True
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
            print_warning("callback does not exists in trigger")

    def add_target_tag(self, tag):
        """
        Adds a target tag to the trigger.

        :param tag: Entity tag to be targeted
        :return:
        """
        if not hasattr(self, "target_tags"):
            self.target_tags = set()
        self.target_tags.add(tag)

    def remove_target_tag(self, tag):
        """
        Removes a target tag from the trigger. If the tag does not exist, a warning is printed.

        :param tag:  Entity tag to be removed
        :return:
        """
        if tag in self.target_tags:
            self.target_tags.remove(tag)
        else:
            print_warning("target tag does not exists in trigger")

    def remove_trigger(self):
        """
        Removes the trigger from the game.
        
        :return:
        """
        self.remove_tag("trigger")
        self.callbacks = []

    def update(self, scene=None):
        """
        Checks for collisions with target objects (tags) and executes callbacks if the trigger is activated.

        Also tracks objects currently inside the trigger to avoid repeated activations.

        :return:
        """
        super().update(scene)
        
        #Récupérer tous les objets de la scène
        game_objects = scene.game_objects
        
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
                    elif not self.track_object:
                        #Si l'objet est déjà dans le trigger mais que le suivi n'est pas activé, exécuter les callbacks à chaque frame
                        for callback in self.callbacks:
                            try:
                                callback(obj)
                            except TypeError:
                                callback()
        
        #Track objects that have exited the trigger
        exited_objects = self.objects_inside - current_objects
        for obj_id in exited_objects:
            self.leave_trigger(obj_id, scene)
            self.objects_inside.discard(obj_id)

        #Add new objects to the tracking set
        self.objects_inside.update(current_objects)

    def leave_trigger(self, obj_id, scene=None):
        pass


class TriggerKillBox(Trigger):
    """
    A specific class for creating a killBox.

    A killBox is a trigger that kills the targeted object when activated.

    Usage: kill the player when falling too much, traps, lava...
    
    Uses a predefined callback (obj.kill())
    """

    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target_tags: set[str], once: bool = False, sfx: list[str] | None = None):
        """
        Initializes the trigger with the given attributes.

        :param pos: killBox position
        :param size: killBox size
        :param target_tags: killbox's target tags (usually "player"). Warning: the tags's entities must have a "kill()" method
        :param once: whether the killbox should be activated only once
        :param sfx: sound effect to play when the trigger is activated
        """
        
        #Définir le callback de kill dans le constructeur
        def kill_callback(obj):
            """
            Calls the kill() method of the object if it has one, otherwise prints a warning.
            
            :param obj: Object to be killed
            :return:
            """
            #Checks if it is the player (only the player, and not a projectile)
            if hasattr(obj, "kill") and "player" in obj.tags and "projectile" not in obj.tags:
                obj.respawn()
                if sfx:
                    AudioManager = self.audio_manager
                    sfx_to_play = rd.choice(sfx) if isinstance(sfx, list) else sfx
                    AudioManager.play_sfx(sfx_to_play)

            #For killing projectiles
            elif hasattr(obj, "on_impact"):
                obj.on_impact()
            else:
                print_warning(f"object {obj} does not have a kill or on_impact method")
        
        #Passer le callback au constructeur parent
        super().__init__(pos, size, target_tags, [kill_callback], once)

class TriggerInteract(Trigger):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target_tags: set[str], callbacks: list[callable], once: bool = False, sfx: str | None = None, trigger_surface: pg.Surface | None = None):
        """
            Trigger which need the player to interact (press a key) to be activated. Used for doors, levers, NPC interactions...

            :param pos: killBox position
            :param size: killBox size
            :param target_tags: killbox's target tags (usually "player"). Warning: the tags's entities must have a "kill()" method
            :param once: whether the killbox should be activated only once
            :param sfx: sound effect to play when the trigger is activated
        """
        self.enabled = False  #Whether the trigger can be activated (can be used to disable the trigger after activation without removing it)
        self.trigger_surface = trigger_surface
        if self.trigger_surface:
            self.BOX_DIM = pg.Vector2(self.trigger_surface.get_size())

        def interact_callback(obj: GameObject):
            """
            Apply a box upper the object to indicate the interaction, and wait for the player to press the "interact" key (default: E) to execute the interaction. The callback function must be passed with the interaction logic (via lambda or partial) and will be executed when the key is pressed.


            :param obj: Object to be interacted with
            :return:
            """
            obj.in_trigger_interact = True
            correct_text = InputManager.get_str_input("interact")
            self.BOX_DIM = pg.Vector2(20, 20)
            self.trigger_surface = pg.Surface(self.BOX_DIM, pg.SRCALPHA, 32).convert_alpha()
            self.trigger_surface.fill((255, 255, 255, 128))  # White box with 50% opacity
            text = Fonts.get_font(Fonts.DEFAULT_FONT, 16).render(correct_text, False,
                                                                           (0, 0, 0))
            self.trigger_surface.blit(text, (self.BOX_DIM.x // 2 - text.get_width() // 2,
                                             self.BOX_DIM.y // 2 - text.get_height() // 2.5))  # Center the "E" text in the box

            if not self.enabled and self.surface:
                self.surface.blit(self.trigger_surface, self.pos - self.offset + (self.size.x//2,-self.size.y//2) - (self.BOX_DIM.x//2,self.BOX_DIM.y//2) ) # Position the box above the trigger

                #Wait for the player to press the "interact" key
            inputs = InputManager.get_inputs()
            if obj.interact and not self.enabled:

                self.enabled = True
                for callback in callbacks:
                    try:
                        callback(obj)
                    except TypeError:
                        callback()

                if sfx:
                    AudioManager = self.audio_manager
                    AudioManager.play_sfx(sfx)





        super().__init__(pos, size, target_tags, [interact_callback], once)
        self.track_object = False

    def leave_trigger(self, obj_id, scene=None):
        game_obj = next((obj for obj in scene.game_objects if obj.id == obj_id), None)
        if game_obj:
            game_obj.in_trigger_interact = False
        self.enabled = False