

import os
from pathlib import Path
from typing import List

from movenue.models.playable import Playable
from movenue.constants import general_settings
from movenue.services.playables_population import add_playable_info


def get_all_playables_in_folder(folder_path: str | Path, include_subfolders: bool = True) -> List[Playable]:
    """
    Get all the playables in the folder path.
    """
    playables = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(tuple(general_settings.SUPPORTED_FILE_ENDINGS)):
                playable = Playable(file_path=os.path.join(root, file_name))
                add_playable_info(playable)
                playables.append(playable)
    return playables