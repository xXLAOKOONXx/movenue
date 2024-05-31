


from datetime import date
import json
import math
from pathlib import Path
from movenue.models.playable import Playable
import xml.etree.ElementTree as ET
from loguru import logger
from PIL import Image, ImageTk
from mutagen.mp4 import MP4
from movenue.constants import nfo_fields, mp4_fields, id3_fields
from mutagen.id3 import ID3, TextFrame


def populate_playable(file_path: str | Path) -> Playable:
  playable = Playable(file_path)
  add_playable_info(playable)
  return playable

def add_playable_info(playable: Playable) -> None:
  """
  Adds all available information to the playable.
  Might be used to refresh the information of a playable.
  Prefers nfo files over mp4 tags.
  """
  nfo_path = f'''{'.'.join(str(playable.file_path).split('.')[0:-1])}.nfo'''
  info_json_path = f'''{'.'.join(str(playable.file_path).split('.')[0:-1])}.info.json'''
  if Path(nfo_path).exists():
    add_nfo_playable_info(playable, nfo_path)
  elif Path(info_json_path).exists():
    add_info_json_playable_info(playable, info_json_path)
  elif str(playable.file_path).endswith('.mp4'):
    add_mp4_playable_info(playable)
  elif str(playable.file_path).endswith('.mp3'):
    add_id3_playable_info(playable)

def add_info_json_playable_info(playable: Playable, info_json_path: str | Path) -> None:
  with open(info_json_path, 'r') as f:
    info = json.load(f)
  playable.title = info.get('title', None)
  playable.index_number = info.get('index_number', None)
  playable.alt_titles = info.get('alt_titles', [])
  playable.lastplayed = date.fromisoformat(info.get('lastplayed', None)) if info.get('lastplayed', None) else None
  playable.user_rating = info.get('user_rating', None)
  playable.public_rating = info.get('public_rating', None)

  poster_path = f'''{'.'.join(str(playable.file_path).split('.')[0:-1])}.jpg'''
  if Path(poster_path).exists():
    playable.poster_location = poster_path
  playable.playcount = int(info.get('playcount', 0))
  playable.tags = info.get('tags', [])
  playable.artists = info.get('artists', [])
  playable.duration = info.get('duration', None)

def add_nfo_playable_info(playable: Playable, nfo_path: str | Path) -> None:
  try:
      xml_tree = ET.parse(nfo_path)
  except Exception as e:
      logger.error(f"Error parsing {nfo_path}: {e}")
      raise e
  xml_root = xml_tree.getroot()
  try:
    playable.title = xml_root.find('title').text
  except:
    pass
  try:
    playable.index_number = int(xml_root.find('episode').text)
  except:
    pass
  try:
    playable.alt_titles = [el.text for el in xml_root if el.tag in ['originaltitle', 'sorttitle']]
  except:
    pass
  try:
    y, m, d = xml_root.find('lastplayed').text.split('-')
    playable.lastplayed = date(int(y),int(m),int(d))
  except:
    pass
  try:
    playable.user_rating = float(xml_root.find('userscore').text)
  except:
    pass
  try:
    ratings = [float(el.find('value').text)/el.get('max') for el in xml_root.find('ratings') if el.tag == 'rating']
    playable.public_rating = sum(ratings) / len(ratings)
  except:
    pass

  poster_url = f'''{'.'.join(nfo_path.split('.')[0:-1])}-poster.jpg'''
  thumb_url = f'''{'.'.join(nfo_path.split('.')[0:-1])}-thumb.jpg'''
  if Path(poster_url).exists():
    playable.poster_location = poster_url
  elif Path(thumb_url).exists():
    playable.poster_location = thumb_url

  try:
    playable.playcount = int(xml_root.find('playcount').text) if xml_root.find('playcount') is not None else 0
  except:
    pass

  try:
    genres = [el.text for el in xml_root if el.tag == 'genre']
    playable.tags = genres
  except:
    pass
  try:
    actor_names = [el.find('name').text for el in xml_root if el.tag == 'actor']
    playable.artists = actor_names
  except:
    pass

def add_mp4_playable_info(playable: Playable) -> None:
  mp4 = MP4(playable.file_path)
  if userrating := mp4.get(mp4_fields.USERRATING, [None])[0]:
    userrating = int(userrating.decode('utf-8'))
  else:
    userrating = None
  playable.user_rating = userrating
  if music_start := mp4.get(mp4_fields.START_TIME_IN_MS, [None])[0]:
    music_start = int(music_start.decode('utf-8'))
  else:
    music_start = None
  playable.start_time_ms = music_start
  if music_end := mp4.get(mp4_fields.END_TIME_IN_MS, [None])[0]:
    music_end = int(music_end.decode('utf-8'))
  else:
    music_end = None
  playable.end_time_ms = music_end

  playable.title = mp4.get(mp4_fields.TITLE, [''])[0]
  playable.artists = mp4.get(mp4_fields.ARTISTS, [])
  playable.play_duration_ms = mp4.info.length * 1000
  playable.tags = mp4.get(mp4_fields.TAGS, [])

  if mp4.get(mp4_fields.COVER_IMAGE, []):
    playable.poster_location = playable.file_path

def add_id3_playable_info(playable: Playable) -> None:
    id3 = ID3(playable.file_path)
    if tags := id3.get(id3_fields.TAGS):
      playable.tags = tags.text.split(',')

    if music_start := id3.get(id3_fields.START_TIME_IN_MS):
      playable.start_time_ms = int(music_start.text[0])

    if music_end := id3.get(id3_fields.END_TIME_IN_MS):
      playable.end_time_ms = int(music_end.text[0])

    if title := id3.get('TIT2'):
      playable.title = title.text[0]

    if artists := id3.get('TPE1'):
      playable.artists = artists.text

    if wmp_rating := id3.get('POPM:Windows Media Player 9 Series'):
      wmp_rating = int(wmp_rating.rating)
      # POPM:Windows Media Player 9 Series decodes in 2^STAR
      playable.user_rating = (int(math.log2(wmp_rating)) - 4) * 2

    if user_rating := id3.get(id3_fields.USERRATING):
      playable.user_rating = int(user_rating.text[0])

    if "APIC:" in id3:
      playable.poster_location = playable.file_path
