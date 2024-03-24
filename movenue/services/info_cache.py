import json
import os

from loguru import logger
from movenue.services.metadata import extract_metadata
from movenue.services.settings import settings

CACHE_FOLDER = os.path.join(os.environ['LOCALAPPDATA'], 'movenue', 'cache')
SHORTFILM_JSON_CACHE = os.path.join(CACHE_FOLDER, 'shortfilm_info.json')
MUSIC_JSON_CACHE = os.path.join(CACHE_FOLDER, 'music_info.json')
MOVIE_JSON_CACHE = os.path.join(CACHE_FOLDER, 'movie_info.json')

class Cache:
  '''
  Class to cache information about shortfilms, movies, series and music.
  usage:
    cache.get_shortfilm_info_json(info_path) -> returns the json tree of the shortfilm info file
  '''
  def __init__(self, shortfilm_folders=settings.shortfilm_folders, movie_folders=settings.movie_folders, series_base_folders=settings.series_base_folders, music_folders=settings.music_folders) -> None:
    self.shortfilm_folders = shortfilm_folders
    self.movie_folders = movie_folders
    self.series_base_folders = series_base_folders
    self.music_folders = music_folders
    if not os.path.exists(CACHE_FOLDER):
      os.makedirs(CACHE_FOLDER)
  
  @property
  def shortfilm_info_jsons(self):
    if not hasattr(self, '_shortfilm_info_jsons'):
      try:
        with open(SHORTFILM_JSON_CACHE, 'r') as f:
          self._shortfilm_info_jsons = json.load(f)
        if not isinstance(self._shortfilm_info_jsons, dict):
          raise Exception('Not a dict')
      except Exception as e:
        try:
          self.rebuild_shortfilm_info_jsons()
          with open(SHORTFILM_JSON_CACHE, 'r') as f:
            self._shortfilm_info_jsons = json.load(f)
        except Exception as e:
          self._shortfilm_info_jsons = {}
    return self._shortfilm_info_jsons
  
  def rebuild_shortfilm_info_jsons(self):
    self._shortfilm_info_jsons = {}
    for shortfilm_folder in self.shortfilm_folders:
      shortfilm_files = os.listdir(shortfilm_folder)
      shortfilm_files = [file_name for file_name in shortfilm_files if file_name.split('.')[-1] in ['json']]
      for file_name in shortfilm_files:
        try:
          with open(os.path.join(shortfilm_folder, file_name), 'r') as f:
            self._shortfilm_info_jsons[os.path.join(shortfilm_folder, file_name)] = json.load(f)
        except Exception as e:
          logger.warning(f'Failed to load {file_name} from {shortfilm_folder}')
    with open(SHORTFILM_JSON_CACHE, 'w') as f:
      json.dump(self._shortfilm_info_jsons, f)
  
  def get_shortfilm_info_json(self, info_path, refresh=False):
    if not settings.get('cache_enabled'):
      return json.load(open(info_path, 'r'))
    try:
      if refresh:
        raise Exception('Forced refresh')
      return self.shortfilm_info_jsons[info_path]
    except Exception:
      with open(info_path, 'r') as f:
        json_tree = json.load(f)
      self._shortfilm_info_jsons[info_path] = json_tree
      try:
        with open(SHORTFILM_JSON_CACHE, 'w') as f:
          json.dump(self._shortfilm_info_jsons, f)
      except Exception as e:
        logger.warning(f'Error writing shortfilm info json to cache: {e}')
      return json_tree
    
  @property
  def music_infos(self):
    if not hasattr(self, '_music_infos'):
      try:
        with open(MUSIC_JSON_CACHE, 'r') as f:
          self._music_infos = json.load(f)
        if not isinstance(self._music_infos, dict):
          raise Exception('Not a dict')
      except Exception as e:
        try:
          self.rebuild_music_info_jsons()
          with open(MUSIC_JSON_CACHE, 'r') as f:
            self._music_infos = json.load(f)
        except Exception as e:
          self._music_infos = {}
    return self._music_infos

  def rebuild_music_info_jsons(self):
    self._music_infos = {}
    for folder_path in self.music_folders:
      for root, dirs, files in os.walk(folder_path):
        for file in files:
          if file.endswith('.mp4') or file.endswith('.mp3'):
            try:
              self._music_infos[os.path.join(root, file).replace('/', '\\')] = extract_metadata(os.path.join(root, file))
            except Exception as e:
              logger.warning(f'Error extracting MP4 metadata: {e}')
    with open(MUSIC_JSON_CACHE, 'w') as f:
      json.dump(self._music_infos, f)
  
  def get_music_info_json(self, info_path, refresh=False):
    if not settings.get('cache_enabled'):
      return extract_metadata(info_path)
    try:
      if refresh:
        raise Exception('Forced refresh')
      return self.music_infos[info_path.replace('/', '\\')]
    except Exception as e:
      logger.debug(f'Error getting music info json for {info_path}: {e}')
      json_tree = extract_metadata(info_path)
      self._music_infos[info_path] = json_tree
      try:
        with open(MUSIC_JSON_CACHE, 'w') as f:
          json.dump(self._music_infos, f)
      except Exception as e:
        logger.warning(f'Error writing music info json to cache: {e}')
      return json_tree
  
info_cache = Cache()