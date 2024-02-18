import os
from laoflix.services.settings import settings
from laoflix.ui_elements.movie_card import MovieCard
from laoflix.ui_elements.series_card import SeriesCard
from laoflix.ui_elements.youtube_card import YoutubeCard

class Cache:
  def __init__(self, youtube_folders=settings.youtube_folders, movie_folders=settings.movie_folders, series_base_folders=settings.series_base_folders, music_folders=settings.music_folders) -> None:
    self.youtube_folders = youtube_folders
    self.movie_folders = movie_folders
    self.series_base_folders = series_base_folders
    self.music_folders = music_folders
  
  def youtubes(self, popup_master):
    if not hasattr(self, '_youtubes'):
      self._youtubes:list[YoutubeCard] = []
      for youtube_folder in self.youtube_folders:
          youtube_files = os.listdir(youtube_folder)
          youtube_files = [file_name for file_name in youtube_files if file_name.split('.')[-1] in ['json']]
          self._youtubes = self._youtubes + [YoutubeCard(youtube_folder, '.'.join(file_name.split('.')[0:-2]), popup_master=popup_master) for file_name in youtube_files]
    return self._youtubes
     
  
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