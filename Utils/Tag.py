from dataclasses import dataclass

@dataclass()
class Tag:
    name: str
    enabled: bool
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False