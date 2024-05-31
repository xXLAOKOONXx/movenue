

import random
from tkinter import Frame

from movenue.ui.elements.poster import playable_poster_lambda, collection_poster_lambda, build_poster
from movenue.ui.elements.row import HeadedScrollRow
from movenue.ui.elements.row_scrollbox import RowScrollBox
from movenue.models.storage import Storage
from movenue.services import scoring
from datetime import date


class CategoryPage(Frame):
  def __init__(self, master, store: Storage, page_name: str, add_random_category:bool=False, add_recent_category:bool=False, **kwargs):
    super().__init__(master, **kwargs)
    self._store = store
    self._page_name = page_name
    self._add_random_category = add_random_category
    self._add_recent_category = add_recent_category

  def set_up(self):
    for slave in self.pack_slaves():
      slave.pack_forget()
    for slave in self.grid_slaves():
      slave.grid_forget()
    for slave in self.place_slaves():
      slave.place_forget()

    categories = []
    collections = self._store.get_collections(self._page_name)
    playables = self._store.get_playables(self._page_name)

    playables.sort(key=lambda p: scoring.calculate_playable_score(p), reverse=True)

    # TODO: Add sorting by score

    for playable in playables:
      for category in playable.tags:
        if category not in categories:
          categories.append(category)
    for collection in collections:
      for category in collection.tags:
        if category not in categories:
          categories.append(category)

    items = playables + collections

    rows = []
    if self._add_recent_category:
      items.sort(key=lambda p: p.lastplayed or date(year=1900,month=1,day=1), reverse=True)
      rows.append(lambda master: HeadedScrollRow([build_poster(p, self, False, storage=self._store) for p in items[:10]], 
                                                 self.winfo_screenwidth(), master=master, title='Recently Played'))
      
    if self._add_random_category:
      random.seed(date.today().isoformat())
      rows.append(lambda master: HeadedScrollRow([build_poster(p, self, False, storage=self._store) for p in random.sample(items, 50)], 
                                                 self.winfo_screenwidth(), master=master, title='Random Selection'))
      random.seed()


    additional_rows = [lambda master, category=category: HeadedScrollRow(
              [playable_poster_lambda(p, self, False, storage=self._store) for p in playables if category in p.tags] + 
              [collection_poster_lambda(p, self, False, storage=self._store) for p in collections if category in p.tags], 
              self.winfo_screenwidth(), 
              master=master,
              title=category,) 
            for category in categories]
    random.shuffle(additional_rows)
    
    rows += additional_rows

    # for row in rows:
    #   row.pack(side='top', fill='x', padx=0, pady=0)
    self.row_scroll_box = RowScrollBox(self, rows)
    self.row_scroll_box.pack(side='top', fill='both', expand=True)

  def pack(self, **kwargs):
    self.set_up()
    super().pack(**kwargs)

  def grid(self, **kwargs):
    self.set_up()
    super().grid(**kwargs)

  def place(self, **kwargs):
    self.set_up()
    super().place(**kwargs)