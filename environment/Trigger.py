from api.GameObject import GameObject
import pygame as pg

class Trigger(GameObject):
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], 
                 target_tags: list[str], actions: list[callable], actions_arg: list = None, once: bool = False):
        super().__init__(pos, size)

        self.add_tag("trigger")
        self.target_tags = target_tags
        self.actions = actions
        self.actions_arg = actions_arg
        self.once = once

    def add_action(self, action):
        if not hasattr(self, "actions"):
            self.actions = []
        self.actions.append(action)

    def remove_action(self, action):
        if action in self.actions:
            self.actions.remove(action)
        else:
            print("== Warning: action does not exists in trigger ==")

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

    def update(self, others):
        super().update(others)
        for obj in others:
            if any(tag in obj.tags for tag in self.target_tags): #Checks if the object has any of the target tags
                print(f"Trigger activated by object with tags: {obj.tags}")
                for i, action in enumerate(self.actions):
                    if self.actions_arg and i < len(self.actions_arg):
                        print(f"Executing action {action.__name__} with argument {self.actions_arg[i]}")
                        action(self.actions_arg[i]) #This precise line launches the action (with args)
                    else:
                        action() #This precise line launches the action
                if self.once:
                    self.remove_trigger()


class Trigger_KillBox(Trigger):
    _EDITOR = "placeable"
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], target_tags: list[str], game: object, once: bool = False):
        self.game = game
        super().__init__(pos, size, target_tags, [], None, once)

    def update(self, others):
        super().update(others)
        for obj in others:
            if any(tag in obj.tags for tag in self.target_tags):
                if hasattr(obj, "kill"):
                    obj.kill(self.game)
                else:
                    print("== Warning: object does not have a kill method ==")