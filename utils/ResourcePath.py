import sys
import os

def resource_path(relative_path):
    try:
        #pyinstaller create a temporary folder for assets
        base_path = sys._MEIPASS
    except Exception:
        #we are not in an exe made with pyinstaller
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)