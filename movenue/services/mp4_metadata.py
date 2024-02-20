from mutagen.mp4 import MP4

def extract_mp4_metadata(file_path):
  '''
  Extracts metadata from an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.

  Returns:
    dict: A dictionary containing the following keys:
      - 'title' (str): The title of the MP4 file.
      - 'artist' (list[str]): The artist of the MP4 file.
      - 'duration' (float): The duration of the MP4 file in seconds.
      - 'bitrate' (int): The bitrate of the MP4 file in bits per second.
      - 'sample_rate' (int): The sample rate of the MP4 file in Hz.
      - 'channels' (int): The number of audio channels in the MP4 file.
      - 'tags' (list): A list of additional tags associated with the MP4 file.
      - 'userrating' (int): The user rating of the MP4 file.

  Raises:
    Exception: If there is an error extracting the MP4 metadata.

  Example:
    >>> extract_mp4_metadata('/path/to/file.mp4')
    {
      'title': 'Song Title',
      'artists': 'Artist Name',
      'duration': 240.5,
      'bitrate': 320000,
      'sample_rate': 44100,
      'channels': 2,
      'tags': ['tag1', 'tag2'],
      'userrating': 4
    }
  '''
  try:
    mp4 = MP4(file_path)
    if userrating := mp4.get('----:LAO:userrating', [None])[0]:
      userrating = int(userrating.decode('utf-8'))
    else:
      userrating = None
    metadata = {
      'title': mp4.get('\xa9nam', [''])[0],
      'artists': mp4.get('\xa9ART', ['']),
      'duration': mp4.info.length,
      'bitrate': mp4.info.bitrate,
      'sample_rate': mp4.info.sample_rate,
      'channels': mp4.info.channels,
      'tags': mp4.get('tags', []),
      # 'thumbnail': mp4.get('covr', []),  # Assuming thumbnail is stored in 'covr' tag
      'userrating': userrating,
    }
    return metadata
  except Exception as e:
    print(f'Error extracting MP4 metadata: {e}')
    return {}
  
def extract_mp4_thumbnail(file_path):
  '''
  Extracts the thumbnail from an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.

  Returns:
    bytes: The binary data of the thumbnail.

  Raises:
    Exception: If there is an error extracting the thumbnail from the MP4 file.
  '''
  try:
    mp4 = MP4(file_path)
    return mp4.get('covr', [])
  except Exception as e:
    raise Exception(f'Error extracting thumbnail from MP4 file: {e}')

def add_tag_to_mp4(file_path, tag):
  '''
  Adds a tag to the list of tags associated with an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    tag (str): The tag to be added.

  Raises:
    Exception: If there is an error adding the tag to the MP4 file.
  '''
  try:
    mp4 = MP4(file_path)
    tags = mp4.get('tags', [])
    tags.append(tag)
    tags = list(set(tags))
    mp4['tags'] = tags
    mp4.save()
  except Exception as e:
    raise Exception(f'Error adding tag to MP4 file: {e}')
  
def set_userrating(file_path, rating: int):
  '''
  Sets the user rating for an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    rating (int): The user rating to be set. Should be between 0 and 10.

  Raises:
    Exception: If there is an error setting the user rating for the MP4 file.
  '''
  try:
    mp4 = MP4(file_path)
    mp4['----:LAO:userrating'] = bytes(str(rating), 'utf-8')
    mp4.save()
  except Exception as e:
    raise Exception(f'Error setting user rating for MP4 file: {e}')
  
def set_thumbnail(file_path, thumbnail_binary):
  '''
  Sets the thumbnail for an MP4 file.

  Args:
    file_path (str): The path to the MP4 file.
    thumbnail_binary (bytes): The binary data of the thumbnail.

  Raises:
    Exception: If there is an error setting the thumbnail for the MP4 file.
  '''
  try:
    mp4 = MP4(file_path)
    mp4['covr'] = [thumbnail_binary]
    mp4.save()
  except Exception as e:
    raise Exception(f'Error setting thumbnail for MP4 file: {e}')
