"""
Manages events (can be input, mouse, in-game event, etc.) for the game, providing a centralized system to handle user interactions and game events.
=> More efficient & organized, allows to reduce code redundancy and improve maintainability

A map associating an event type with a callback function when triggered, gathered under a name
"""

from api.events.DefaultEventCollection import DefaultEventCollection

class EventManager:
    """
    EventManager class. Handles the registration and execution of events in the game.
    """

    def __init__(self):
        self.Instances = self.Instances()
        self.events = {}    

    class Instances:
        def __init__(self):
            self.game = None
            self.scene = None
            self.player = None
            self.enemy = None
            self.menu = None
            #... add other instances as needed

        def bindInstance(self, attrName, instance):
            """
            Binds an instance to `EventManager.Instances`, to call its methods when an event is triggered.

            Exemple: player, enemy, Menu, etc.

            :param attrName: Name of the instance to be bound, used to call its methods (ex: "player" to call player.do_jump())
            :param instance: Instance to be bound
            """
        
            setattr(self, attrName, instance)

        def bindInstancesDict(self, instances: dict[str, object]):
            """
            Binds multiple instances to `EventManager.Instances` at once.

            :param instances: Dictionary of instances to be bound (key: attrName, value: instance)  
            """

            for attrName, instance in instances.items():
                self.bindInstance(attrName, instance)


    def registerDefaultEventCollection(self):
        """
        Registers default events from `DefaultEventCollection` to the `EventManager`.

        """

        self.events.update(DefaultEventCollection)

    def registerEvent(self, event_name: str, callback: callable):
        """
        Registers a single event to the `EventManager`.

        :param event_name: Name of the event to be registered (ex: "player_jump", "enemy_attack", etc.)
        :param callback: Callback function when event happens. should take an `event` object as parameter (ex: lambda event: event.Instances.player.do_jump())
        """

        if event_name in self.events:
            self.events[event_name].append(callback)
        else:
            self.events[event_name] = [callback]