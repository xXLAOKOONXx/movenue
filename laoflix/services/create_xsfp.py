import os
import tempfile
import xml.etree.ElementTree as ET

def default_playlist_location():
  """
  Get the default location for the XML playlist file.

  Returns:
    str: Default location for the XML playlist file.
  """
  # Get the tmp folder assigned to the application
  tmp_folder = tempfile.gettempdir()
  return os.path.join(tmp_folder, "playlist.xspf")

def build_xml_playlist(files, target_location=None):
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
  playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")

  # Create the trackList element
  tracklist = ET.SubElement(playlist, "trackList")

  # Iterate over the files and create track elements
  for file in files:
    track = ET.SubElement(tracklist, "track")
    location = ET.SubElement(track, "location")
    location.text = file

  # Create the XML tree
  tree = ET.ElementTree(playlist)

  # Write the XML tree to the target location
  tree.write(target_location, encoding="utf-8", xml_declaration=True)
