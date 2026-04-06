import json


class GlobalHeader:
    """
    This class is used to match some GameObject to their properties to remove possible redundancy in the level's file.

    FILE Structure : The JSON file can be represented as a list of dictionaries that have as a key the name of the GameObject, and as value all it properties;

    """

    def __init__(self, path:str):

        self.path=path
        self.known = set()
        self.content = {}

    def add_to_known(self, new_prop_name: str):
        """
        This method actualizes the attributes known to make sure we don't duplicate some values in the JSON file
        :return:
        """

        self.known.add(new_prop_name)

    def get_content(self):
        """
        This method imports all the datas in the JSON file GlobalHeader.
        :return:
        """
        with open(self.path, 'r', encoding="utf-8") as file:
            self.content = json.load(file)

        for key in self.content.keys():
            self.add_to_known(key)



    def add_to_global(self, new_prop : dict)->bool:
        """
        This method add a new prop in the JSON file if it doesn't exist in this one.
        :param new_prop:    dict -> contains the datas about the new object;
        :return:            bool -> represent if we added the new_prop to the datas;
        """
        if(not isinstance(new_prop, dict)):
            raise TypeError

        self.get_content()

        if(len(self.known) == len(self.known | set(new_prop["name"]))):
            return False

        name = new_prop["name"]
        del new_prop["name"]
        self.content[name]= new_prop
        new_prop["name"]=name

        with open(self.path, 'w', encoding="utf-8") as file:
            json.dump(self.content, file , indent=2)
        return True

