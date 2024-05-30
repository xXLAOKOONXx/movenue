import json
import os
from loguru import logger

from movenue.models.settings import CategorySettings, FolderSetting
from movenue.ui.constants import ui_colors
from movenue.ui.main_window import MainWindow


if __name__ == '__main__':
    
    # create folder if not present
    local_app_data_folder = os.path.join(os.environ['LOCALAPPDATA'], 'movenue')
    if not os.path.exists(local_app_data_folder):
        os.makedirs(local_app_data_folder)
    logging_path = os.path.join(local_app_data_folder, 'logs')
    if not os.path.exists(logging_path):
        os.makedirs(logging_path)
    # setup logging
    logger.add(os.path.join(logging_path, 'movenue.log'), format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=False)

    settings_path = os.path.join(local_app_data_folder, 'category_settings.json')
    if not os.path.exists(settings_path): 
        cat_settings:list[CategorySettings] = []

        films_settings = CategorySettings('Filme', [FolderSetting('//mynas/Daten/Videos/Filme', 'playables', False)], 'category_page')
        search_settings = CategorySettings('Suche', [FolderSetting('//mynas/Daten/Videos/Filme', 'playables', False)], 'search_page')
        series_settings = CategorySettings('Serien', [FolderSetting('//mynas/Daten/Videos/Serien', 'collections', False)], 'category_page')
        music_settings = CategorySettings('Musik', [FolderSetting('//mynas/Daten/Musik/Videos', 'playables', True)], 'filter_page')

        cat_settings.append(films_settings)
        cat_settings.append(search_settings)
        cat_settings.append(series_settings)
        cat_settings.append(music_settings)

        with open(settings_path, 'w') as f:
            json.dump([cat.__to_json__() for cat in cat_settings], f)
    
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            cat_settings = [CategorySettings.from_json(item) for item in json.load(f)]

    mw = MainWindow(cat_settings=cat_settings)
    mw.start()
