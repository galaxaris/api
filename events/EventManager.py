"""
Manages events (can be input, mouse, in-game event, etc.) for the game, providing a centralized system to handle user interactions and game events.
=> More efficient & organized, allows to reduce code redundancy and improve maintainability

A map associating an event type with a callback function when triggered, gathered under a name
"""

from typing import Callable

from api.utils.Console import *

class EventManager:
    """
    EventManager class. Handles the registration and execution of events in the game.
    """

    def __init__(self):
        self.Instances = self.Instances()
        self.events = {}    

    class Instances:
        """
        Class to bind instances to the EventManager, to call their methods when an event is triggered.
        """
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
        #LAZY IMPORT to avoid circular imports
        from api.events.DefaultEventCollection import get_default_events

        #Injecting directly the EventManager        
        for event_name, callbacks in get_default_events(self).items():
            for callback in callbacks:
                self.registerEvent(event_name, callback)

    def registerEvent(self, event_name: str, callback: Callable | list[Callable] | tuple[Callable, ...]):
        """
        Registers a single event to the `EventManager`, providing callback(s). If event already exists, adds callback(s)

        :param event_name: Name of the event to be registered (ex: "player_jump", "enemy_attack", etc.)
        :param callback: Callback function when event happens. should take an `event` object as parameter (ex: lambda event: event.Instances.player.do_jump())
        """

        #Register new event if doesn't exist yet
        if event_name not in self.events:
            self.events[event_name] = []


        if isinstance(callback, (tuple, list)):
            self.events[event_name].extend(callback)
        else:
            self.events[event_name].append(callback)

    def unregisterEvent(self, event_name: str):
        """
        Unregisters an event from the `EventManager`.

        :param event_name: Name of the event to be unregistered
        """

        if event_name in self.events:
            del self.events[event_name]
        else:
            print_warning(f"Event '{event_name}' not found in EventManager! Cannot unregister.")

    def triggerEvent(self, event_name: str, event=None):
        """
        Triggers an event, calling all its associated callback functions.

        :param event_name: Name of the event to be triggered
        :param event: Event object to be passed to the callback functions (optional). If None, passes the EventManager itself.
        """

        if event_name in self.events:
            count = 0
            for callback in self.events[event_name]:
                count += 1
                try:
                    callback(event if event is not None else self)
                except AttributeError:
                    print_error(f"Error triggering event '{event_name}'. It's {to_ordinal_number(count)} callback is trying to access an non-existent instance method or an instance that is not bound to EventManager.Instances.") 
                except NameError:
                    print_error(f"Error triggering event '{event_name}'. It's {to_ordinal_number(count)} callback is trying to call a non-existent function.")
                
        else:
            print_warning(f"Event '{event_name}' not found in EventManager.")

    def getRegisteredEvents(self):
        """
        Returns a list of all registered event names.

        :return: List of registered event names
        """
        return list(self.events.keys())