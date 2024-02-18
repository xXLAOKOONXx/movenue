import json
import os

from loguru import logger
from laoflix.services.mp4_metadata import extract_mp4_metadata
from laoflix.services.settings import settings

CACHE_FOLDER = os.path.join(os.environ['LOCALAPPDATA'], 'laoflix', 'cache')
YOUTUBE_JSON_CACHE = os.path.join(CACHE_FOLDER, 'youtube_info.json')
MUSIC_JSON_CACHE = os.path.join(CACHE_FOLDER, 'music_info.json')

class Cache:
  def __init__(self, youtube_folders=settings.youtube_folders, movie_folders=settings.movie_folders, series_base_folders=settings.series_base_folders, music_folders=settings.music_folders) -> None:
    self.youtube_folders = youtube_folders
    self.movie_folders = movie_folders
    self.series_base_folders = series_base_folders
    self.music_folders = music_folders
    if not os.path.exists(CACHE_FOLDER):
      os.makedirs(CACHE_FOLDER)
  
  @property
  def youtube_info_jsons(self):
    if not hasattr(self, '_youtube_info_jsons'):
      try:
        with open(YOUTUBE_JSON_CACHE, 'r') as f:
          self._youtube_info_jsons = json.load(f)
        if not isinstance(self._youtube_info_jsons, dict):
          raise Exception('Not a dict')
      except Exception as e:
        try:
          self.rebuild_youtube_info_jsons()
          with open(YOUTUBE_JSON_CACHE, 'r') as f:
            self._youtube_info_jsons = json.load(f)
        except Exception as e:
          self._youtube_info_jsons = {}
    return self._youtube_info_jsons
  
  def rebuild_youtube_info_jsons(self):
    self._youtube_info_jsons = {}
    for youtube_folder in self.youtube_folders:
      youtube_files = os.listdir(youtube_folder)
      youtube_files = [file_name for file_name in youtube_files if file_name.split('.')[-1] in ['json']]
      for file_name in youtube_files:
        try:
          with open(os.path.join(youtube_folder, file_name), 'r') as f:
            self._youtube_info_jsons[os.path.join(youtube_folder, file_name)] = json.load(f)
        except Exception as e:
          logger.warning(f'Failed to load {file_name} from {youtube_folder}')
    with open(YOUTUBE_JSON_CACHE, 'w') as f:
      json.dump(self._youtube_info_jsons, f)
  
  def get_youtube_info_json(self, info_path, refresh=False):
    try:
      if refresh:
        raise Exception('Forced refresh')
      return self.youtube_info_jsons[info_path]
    except Exception:
      with open(info_path, 'r') as f:
        json_tree = json.load(f)
      self._youtube_info_jsons[info_path] = json_tree
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
          if file.endswith('.mp4'):
            try:
              self._music_infos[os.path.join(root, file).replace('/', '\\')] = extract_mp4_metadata(os.path.join(root, file))
            except Exception as e:
              logger.warning(f'Error extracting MP4 metadata: {e}')
    with open(MUSIC_JSON_CACHE, 'w') as f:
      json.dump(self._music_infos, f)
  
  def get_music_info_json(self, info_path, refresh=False):
    try:
      if refresh:
        raise Exception('Forced refresh')
      return self.music_infos[info_path.replace('/', '\\')]
    except Exception as e:
      logger.debug(f'Error getting music info json for {info_path}: {e}')
      json_tree = extract_mp4_metadata(info_path)
      self._music_infos[info_path] = json_tree
      return json_tree
  
info_cache = Cache()