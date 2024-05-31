
import os
from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.services import add_infos


def play_playable(playable:Playable, store:Storage, collection:Collection|None=None):
  playable.add_play_now_infos()
  if collection:
    collection.add_play_now_infos()
    add_infos.save_collection_to_file(collection)
  add_infos.save_playable_to_file(playable)
  os.startfile(os.path.abspath(playable.file_path))
  if store:
    store.recache(playable)