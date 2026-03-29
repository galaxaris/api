import time
import json
import os

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
        print(f"Save directory '{SAVE_DIR}' not found. Returning empty list.")
        return []
    except Exception as e:
        print(f"Error accessing save directory '{SAVE_DIR}': {e}. Returning empty list.")
        return []

def load_data(name: str = DEFAULT_SAVE_NAME):
    global DATA
    try:
        with open(SAVE_DIR + name, "r") as f:
            DATA = json.load(f)
    except FileNotFoundError:
        print(f"Save file '{name}' not found. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{name}'. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()
    except Exception as e:
        print(f"Error loading data from '{name}': {e}. Returning default structure.")
        return DEFAULT_STRUCTURE.copy()

def delete_data(name: str = DEFAULT_SAVE_NAME):
    try:
        os.remove(SAVE_DIR + name)
        print(f"Save file '{name}' deleted successfully.")
    except FileNotFoundError:
        print(f"Save file '{name}' not found. Nothing to delete.")
    except Exception as e:
        print(f"Error deleting save file '{name}': {e}.")

