

from loguru import logger
from movenue.models.collection import Collection
from movenue.models.playable import Playable
from PIL import ImageTk, Image
from mutagen.mp4 import MP4
import io
from mutagen.id3 import ID3


def populate_playable_image(playable: Playable) -> None:

  # TODO: Add path for snapshotting a frame from video

  if playable.poster_image:
    return

  cover_path = playable.poster_location
  if not cover_path:
    return
  try:
    if str(cover_path).endswith('mp3'):
      id3 = ID3(cover_path)
      cover_data = id3.get("APIC:").data
      if cover_data:
        playable.poster_image = Image.open(io.BytesIO(cover_data))
    if str(cover_path).endswith('mp4'):
      mp4 = MP4(cover_path)
      cover_data = mp4.get('covr', [])
      if cover_data:
        if isinstance(cover_data, list):
          cover_data = cover_data[0]
        playable.poster_image = Image.open(io.BytesIO(cover_data))
      return
    if str(cover_path).endswith('.jpg'):
      playable.poster_image = Image.open(cover_path)
      return
    if str(cover_path).endswith('.png'):
      playable.poster_image = Image.open(cover_path)
      return
  except Exception as e:
    logger.warning(f'Error loading image {cover_path}: {e}')
    pass

def populate_collection_image(collection: Collection) -> None:
  cover_path = collection.poster_location
  if not cover_path:
    return
  try:
    if str(cover_path).endswith('.jpg'):
      collection.poster_image = Image.open(cover_path)
      return
    if str(cover_path).endswith('.png'):
      collection.poster_image = Image.open(cover_path)
      return
    if str(cover_path).endswith('mp4'):
      mp4 = MP4(cover_path)
      cover_data = mp4.get('covr', [])
      if cover_data:
        if isinstance(cover_data, list):
          cover_data = cover_data[0]
        collection.poster_image = Image.open(io.BytesIO(cover_data))
      return
  except Exception as e:
    logger.warning(f'Error loading image {cover_path}: {e}')