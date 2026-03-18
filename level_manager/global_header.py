import json


class GlobalHeader:
    """
    This class is used to match some GameObject to their properties to remove possible redundancy in the level's file.

    Structure : The JSON file can be represented as a list of dictionaries that have as a key the name of the GameObject, and as value all it properties;

    """

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
