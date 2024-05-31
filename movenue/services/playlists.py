from dataclasses import dataclass
import os
from pathlib import Path
import tempfile
from typing import Callable
import xml.etree.ElementTree as ET
from movenue.models.collection import Collection
from movenue.models.playable import Playable

def default_playlist_location():
  """
  Get the default location for the XML playlist file.

  Returns:
    str: Default location for the XML playlist file.
  """
  # Get the tmp folder assigned to the application
  tmp_folder = tempfile.gettempdir()
  return os.path.join(tmp_folder, "playlist.xspf")

def build_xml_playlist(items:list[Playable | Collection], target_location=None):
  """
  Build an XML playlist file.

  Args:
    files (list): List of PlaylistItems.
    target_location (str, optional): Target location to save the XML playlist file.
      If not provided, a file in the tmp folder assigned to the application will be used.

  Example usage:
    files = [PlaylistItem("song1.mp3"), PlaylistItem("song2.mp3"), PlaylistItem("song3.mp3")]
    target_location = "playlist.xspf"
    build_xml_playlist(files, target_location)
  """
  if target_location is None:
    target_location = default_playlist_location()

  # Create the root element
  playlist = ET.Element("playlist", {"xmlns:vlc":"http://www.videolan.org/vlc/playlist/ns/0/"}, version="1", xmlns="http://xspf.org/ns/0/")

  # Create the trackList element
  tracklist = ET.SubElement(playlist, "trackList")

  for item in items:
    track = ET.SubElement(tracklist, "track")
    location = ET.SubElement(track, "location")
    location.text = str(Path(item.file_path))
    if item.start_time_ms or item.end_time_ms:
      # Implemented based on: https://wiki.videolan.org/XSPF/#Example_of_XSPF_with_VLC_extensions 
      extension = ET.SubElement(track, 'extension', application='http://www.videolan.org/vlc/playlist/0')
      if item.start_time_ms:
        start_el = ET.SubElement(extension, 'vlc:option')
        start_el.text = f'start-time={item.start_time_ms / 1000}'
      if item.end_time_ms:
        end_el = ET.SubElement(extension, 'vlc:option')
        end_el.text = f'stop-time={item.end_time_ms / 1000}'

  # Create the XML tree
  tree = ET.ElementTree(playlist)

  # Write the XML tree to the target location
  tree.write(target_location, encoding="utf-8", xml_declaration=True)

def linear_weighting(score: int | float | None) -> int:
  if not score:
    return 1
  return int(score)

def exponential_weighting(score: int | float | None) -> int:
  '''
  example implementation for exponential weighting.
  I disadvise using it as the playlist gets too fast too big.
  '''
  if score is None:
    return 1
  return int(2**score)

def weight_playlist_items(items:list[Playable | Collection], weighting_function:Callable[[int|float|None], int] = linear_weighting) -> list[Playable | Collection]:
  '''
  function to build a new list of PlaylistItems weighted based on the score and weighting_function.
  Args:
  - items: Items to use in the new list
  - weighting_function: Function to determine the occurance amount of each item, be careful with this as too big playlists might lead to faulty behavior of the player
  Returns:
  - weighted_playlist_items list[PlaylistItem]
  '''
  new_list = []
  for item in items:
    for _ in range(0, weighting_function(item.user_rating)):
      new_list.append(item)
  return new_list
