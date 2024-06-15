from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Self, Tuple

from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.settings import SEARCH_TYPES, CategorySettings
from movenue.constants import general_settings
from movenue.services.playables_population import add_playable_info
from movenue.services.collections_population import add_collection_info

CACHE_FOLDER = os.path.join(os.environ['LOCALAPPDATA'], 'movenue', 'cache')

def get_folder_storage_key(path, search_type, include_subfolders_for_playables) -> Tuple[str, str, bool]:
  return f"{str(path).replace('/','-').replace('\\','-')}_{search_type}_{include_subfolders_for_playables}"

@dataclass
class FolderStorage:
  folder_path : str | Path
  search_type: SEARCH_TYPES
  playables : list[Playable] = field(default_factory=list)
  collections : list[Collection] = field(default_factory=list)
  include_subfolders: bool = True

  def __to_json__(self):
    return {
      'folder_path': self.folder_path,
      'search_type': self.search_type,
      'playables': [playable.__to_json__() for playable in self.playables],
      'collections': [collection.__to_json__() for collection in self.collections],
      'include_subfolders': self.include_subfolders
    }
  
  @staticmethod
  def from_json(json_data: dict) -> Self:
    return FolderStorage(
      folder_path=json_data['folder_path'],
      search_type=json_data['search_type'],
      playables=[Playable.from_json(playable) for playable in json_data['playables']],
      collections=[Collection.from_json(collection) for collection in json_data['collections']],
      include_subfolders=json_data['include_subfolders']
    )


class Storage:
  categories : dict[str, list[FolderStorage]]
  _all_storages: dict[Tuple[str, str, bool], FolderStorage] = {}
  def __init__(self, category_settings: list[CategorySettings]):
    self._all_storages = {}
    self.categories = {}
    for category_setting in category_settings:
      self.categories[category_setting.name] = []
      for folder in category_setting.folders:
        if not self._all_storages.get((folder.path, folder.search_type, folder.include_subfolders_for_playables)):
          if os.path.exists(os.path.join(CACHE_FOLDER, get_folder_storage_key(folder.path, folder.search_type, folder.include_subfolders_for_playables))):
            try:
              with open(os.path.join(CACHE_FOLDER, get_folder_storage_key(folder.path, folder.search_type, folder.include_subfolders_for_playables)), 'r') as file:
                self._all_storages[(folder.path, folder.search_type, folder.include_subfolders_for_playables)] = FolderStorage.from_json(json.load(file))
            except:
              self._all_storages[(folder.path, folder.search_type, folder.include_subfolders_for_playables)] = FolderStorage(folder.path, folder.search_type, [], [], folder.include_subfolders_for_playables)
          else:
            self._all_storages[(folder.path, folder.search_type, folder.include_subfolders_for_playables)] = FolderStorage(folder.path, folder.search_type, [], [], folder.include_subfolders_for_playables)
        self.categories[category_setting.name].append(self._all_storages.get((folder.path, folder.search_type, folder.include_subfolders_for_playables)))

  def get_playables(self, category: str) -> list[Playable]:
    playables = []
    for folder_storage in self.categories[category]:
      if (folder_storage.search_type == 'playables' and not folder_storage.playables):
        Storage.refresh_folder_store(folder_storage)
      playables += folder_storage.playables
    return playables
  
  def get_collections(self, category: str) -> list[Collection]:
    collections = []
    for folder_storage in self.categories[category]:
      if (folder_storage.search_type == 'collections' and not folder_storage.collections):
        Storage.refresh_folder_store(folder_storage)
      collections += folder_storage.collections
    return collections
  
  def refresh_category(self, category: str):
    for folder_storage in self.categories[category]:
      Storage.refresh_folder_store(folder_storage)

  def save(self):
    for folder_storage in self._all_storages.values():
      Storage.save_folder_storage(folder_storage)

  def recache(self, item: Playable|Collection):
    def playable_in_collection(playable: Playable, collection: Collection):
      if not collection.collectables:
        return False
      if isinstance(collection.collectables[0], Playable):
        if playable in collection.collectables:
          return True
      if isinstance(collection.collectables[0], Collection):
        for sub_collection in collection.collectables:
          if playable_in_collection(playable, sub_collection):
            return True
      return False
    
    def collection_in_collection(collection: Collection, parent_collection: Collection):
      if not parent_collection.collectables:
        return False
      if collection in parent_collection.collectables:
        return True
      if isinstance(parent_collection.collectables[0], Collection):
        for sub_collection in parent_collection.collectables:
          if collection_in_collection(collection, sub_collection):
            return True
      return False

    if isinstance(item, Playable):
      for folder_storage in self._all_storages.values():
        if item in folder_storage.playables or any([playable_in_collection(item, collection) for collection in folder_storage.collections]):
          add_playable_info(item)
          Storage.save_folder_storage(folder_storage)

    if isinstance(item, Collection):
      for folder_storage in self._all_storages.values():
        if item in folder_storage.collections or any([collection_in_collection(item, collection) for collection in folder_storage.collections]):
          add_collection_info(item)
          Storage.save_folder_storage(folder_storage)

  @staticmethod
  def refresh_folder_store(folder_storage: FolderStorage):
    folder_storage.playables = []
    folder_storage.collections = []
    if folder_storage.include_subfolders and folder_storage.search_type == 'playables':
      for root, _, files in os.walk(folder_storage.folder_path):
          for file_name in files:
              if file_name.endswith(tuple(general_settings.SUPPORTED_FILE_ENDINGS)):
                  playable = Playable(file_path=os.path.join(root, file_name))
                  add_playable_info(playable)
                  folder_storage.playables.append(playable)
    if not folder_storage.include_subfolders and folder_storage.search_type == 'playables':
      for file_name in os.listdir(folder_storage.folder_path):
        if file_name.endswith(tuple(general_settings.SUPPORTED_FILE_ENDINGS)):
          playable = Playable(file_path=os.path.join(folder_storage.folder_path, file_name))
          add_playable_info(playable)
          folder_storage.playables.append(playable)
    if folder_storage.search_type == 'collections':
      for dir_name in os.listdir(folder_storage.folder_path):
        if os.path.isdir(os.path.join(folder_storage.folder_path, dir_name)):
          try:
            collection = Collection(os.path.join(folder_storage.folder_path, dir_name))
            add_collection_info(collection, draw_collectbles=False)
            folder_storage.collections.append(collection)
          except:
            pass
    Storage.save_folder_storage(folder_storage)


  @staticmethod
  def save_folder_storage(folder_storage: FolderStorage):
      with open(os.path.join(CACHE_FOLDER, get_folder_storage_key(folder_storage.folder_path, folder_storage.search_type, folder_storage.include_subfolders)), 'w') as file:
        json.dump(folder_storage.__to_json__(), file)
