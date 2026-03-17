import json


class GlobalHeader:

    def __init__(self, path:str):

        self.path=path
        self.content = []

    def add_to_global(self, new_prop : dict):

        if(not isinstance(new_prop, dict)):
            raise TypeError

        with open(self.path, 'r', encoding="utf-8") as file:
            self.content = json.load(file)
        self.content.append(new_prop)

        with open(self.path, 'w', encoding="utf-8") as file:
            json.dump(self.content, file , indent=2)
