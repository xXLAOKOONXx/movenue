from datetime import date
import os

from loguru import logger
from movenue.models.collection import Collection
from movenue.models.playable import Playable
import xml.etree.ElementTree as ET
from movenue.constants import nfo_fields, mp4_fields, id3_fields
from mutagen.mp4 import MP4
from movenue.models.storage import FolderStorage, Storage
from mutagen.id3 import ID3, TextFrame


def save_playable_to_file(playable: Playable, filestore:FolderStorage|None=None) -> None:
  nfo_path = f'''{'.'.join(str(playable.file_path).split('.')[0:-1])}.nfo'''
  if os.path.exists(nfo_path):
    try:
      save_playable_to_nfo(playable, nfo_path)
      if filestore:
        Storage.refresh_folder_store(filestore)
      return
    except Exception as e:
      logger.error(f"Error saving infos to {nfo_path}: {e}")
  if str(playable.file_path).endswith('.mp4'):
    try:
      save_playable_to_mp4(playable)
      if filestore:
        Storage.refresh_folder_store(filestore)
      return
    except Exception as e:
      logger.error(f"Error saving infos to {playable.file_path}: {e}")
  if str(playable.file_path).endswith('.mp3'):
    try:
      save_playable_to_id3(playable)
      if filestore:
        Storage.refresh_folder_store(filestore)
      return
    except Exception as e:
      logger.error(f"Error saving infos to {playable.file_path}: {e}")

def save_playable_to_id3(playable: Playable) -> None:
  try:
    id3 = ID3(playable.file_path)

    tf = TextFrame(text=playable.tags)
    id3.setall(id3_fields.TAGS, [tf])

    if playable.lastplayed is not None:
      tf = TextFrame(text=str(playable.lastplayed))
      id3.setall(id3_fields.LASTPLAYED, tf)

    if playable.user_rating is not None:
      tf = TextFrame(text=str(playable.user_rating))
      id3.setall(id3_fields.USERRATING, tf)
    
    if playable.playcount is not None:
      tf = TextFrame(text=str(playable.playcount))
      id3.setall(id3_fields.PLAYCOUNT, tf)

    if playable.start_time_ms is not None:
      tf = TextFrame(text=str(playable.start_time_ms))
      id3.setall(id3_fields.START_TIME_IN_MS, tf)

    if playable.end_time_ms is not None:
      tf = TextFrame(text=str(playable.end_time_ms))
      id3.setall(id3_fields.END_TIME_IN_MS, tf)

    id3.save()
  except Exception as e:
    raise logger.error(f"Error writing ID3 tags to {playable.file_path}: {e}")
  

def save_playable_to_nfo(playable: Playable, nfo_path) -> None:
  try:
      xml_tree = ET.parse(nfo_path)
  except Exception as e:
      raise e
  
  xml_root = xml_tree.getroot()

  if playable.lastplayed is not None:
    last_played = xml_root.find(nfo_fields.LASTPLAYED)
    if last_played is None:
        last_played = ET.SubElement(xml_root, nfo_fields.LASTPLAYED)
    last_played.text = str(playable.lastplayed)

  if playable.user_rating is not None:
    userscore = xml_root.find(nfo_fields.USERRATING)
    if userscore is None:
        userscore = ET.SubElement(xml_root, nfo_fields.USERRATING)
    userscore.text = str(playable.user_rating)

  if playable.playcount is not None:
    playcount = xml_root.find(nfo_fields.PLAYCOUNT)
    if playcount is None:
        playcount = ET.SubElement(xml_root, nfo_fields.PLAYCOUNT)
    playcount.text = str(playable.playcount)

  if playable.start_time_ms is not None:
    start_time_ms = xml_root.find(nfo_fields.START_TIME_IN_MS)
    if start_time_ms is None:
        start_time_ms = ET.SubElement(xml_root, nfo_fields.START_TIME_IN_MS)
    start_time_ms.text = str(playable.start_time_ms)

  if playable.end_time_ms is not None:
    end_time_ms = xml_root.find(nfo_fields.END_TIME_IN_MS)
    if end_time_ms is None:
        end_time_ms = ET.SubElement(xml_root, nfo_fields.END_TIME_IN_MS)
    end_time_ms.text = str(playable.end_time_ms)

  genres = xml_root.findall(nfo_fields.TAG)
  if not genres:
    genres = xml_root.findall(nfo_fields.TAG.lower())
  if genres:
    for genre in genres:
      if genre.text not in playable.tags:
        xml_root.remove(genre)
  if playable.tags:
    for tag in playable.tags:
      if not genres or tag not in [el.text for el in genres]:
        genre = ET.SubElement(xml_root, nfo_fields.TAG)
        genre.text = tag

  xml_tree.write(nfo_path)

def save_playable_to_mp4(playable: Playable) -> None:
  mp4 = MP4(playable.file_path)

  if playable.lastplayed is not None:
    mp4[mp4_fields.LASTPLAYED] = bytes(str(playable.lastplayed), 'utf-8')
  if playable.user_rating is not None:
    mp4[mp4_fields.USERRATING] = bytes(str(playable.user_rating), 'utf-8')
  if playable.playcount is not None:
    mp4[mp4_fields.PLAYCOUNT] = bytes(str(playable.playcount), 'utf-8')
  if playable.start_time_ms is not None:
    mp4[mp4_fields.START_TIME_IN_MS] = bytes(str(playable.start_time_ms), 'utf-8')
  if playable.end_time_ms is not None:
    mp4[mp4_fields.END_TIME_IN_MS] = bytes(str(playable.end_time_ms), 'utf-8')
  if playable.tags:
    tags = list(set(playable.tags))
    mp4['tags'] = tags

  try:
    mp4.save()
  except Exception as e:
    raise Exception(f'Error saving MP4 metadata: {e}')
  
def save_collection_to_file(collection: Collection) -> None:
  nfo_path = os.path.join(collection.full_path, f'tvshow.nfo')
  if os.path.exists(nfo_path):
    try:
      save_collection_to_nfo(collection, nfo_path)
    except Exception as e:
      logger.error(f"Error saving {nfo_path}: {e}")


def save_collection_to_nfo(collection: Collection, nfo_path) -> None:
  
    try:
        xml_tree = ET.parse(nfo_path)
    except Exception as e:
        logger.error(f'Error interpreting {nfo_path}')
        raise e
    xml_root = xml_tree.getroot()

    if collection.lastplayed is not None:
      last_played = xml_root.find('lastplayed')
      if last_played is None:
          last_played = ET.SubElement(xml_root, 'lastplayed')
      last_played.text = str(collection.lastplayed)

    xml_tree.write(nfo_path)