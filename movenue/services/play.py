
import os
from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.services import add_infos
from movenue.services.playables_population import add_playable_info
from movenue.services.collections_population import add_collection_info


def play_playable(playable:Playable, store:Storage, collection:Collection|None=None):
  os.startfile(os.path.abspath(playable.file_path))
  add_playable_info(playable)
  playable.add_play_now_infos()
  if collection:
    add_collection_info(collection, draw_collectbles=False)
    collection.add_play_now_infos()
    add_infos.save_collection_to_file(collection, storage=store)
  add_infos.save_playable_to_file(playable, store=store)
