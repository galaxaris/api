from collections.abc import Callable
from dataclasses import dataclass

from api.Utils.Tag import Tag


@dataclass()
class Event:
    name: str
    trigger: Tag
    callback: Callable
    state: bool = True
    def execute(self, *args, **kwargs):
        if self.trigger.enabled & self.state:
            return self.callback(*args, **kwargs)
        else:
            return None
    def enable(self):
        self.state = True
    def disable(self):
        self.state = False
