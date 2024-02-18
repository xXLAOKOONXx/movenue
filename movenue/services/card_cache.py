import os
from movenue.services.settings import settings
from movenue.ui_elements.movie_card import MovieCard
from movenue.ui_elements.series_card import SeriesCard
from movenue.ui_elements.shortfilm.shortfilm_card import ShortfilmCard

class Cache:
  def __init__(self, shortfilm_folders=settings.shortfilm_folders, movie_folders=settings.movie_folders, series_base_folders=settings.series_base_folders, music_folders=settings.music_folders) -> None:
    self.shortfilm_folders = shortfilm_folders
    self.movie_folders = movie_folders
    self.series_base_folders = series_base_folders
    self.music_folders = music_folders
  
  def shortfilms(self, popup_master):
    if not hasattr(self, '_shortfilms'):
      self._shortfilms:list[ShortfilmCard] = []
      for shortfilm_folder in self.shortfilm_folders:
          shortfilm_files = os.listdir(shortfilm_folder)
          shortfilm_files = [file_name for file_name in shortfilm_files if file_name.split('.')[-1] in ['json']]
          self._shortfilms = self._shortfilms + [ShortfilmCard(shortfilm_folder, '.'.join(file_name.split('.')[0:-2]), popup_master=popup_master) for file_name in shortfilm_files]
    return self._shortfilms
     
  
  def movies(self, popup_master):
    if not hasattr(self, '_movies'):
      self._movies = []
      for movie_folder in self.movie_folders:
          available_movie_types = ['nfo']
          movie_files = os.listdir(movie_folder)
          movie_files = [file_name for file_name in movie_files if file_name.split('.')[-1] in available_movie_types]
          self._movies = self._movies + [MovieCard(movie_folder, '.'.join(file_name.split('.')[0:-1]), popup_master=popup_master) for file_name in movie_files]
    return self._movies
  
  def series(self, popup_master):
    if not hasattr(self, '_series'):
      self._series = []
      for series_base_folder in self.series_base_folders:
        series_folders = os.listdir(series_base_folder)
        self._series = self._series + [SeriesCard(series_base_folder, series_folder_name, popup_frame=popup_master) for series_folder_name in series_folders]
    return self._series
  
card_cache = Cache()