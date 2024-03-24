'''
Interface module for communication with files metadata

Supported types:
- MP4
- ID3 (eg MP3)
'''

from movenue.services import mp4_metadata
from movenue.services import id3_metadata
import os

def is_mp4_file(file_path):
  _filename, file_extension = os.path.splitext(file_path)
  return file_extension == '.mp4'

def extract_metadata(file_path):
  '''
  Extracts metadata from an file.

  Args:
    file_path (str): The path to the file.

  Returns:
    dict: A dictionary containing the following keys:
      - 'title' (str): The title of the file.
      - 'artist' (list[str]): The artist of the file.
      - 'tags' (list): A list of additional tags associated with the file.
      - 'userrating' (int): The user rating of the file.

  Raises:
    Exception: If there is an error extracting the metadata.

  Example:
    >>> extract_mp4_metadata('/path/to/file.mp4')
    {
      'title': 'Song Title',
      'artists': 'Artist Name',
      'tags': ['tag1', 'tag2'],
      'userrating': 4
    }
  '''
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.extract_mp4_metadata(file_path=file_path)
  return id3_metadata.extract_id3_metadata(file_path=file_path)

  
def extract_thumbnail(file_path):
  '''
  Extracts the thumbnail from an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.

  Returns:
    bytes: The binary data of the thumbnail.

  Raises:
    Exception: If there is an error extracting the thumbnail from the MP4 file.
  '''
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.extract_mp4_thumbnail(file_path=file_path)
  return id3_metadata.extract_id3_thumbnail(file_path=file_path)

def add_tag(file_path, tag):
  '''
  Adds a tag to the list of tags associated with an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    tag (str): The tag to be added.

  Raises:
    Exception: If there is an error adding the tag to the MP4 file.
  '''
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.add_tag_to_mp4(file_path=file_path, tag=tag)
  return id3_metadata.add_tag_to_id3(file_path=file_path, tag=tag)

def set_userrating(file_path, rating: int):
  '''
  Sets the user rating for an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    rating (int): The user rating to be set. Should be between 0 and 10.

  Raises:
    Exception: If there is an error setting the user rating for the MP4 file.
  '''
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.add_tag_to_mp4(file_path=file_path, rating=rating)
  return id3_metadata.add_tag_to_id3(file_path=file_path, rating=rating)

def set_thumbnail(file_path, thumbnail_binary):
  '''
  Sets the thumbnail for an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    thumbnail_binary (bytes): The binary data of the thumbnail.

  Raises:
    Exception: If there is an error setting the thumbnail for the MP4 file.
  '''
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.set_thumbnail(file_path=file_path, thumbnail_binary=thumbnail_binary)
  return id3_metadata.set_thumbnail(file_path=file_path, thumbnail_binary=thumbnail_binary)

def set_music_start(file_path, start_in_ms):
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.set_music_start(file_path=file_path, start_in_ms=start_in_ms)
  return id3_metadata.set_id3_music_start(file_path=file_path, start_in_ms=start_in_ms)

def set_music_end(file_path, end_in_s):
  if is_mp4_file(file_path=file_path):
    return mp4_metadata.set_music_end(file_path=file_path, end_in_s=end_in_s)
  return id3_metadata.set_id3_music_end(file_path=file_path, end_in_s=end_in_s)
