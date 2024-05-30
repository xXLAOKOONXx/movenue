from datetime import date
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from loguru import logger
from PIL import Image

from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.services.playables_population import add_playable_info
from movenue.constants import general_settings


def add_collection_info(collection: Collection, draw_collectbles:bool=True) -> None:
    """
    Adds all available information to the collection.
    Might be used to refresh the information of a collection.
    Prefers nfo files over mp4 tags.
    """
    nfo_path = os.path.join(collection.full_path, 'tvshow.nfo')
    if os.path.exists(nfo_path):
        add_nfo_collection_info(collection, nfo_path, draw_collectbles=draw_collectbles)
    else:
        add_just_folders_collection_info(collection)

def add_nfo_collection_info(collection:Collection, nfo_path: str | Path, draw_collectbles:bool=True) -> None:
    """
    Populate the series collection with the series in the folder path.
    """
    try:
      xml_tree = ET.parse(nfo_path)
    except Exception as e:
      logger.error(f"Error parsing {nfo_path}: {e}")
      raise e
    xml_root = xml_tree.getroot()
    genres = [el.text for el in xml_root if el.tag == 'genre']
    titles = [el.text for el in xml_root if el.tag in ['title', 'originaltitle', 'sorttitle']]
    playcount = int(xml_root.find('playcount').text) if xml_root.find('playcount') else 0
    last_played_text = xml_root.find('lastplayed').text if xml_root.find('lastplayed') is not None else None
    try:
        y, m, d = last_played_text.split('-')
        lastplayed = date(int(y),int(m),int(d))
    except Exception as ex:
        lastplayed = None
    try:
        userscore = float(xml_root.find('userscore').text)
    except:
        userscore = None
    try:
        ratings = [float(el.find('value'))/el.get('max') for el in xml_root.find('ratings') if el.tag == 'rating']
        public_rating = sum(ratings) / len(ratings)
    except:
        public_rating = None
    actor_names = [el.find('name').text for el in xml_root if el.tag == 'actor']

    poster_url = os.path.join(collection.full_path, 'poster.jpg')
    if not os.path.exists(poster_url):
        poster_url = None

    def get_seasons() -> list[int]:
      seasons = []
      subdirs = [name for name in os.listdir(collection.full_path)
          if os.path.isdir(os.path.join(collection.full_path, name))]
      for subdir in subdirs:
          if subdir != '.actors':
              no = int(subdir.strip('S'))
              seasons.append(no)
      return seasons
    
    
    def get_season_poster_path(no: int):
        if no > 100:
            path = os.path.join(collection.full_path, f'season{int(no/100):02}-poster.jpg')
            if os.path.exists(path):
                return path
        return os.path.join(collection.full_path, f'season{no:02}-poster.jpg')
    
    collection.title=titles[0]
    collection.alt_titles=titles[1:]
    collection.lastplayed=lastplayed
    collection.playcount=playcount
    collection.user_rating=userscore
    collection.public_rating=public_rating
    collection.tags=genres
    collection.artists=actor_names
    collection.poster_location=poster_url


    seasons = []

    if draw_collectbles:
        collectable_last_played = None
        for season_no in get_seasons():
            season_img = None
            season_poster_path = get_season_poster_path(season_no)
            if os.path.exists(season_poster_path):
                season_img = Image.open(season_poster_path)
            season_full_path = os.path.join(collection.full_path, f'S{season_no:02}')
            episode_paths = [os.path.join(collection.full_path, f'S{season_no:02}', name) for name in os.listdir(season_full_path) if name.endswith('.mp4')]
            episodes = []
            for episode_path in episode_paths:
                playable = Playable(file_path=episode_path)
                add_playable_info(playable)
                episodes.append(playable)
            
            season = Collection(
                full_path=season_full_path,
                title=f"Season {season_no}",
                collectables=episodes,
                poster_image=season_img,
            )

            seasons.append(season)


    collection.collectables=seasons

    return collection

def add_just_folders_collection_info(collection: Collection, draw_collectbles:bool=True) -> None:
    """
    Adds all available information to the collection.
    Assumes no meta infos are present.
    """
    collection.title = os.path.basename(collection.full_path)
    if not draw_collectbles:
        return
    playables = []
    for dir_name in os.listdir(collection.full_path):
        if os.path.isdir(os.path.join(collection.full_path, dir_name)):
            try:
                sub_collection = Collection(os.path.join(collection.full_path, dir_name))
                add_just_folders_collection_info(sub_collection)
                if sub_collection.collectables:
                    collection.collectables.append(sub_collection)
            except Exception as e:
                logger.error(f"Error adding subcollection {dir_name}: {e}")
                pass
        if dir_name.endswith(tuple(general_settings.SUPPORTED_FILE_ENDINGS)):
            try:
                playable = Playable(os.path.join(collection.full_path, dir_name))
                add_playable_info(playable)
                playables.append(playable)
            except Exception as e:
                logger.error(f"Error adding playable {dir_name}: {e}")
                pass
    if collection.collectables:
        folder_collection = Collection(full_path=collection.full_path, title=general_settings.OTHER_COLLECTION_CATEGORY, collectables=playables)
        collection.collectables.append(folder_collection)
    else:
        collection.collectables = playables