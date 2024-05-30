


from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Literal, Self

SEARCH_TYPES = Literal['playables', 'collections']
PAGE_MODULES = Literal['category_page', 'search_page', 'filter_page']

@dataclass
class FolderSetting:
  path: str | Path
  search_type: SEARCH_TYPES
  include_subfolders_for_playables: bool = True

  def __to_json__(self):
    return {
      'path': str(self.path),
      'search_type': self.search_type,
      'include_subfolders_for_playables': self.include_subfolders_for_playables
    }
  
  @staticmethod
  def from_json(json) -> Self:
    return FolderSetting(
      path=json['path'],
      search_type=json['search_type'],
      include_subfolders_for_playables=json['include_subfolders_for_playables']
    )



@dataclass
class CategorySettings:
  name: str
  folders: List[FolderSetting]
  page_module: PAGE_MODULES
  key_word_args: dict[str,any] = field(default_factory=dict)

  def __to_json__(self):
    return {
      'name': self.name,
      'folders': [folder.__to_json__() for folder in self.folders],
      'page_module': self.page_module,
      'key_word_args': self.key_word_args
    }
  
  @staticmethod
  def from_json(json) -> Self:
    return CategorySettings(
      name=json['name'],
      folders=[FolderSetting.from_json(folder_json) for folder_json in json['folders']],
      page_module=json['page_module'],
      key_word_args=json.get('key_word_args', {})
    )