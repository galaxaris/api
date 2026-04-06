

import os

from api.utils.Console import print_warning

def treat_path(name:str)->tuple[str, bool]:
    """
    This function returns a path pointing to the levels directory.

    :param name: A str that is the name of the file you are looking for
    :return: A str that represents the path to the level directory.
    """

    path = os.getcwd()
    path.replace("api\SceneManager", "game\levels")
    try:
        os.mkdir(os.path.join(path, name))
        new = True
    except OSError:
        print_warning("This file already exists")
        new= False
    return os.path.join(path,name), new