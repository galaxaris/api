from utils import *
import json

class Level:
    """
    Level is a class that manage the levels from the saving to the loading.
    """

    def __init__ (self,name:str):
        """
        Any object of the class is initialized with the path that brings to the level's file and the name of the file.
        :param name: Name of the directory you are aiming.
        """

        self.name = name
        self.path , self.new= treat_path(name)
        self.header= None
        self.body= None

    def save_level (self, header:dict, body:dict):

        self.header = header
        self.body = body

        #Thanks to json.dump, we don't have to manage the saving of files, and it will do it for us.

        try:
            with open(os.path.join(self.path,"header")) as h_file:
                json.dump(self.header, h_file, indent=2)
            with open(os.path.join(self.path,"body")) as b_file:
                json.dump(self.body, b_file, indent=2)

        except FileNotFoundError:
            print("ERROR : The procedure to save file failed. Please verify the integrity of the file at : "+self.path+";")

        pass

    def load_level (self):

        pass