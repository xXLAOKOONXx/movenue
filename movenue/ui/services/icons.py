import os
import sys
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Icons:
    def __init__(self):
        pass

    def eye_icon(self, size:int=50):
        if not hasattr(self, '_eye_icons'):
            self._eye_icons = {}
        if size not in self._eye_icons.keys():
            try:
                self._eye_icons[size] = ImageTk.PhotoImage(Image.open(resource_path('movenue/assets/icons8-sichtbar-50.png')).resize((size, size)))
            except:
                self._eye_icons[size] = ImageTk.PhotoImage(Image.open(resource_path('assets/icons8-sichtbar-50.png')).resize((size, size)))
        return self._eye_icons[size]
    
def get_app_icon_path():
    try:
        return resource_path('movenue/assets/polygon.ico')
    except:
        return resource_path('assets/polygon.ico')
    
icons = Icons()