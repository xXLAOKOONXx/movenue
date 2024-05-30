from dataclasses import dataclass, field
from pathlib import Path
from PIL.Image import Image

from movenue.models.playable import Playable
from typing import List, Optional
from datetime import date


class Collection:
  pass

@dataclass
class Collection:
  """
  Represents a collection of either Collections or Playables.
  Examples might be series, seasons, franchises, albums, etc.
  """

  full_path: str | Path
  """
  The full path of the collection.
  """

  title: str = ''
  """
  The title of the collection.
  """

  alt_titles: List[str] = field(default_factory=list)
  """
  Alternative titles for the collection.
  """

  index_number: int | None = None
  """
  Number of this collection within a different colection.
  """

  collectables: List[Playable] | List[Collection] = field(default_factory=list)
  """
  The list of items (playables or sub-collections) in the collection.
  """

  lastplayed: Optional[date] = None
  """
  The date when the collection was last played.
  """

  playcount: int = 0
  """
  The number of times the collection has been played.
  """

  user_rating: int | None = None
  """
  The user rating for the collection.
  """

  public_rating: float | None = None
  """
  The public rating for the collection.
  """

  tags: List[str] = field(default_factory=list)
  """
  The tags associated with the collection.
  """

  artists: List[str] = field(default_factory=list)
  """
  The artists associated with the collection.
  """

  poster_image: Image | None = None
  """
  The poster image for the collection.
  Might be None if not built yet.
  Check the poster_location for the location of the image.
  """

  poster_location: str | Path | None = None
  """
  The location of the poster image of the playable item.
  Might be a file path to an image or a file containing the image.
  Might be None if no poster image is available.
  """

  def add_play_now_infos(self) -> None:
    """
    Add information for the current play session.
    """
    self.lastplayed = date.today()
    self.playcount += 1

  tkimages: dict[tuple[int, int], Image] = field(default_factory=dict)

  def __to_json__(self):
    return {
      'full_path': self.full_path,
      'title': self.title,
      'alt_titles': self.alt_titles,
      'index_number': self.index_number,
      'collectables': [collectable.__to_json__() for collectable in self.collectables],
      'lastplayed': self.lastplayed.isoformat() if self.lastplayed else None,
      'playcount': self.playcount,
      'user_rating': self.user_rating,
      'public_rating': self.public_rating,
      'tags': self.tags,
      'artists': self.artists,
      'poster_location': self.poster_location
    }
  
  @staticmethod
  def from_json(json_data: dict) -> Collection:
    return Collection(
      full_path=json_data['full_path'],
      title=json_data['title'],
      alt_titles=json_data['alt_titles'],
      index_number=json_data['index_number'],
      collectables=[Collection.from_json(collectable) if 'collectables' in collectable else Playable.from_json(collectable) for collectable in json_data['collectables']],
      lastplayed=date.fromisoformat(json_data['lastplayed']) if json_data['lastplayed'] else None,
      playcount=json_data['playcount'],
      user_rating=json_data['user_rating'],
      public_rating=json_data['public_rating'],
      tags=json_data['tags'],
      artists=json_data['artists'],
      poster_location=json_data['poster_location']
    )
