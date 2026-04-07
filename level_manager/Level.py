
from utils import *
import json
from api.engine.Scene import *
import importlib
from global_header import *
from api.GameObject import *
from api.assets.Resource import *

class Level:
    """
    Level is a class that manage the levels from the saving to the loading.

    NOTE :
            THE HEADER CONTAINS :
                -The level parallax datas;
                -The name level;
                -The size of the scene;
                -The level music;
                (-The script of the game);

            THE BODY CONTAINS :
                -All the datas to place the GameObjects of the scene;
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
        self.global_header = GlobalHeader().content

    def save_level (self, header:dict, body:list):

        self.header = header
        self.body = body

        #Thanks to json.dump, we don't have to manage the saving of files, and it will do it for us.

        try:
            with open(os.path.join(self.path,"header"), 'w', encoding='utf-8') as h_file:
                json.dump(self.header, h_file, indent=2)
            with open(os.path.join(self.path,"body"), 'w', encoding='utf-8') as b_file:
                json.dump(self.body, b_file, indent=2)

        except FileNotFoundError:
            print("ERROR : The procedure to save file failed. Please verify the integrity of the file at : "+self.path+";")

        pass

    def get_level(self):
        """
        This function load the JSON file containing the datas about the level.
        :return:
        """
        with open(os.path.join(self.path, "header"), 'r', encoding="utf-8") as h_file:
            self.header = json.load(h_file)
        with open(os.path.join(self.path, "body"), 'r', encoding="utf-8") as b_file:
            self.body = json.load(b_file)

    def load_level (self):
        """
        This method will load the level given and make a scene based on this level.
        :return:
        """
        self.get_level()

        party = Scene(self.header["scene"])

        for elem in self.body:
            prop = dict(self.global_header[elem["name"]])

            brut_path = prop["class_ref"]
            path = brut_path.split("'")[1]

            module_path, class_name = path.rsplit(".",1)

            module = importlib.import_module(module_path)
            current_class = getattr(module, class_name)

            params = prop["params"]

            new_obj = current_class(elem["pos"], elem["size"], **params)


            path_to_assets = os.getcwd()
            path_to_assets.replace(r"api\level_manager",r"game\assets")
            ress = Resource(ResourceType.GLOBAL, path_to_assets)

            if (prop["textures"] != [] and prop["textures"] != None ):
                texture = Texture(prop["textures"]["path"], ress)
                new_obj.set_texture(texture, rescale=prop["textures"]["rescale"])
            elif(prop["animation"] != []):
                texture = Texture(prop["animation"]["path"], ress)
                anim = Animation(texture,prop["animation"]["frame_count"], delay=prop["animation"]["delay"])
                new_obj.set_animation(anim)

            for tag in prop["tags"]:
                new_obj.add_tag(tag)





            party.add(new_obj,elem["layer"])
        pass