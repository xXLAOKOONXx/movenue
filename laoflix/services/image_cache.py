import io
import json
import os

from loguru import logger
import numpy as np
from laoflix.services.mp4_metadata import extract_mp4_thumbnail
from laoflix.services.settings import settings
from PIL import Image, ImageTk
import moviepy.editor as mp
from laoflix.constants import ui_sizes

CACHE_FOLDER = os.path.join(os.environ['LOCALAPPDATA'], 'laoflix', 'cache')
MUSIC_IMAGES_CACHE = os.path.join(CACHE_FOLDER, 'music_images.json')

class Cache:
  def __init__(self, youtube_folders=settings.youtube_folders, movie_folders=settings.movie_folders, series_base_folders=settings.series_base_folders, music_folders=settings.music_folders) -> None:
    self.youtube_folders = youtube_folders
    self.movie_folders = movie_folders
    self.series_base_folders = series_base_folders
    self.music_folders = music_folders
    if not os.path.exists(CACHE_FOLDER):
      os.makedirs(CACHE_FOLDER)

  @property
  def music_images(self):
    if not hasattr(self, '_music_images'):
      self._music_images = {}
      # try:
      #   with open(MUSIC_IMAGES_CACHE, 'r') as f:
      #     self._music_images = {}
      #     content_dict = json.load(f)
      #     for key, val in content_dict.items():
      #       new_image = Image.fromarray(np.array(val, dtype='uint8'))
      #       self._music_images[key] = new_image
      #   if not isinstance(self._music_images, dict):
      #     raise Exception('Not a dict')
      # except Exception as e:
      #   try:
      #     self.rebuild_music_images()
      #   except Exception as e:
      #     logger.warning(f'Failed to rebuild music images due to {str(e)}')
      #     self._music_images = self._music_images or {}
    return self._music_images
  
  def rebuild_music_images(self):
    self._music_images:dict[str, Image.Image] = {}
    for music_folder in self.music_folders:
      for root, dirs, files in os.walk(music_folder):
        for file in files:
          if file.endswith('.mp4'):
            self.refresh_music_image(os.path.join(root, file))
    # self.save_music_images()

  def save_music_images(self):
    with open(MUSIC_IMAGES_CACHE, 'w') as f:
      binary_dict = {}
      for key, img in self._music_images.items():
            
        json_data = np.array(img).tolist()

        binary_dict[key] = json_data
      json.dump(binary_dict, f)

  def refresh_music_image(self, video_path):
    try:
      binary = extract_mp4_thumbnail(video_path)
      image_data = io.BytesIO(binary[0])
      image = Image.open(image_data)
      self._music_images[video_path] = image.resize((ui_sizes.MUSIC_WIDTH, ui_sizes.MUSIC_HEIGHT))
    except Exception as e:
      logger.debug(f'Creating thumbnail for {video_path} from video')
      try:
        video = mp.VideoFileClip(video_path)
        snapshot = video.get_frame(3)  # Get the third frame of the video as a snapshot
        image = Image.fromarray(snapshot)
        self._music_images[video_path] = image.resize((ui_sizes.MUSIC_WIDTH, ui_sizes.MUSIC_HEIGHT))
      except Exception as e:
        logger.info(f'Exception for {video_path}: {str(e)}')  

  def get_music_image(self, video_path, refresh=False) -> Image.Image|None:
    if refresh:
      self.refresh_music_image(video_path)
    img = self.music_images.get(video_path, None)
    if img is None:
      self.refresh_music_image(video_path)
      img = self.music_images.get(video_path, None)
    return img
  
image_cache = Cache()