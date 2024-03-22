from dataclasses import dataclass
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

@dataclass
class PlaylistItem:
  file_path: str | Path
  '''path to the music file'''
  music_start: int | None = None
  '''Start in milliseconds, defaults to None (no cropping)'''
  music_end: int | None = None
  '''End of music in milliseconds, defaults to None (no cropping)'''


def default_playlist_location():
  """
  Get the default location for the XML playlist file.

  Returns:
    str: Default location for the XML playlist file.
  """
  # Get the tmp folder assigned to the application
  tmp_folder = tempfile.gettempdir()
  return os.path.join(tmp_folder, "playlist.xspf")

# TODO: Encorporate music-start and music-end
# Implemented it looks like this example: https://wiki.videolan.org/XSPF/#Example_of_XSPF_with_VLC_extensions
def build_xml_playlist(items:list[PlaylistItem], target_location=None):
  """
  Build an XML playlist file.

  Args:
    files (list): List of file names.
    target_location (str, optional): Target location to save the XML playlist file.
      If not provided, a file in the tmp folder assigned to the application will be used.

  Example usage:
    files = ["song1.mp3", "song2.mp3", "song3.mp3"]
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
    location.text = str(item.file_path)
    if item.music_start or item.music_end:
      extension = ET.SubElement(track, 'extension', application='http://www.videolan.org/vlc/playlist/0')
      if item.music_start:
        start_el = ET.SubElement(extension, 'vlc:option')
        start_el.text = f'start-time={item.music_start / 1000}'
      if item.music_end:
        end_el = ET.SubElement(extension, 'vlc:option')
        end_el.text = f'stop-time={item.music_end / 1000}'

  # Create the XML tree
  tree = ET.ElementTree(playlist)

  # Write the XML tree to the target location
  tree.write(target_location, encoding="utf-8", xml_declaration=True)
