import json
import os

SETTINGS_FILE = os.path.join(os.environ['LOCALAPPDATA'], 'movenue', 'settings.json')


class Settings:
    '''
    Class to manage the settings for the application.
    '''
    def __init__(self, file_path=SETTINGS_FILE):
        self.file_path = file_path
        self.settings = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.settings = json.load(f)

    def get(self, key):
        '''
        Gets a setting.

        Args:
          key (str): The setting key.

        Returns:
          str: The setting value.
        '''
        return self.settings.get(key, None)

    def set(self, key, value):
        '''
        Sets a setting.

        Args:
          key (str): The setting key.
          value (str): The setting value.
        '''
        self.settings[key] = value
        with open(SETTINGS_FILE, '+w') as f:
            json.dump(self.settings, f, indent=2)

    @property
    def movie_folders(self) -> list[str]:
        '''
        Gets the movie folders.

        Returns:
          list: The movie folders.
        '''
        if not self.get('movie_folders'):
            self.set('movie_folders', [])
        return self.get('movie_folders')
    
    def add_movie_folder(self, folder): 
        '''
        Adds a movie folder.

        Args:
          folder (str): The folder to be added.
        '''
        movie_folders = self.movie_folders
        movie_folders.append(folder)
        self.set('movie_folders', movie_folders)
    
    @property
    def shortfilm_folders(self) -> list[str]:
        '''
        Gets the Shortfilm folders.

        Returns:
          list: The Shortfilm folders.
        '''
        if not self.get('shortfilm_folders'):
            self.set('shortfilm_folders', [])
        return self.get('shortfilm_folders')
    
    def add_shortfilm_folder(self, folder):
        '''
        Adds a Shortfilm folder.

        Args:
          folder (str): The folder to be added.
        '''
        shortfilm_folders = self.shortfilm_folders
        shortfilm_folders.append(folder)
        self.set('shortfilm_folders', shortfilm_folders)
    
    @property
    def series_base_folders(self) -> list[str]:
        '''
        Gets the series base folder.

        Returns:
          str: The series base folder.
        '''
        if not self.get('series_base_folder'):
            self.set('series_base_folder', [])
        return self.get('series_base_folder')
    
    def add_series_base_folder(self, folder):
        '''
        Adds a series base folder.

        Args:
          folder (str): The folder to be added.
        '''
        series_base_folders = self.series_base_folders
        series_base_folders.append(folder)
        self.set('series_base_folder', series_base_folders)

    @property
    def music_folders(self) -> list[str]:
        '''
        Gets the music folders.

        Returns:
          list: The music folders.
        '''
        if not self.get('music_folders'):
            self.set('music_folders', [])
        return self.get('music_folders')
    
    def add_music_folder(self, folder):
        '''
        Adds a music folder.

        Args:
          folder (str): The folder to be added.
        '''
        music_folders = self.music_folders
        music_folders.append(folder)
        self.set('music_folders', music_folders)
    
settings = Settings()