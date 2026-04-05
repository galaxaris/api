"""
DataManager module for handling game data saving and loading, used in the Editor and potentially in the game itself for saving progress, settings, etc.
"""

import time
import json
import os

from api.utils.Console import print_error, print_info, print_warning

ACTUAL_TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
DEFAULT_SAVE_NAME = "save.json"
SAVE_DIR = "saves/"

DEFAULT_STRUCTURE = {

}

DATA = DEFAULT_STRUCTURE.copy()

def get(key, default=None):
    global DATA
    return DATA.get(key, default)

def set_value(key, value):
    global DATA
    DATA[key] = value

def set_default_structure(structure: dict):
    global DEFAULT_STRUCTURE
    DEFAULT_STRUCTURE = structure

def set_save_dir(directory: str):
    global SAVE_DIR
    SAVE_DIR = directory

def save_data(name: str = DEFAULT_SAVE_NAME):
    global DATA
    with open(SAVE_DIR + name, "w") as f:
        json.dump(DATA, f)

def get_saves():
    try:
        return [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    except FileNotFoundError:
        print_error(f"Save directory '{SAVE_DIR}' not found. Returning empty list.")
        return []
    except Exception as e:
        print_error(f"Error accessing save directory '{SAVE_DIR}': {e}. Returning empty list.")
        return []

def load_data(name: str = DEFAULT_SAVE_NAME):
    global DATA
    try:
        with open(SAVE_DIR + name, "r") as f:
            DATA = json.load(f)
    except FileNotFoundError:
        print_error(f"Save file '{name}' not found. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()
    except json.JSONDecodeError:
        print_error(f"Error decoding JSON from '{name}'. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()
    except Exception as e:
        print_error(f"Error loading data from '{name}': {e}. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()

def delete_data(name: str = DEFAULT_SAVE_NAME):
    try:
        os.remove(SAVE_DIR + name)
        print_info(f"Save file '{name}' deleted successfully.")
    except FileNotFoundError:
        print_error(f"Save file '{name}' not found. Nothing to delete.")
    except Exception as e:
        print_error(f"Error deleting save file '{name}': {e}.")


#%############### Not using the data manager #################
##### Functions loading files directly (useful for the game setup, e.g.)

def load_json(path: str) -> dict:
    """
    Loads a JSON file and returns its content as a dictionary.
    
    :param path: JSON path
    :return: JSON Dict, empty if error
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"File '{path}' not found. Returning empty dictionary.")
        return {}
    except json.JSONDecodeError:
        print_error(f"Error decoding JSON from '{path}'. Returning empty dictionary.")
        return {}
    except Exception as e:
        print_error(f"Error loading JSON from '{path}': {e}. Returning empty dictionary.")
        return {}