from mutagen.id3 import ID3, TextFrame
import json
import math

TAGS_KEY = 'TXXX:LAO:TAGS'
MUSIC_START_KEY = 'TXXX:LAO:MUSIC_START'
MUSIC_END_KEY = 'TXXX:LAO:MUSIC_END'
USERRATING_KEY = 'TXXX:LAO:USERRATING'


def extract_id3_metadata(file_path):
  '''
  Extracts metadata from a file with id3 tags.

  Args:
    file_path (str): The path to the file with id3 tags.

  Returns:
    dict: A dictionary containing the following keys:
      - 'title' (str): The title of the file.
      - 'artist' (list[str]): The artist of the file.
      - 'tags' (list): A list of additional tags associated with the file. (TXXX:LAO:TAGS)
      - 'userrating' (int): The user rating of the file. Prefers TXXX:LAO:USERRATING and also supports Windows rating (POPM:Windows Media Player 9 Series)
      - 'music_start' (int): time the music starts in milliseconds
      - 'music_end' (int): time the music ends in milliseconds

  Raises:
    Exception: If there is an error extracting the metadata.

  Example:
    >>> extract_mp4_metadata('/path/to/file.mp4')
    {
      'title': 'Song Title',
      'artists': ['Artist Name'],
      'tags': ['tag1', 'tag2'],
      'userrating': 4,      
      'music_start': 2000,
      'music_end': 160000,
    }
  '''
  try:
    id3 = ID3(file_path)
    if tags := id3.get(TAGS_KEY):
      tags = tags.text
    else:
      tags = []

    if music_start := id3.get(MUSIC_START_KEY):
      music_start = int(music_start.text[0])
    else:
      music_start = None

    if music_end := id3.get(MUSIC_END_KEY):
      music_end = int(music_end.text[0])
    else:
      music_end = None

    if title := id3.get('TIT2'):
      title = title.text[0]
    else:
      title = ''

    if artists := id3.get('TPE1'):
      artists = artists.text
    else:
      artists = ['']

    if wmp_rating := id3.get('POPM:Windows Media Player 9 Series'):
      wmp_rating = int(wmp_rating.rating)
      # POPM:Windows Media Player 9 Series decodes in 2^STAR
      wmp_rating = (int(math.log2(wmp_rating)) - 4) * 2
    else:
      wmp_rating = None

    if user_rating := id3.get(USERRATING_KEY):
      user_rating = int(user_rating.text[0])
    else:
      user_rating = None

    metadata = {
      'title': title,
      'artists': artists,
      # 'duration': mp4.info.length,
      # 'bitrate': mp4.info.bitrate,
      # 'sample_rate': mp4.info.sample_rate,
      # 'channels': mp4.info.channels,
      'tags': tags,
      # 'thumbnail': mp4.get('covr', []),  # Assuming thumbnail is stored in 'covr' tag
      'userrating': user_rating or wmp_rating,
      'music_start': music_start,
      'music_end': music_end,
    }
    return metadata
  except Exception as e:
    print(f'Error extracting ID3 metadata: {e}')
    return {}
  

def extract_id3_thumbnail(file_path):
  '''
  Extracts the thumbnail from a id3 file.

  Args:
    file_path (str): The path to the id3 file.

  Returns:
    bytes: The binary data of the thumbnail.

  Raises:
    Exception: If there is an error extracting the thumbnail from the MP4 file.
  '''
  try:
    id3 = ID3(file_path)
    pict = id3.get("APIC:").data
    # im = Image.open(BytesIO(pict))
    return pict
  except Exception as e:
    raise Exception(f'Error extracting thumbnail from ID3 file: {e}')

def set_thumbnail(file_path, thumbnail_binary):
  raise NotImplementedError()

def add_tag_to_id3(file_path, tag):
  '''
  Adds a tag to the list of tags associated with an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    tag (str): The tag to be added.

  Raises:
    Exception: If there is an error adding the tag to the MP4 file.
  '''
  try:
    id3 = ID3(file_path)
    tags = []
    if prev_tags := id3.get(TAGS_KEY):
      tags = prev_tags.text
    tags.append(tag)

    tf = TextFrame(text=tags)
    id3.setall(TAGS_KEY, [tf])

    id3.save()
  except Exception as e:
    raise Exception(f'Error adding tag to MP4 file: {e}')
  
    
def set_id3_userrating(file_path, rating: int):
  '''
  Sets the user rating for an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    rating (int): The user rating to be set. Should be between 0 and 10.

  Raises:
    Exception: If there is an error setting the user rating for the MP4 file.
  '''
  try:
    id3 = ID3(file_path)
    tf = TextFrame(text=str(rating))
    id3.setall(USERRATING_KEY, tf)
    id3.save()
  except Exception as e:
    raise Exception(f'Error setting user rating for id3 file: {e}')
  

def set_id3_music_start(file_path, start_in_ms):
  try:
    id3 = ID3(file_path)
    tf = TextFrame(text=str(start_in_ms))
    id3.setall(MUSIC_START_KEY, tf)
    id3.save()
  except Exception as e:
    raise Exception(f'Error setting music start for id3 file: {e}')

def set_id3_music_end(file_path, end_in_ms):
  try:
    id3 = ID3(file_path)
    tf = TextFrame(text=str(end_in_ms))
    id3.setall(MUSIC_END_KEY, tf)
    id3.save()
  except Exception as e:
    raise Exception(f'Error setting music end for id3 file: {e}')