from utils import *

class Level:
    """
    Level is a class that manage the levels from the saving to the loading.
    """

    def __init__ (self,name:str):
        """
        Any object of the class is initialized with the path that brings to the level's file and the name of the file.
        :param name: Name of the directory you are aiming.
        :param header: A dictionary that contains data needed to save or load the header.
        :param body: A dictionary that contains data needed to save or load the body.
        """

        self.name = name
        self.path , self.new= treat_path(name)
        self.header= None
        self.body= None

    def save_level (self):
        if (self.new):
            pass
        pass

    def load_level (self):
        pass