from tkinter import PhotoImage
from typing import List, Self
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from PIL.Image import Image

# TODDO Add description

@dataclass
class Playable:
  """
  Represents a playable item in the application.
  """

  file_path: str | Path
  """
  The file path or URL of the playable item.
  """

  title: str = ''
  """
  The title of the playable item.
  """

  index_number: int | None = None
  """
  Number of the playable item in the collection.
  """

  alt_titles: list[str] = field(default_factory=list)
  """
  Alternate titles of the playable item.
  """

  lastplayed: date | None = None
  """
  The date when the playable item was last played.
  """

  playcount: int = 0
  """
  The number of times the playable item has been played.
  """

  user_rating: int | None = None
  """
  The user rating of the playable item.
  """

  public_rating: float | None = None
  """
  The public rating of the playable item.
  """

  tags: list[str] = field(default_factory=list)
  """
  The tags associated with the playable item.
  """

  poster_image: Image | None = None
  """
  The poster image of the playable item.
  """

  poster_location: str | Path | None = None
  """
  The location of the poster image of the playable item.
  Might be a file path to an image or a file containing the image.
  """

  languages: list[str] = field(default_factory=list)
  """
  The languages of the playable item.
  """

  uploader: str | None = None
  """
  The uploader of the playable item.
  """

  artists: list[str] = field(default_factory=list)
  """
  The artists associated with the playable item.
  This might include directors, actors, singers, etc.
  """

  start_time_ms: int | None = None
  """
  The start time of the playable item in milliseconds.
  """

  end_time_ms: int | None = None
  """
  The end time of the playable item in milliseconds.
  (timepoint based on original duration of the item excluding any cuts)
  """

  play_duration_ms: int | None = None
  """
  The duration of the playable item in milliseconds excluding any cuts.
  """

  premiere_date: date | None = None
  """
  The premiere date of the playable item.
  """

  def add_play_now_infos(self) -> None:
    """
    Add information for the current play session.
    """
    self.lastplayed = date.today()
    self.playcount += 1

  tkimages: dict[tuple[int,int], PhotoImage] = field(default_factory=dict)

  def __to_json__(self) -> dict:
    """
    Convert the object to a JSON serializable dictionary.
    """
    return {
      'file_path': self.file_path,
      'title': self.title,
      'index_number': self.index_number,
      'alt_titles': self.alt_titles,
      'lastplayed': self.lastplayed.isoformat() if self.lastplayed else None,
      'playcount': self.playcount,
      'user_rating': self.user_rating,
      'public_rating': self.public_rating,
      'tags': self.tags,
      'poster_location': self.poster_location,
      'languages': self.languages,
      'uploader': self.uploader,
      'artists': self.artists,
      'start_time_ms': self.start_time_ms,
      'end_time_ms': self.end_time_ms,
      'play_duration_ms': self.play_duration_ms,
      'premiere_date': self.premiere_date.isoformat() if self.premiere_date else None
    }
  
  @staticmethod
  def from_json(json_data: dict) -> Self:
    """
    Create a Playable object from a JSON serializable dictionary.
    """
    return Playable(
      file_path=json_data['file_path'],
      title=json_data['title'],
      index_number=json_data['index_number'],
      alt_titles=json_data['alt_titles'],
      lastplayed=date.fromisoformat(json_data['lastplayed']) if json_data['lastplayed'] else None,
      playcount=json_data['playcount'],
      user_rating=json_data['user_rating'],
      public_rating=json_data['public_rating'],
      tags=json_data['tags'],
      poster_location=json_data['poster_location'],
      languages=json_data['languages'],
      uploader=json_data['uploader'],
      artists=json_data['artists'],
      start_time_ms=json_data['start_time_ms'],
      end_time_ms=json_data['end_time_ms'],
      play_duration_ms=json_data['play_duration_ms'],
      premiere_date=date.fromisoformat(json_data.get('premiere_date')) if json_data.get('premiere_date') else None
    )