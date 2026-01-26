from dataclasses import dataclass

from api.Character import Character
from api.Story.Dialog import Dialog


@dataclass()
class PNJ(Character):
    dialog: Dialog
    super().playable = False