from tkinter import ttk
import tkinter as tk
from movenue.ui_elements.music.music_card import MusicCard

# Filtering:
# n Filtergroups
# options in filtergroup:
# - at least one of the following tags []
# - minimum user rating
# - search string
# - minimum duration in s
# - maximum duration in s
# - interpret

class MusicFilter:
    def __init__(self):
        self.filter_tags:list[tk.StringVar] = []
        self.min_userrating = tk.StringVar()
        self.max_userrating = tk.StringVar()
        self.min_duration = tk.StringVar()
        self.max_duration = tk.StringVar()
        self.search_string = tk.StringVar()
        self.interpret = tk.StringVar()
    
    def get_ui_element(self, master: tk.Widget, available_tags: list[str]):
        available_tags = available_tags + ['']
        available_tags = sorted(available_tags)
        self.frame = tk.Frame(master)

        # TAGS
        def add_tag_dropdown():
          string_var = tk.StringVar()
          self.filter_tags.append(string_var)
          ttk.Combobox(self.tag_frame, values=available_tags, textvariable=string_var, state='readonly').pack(side=tk.LEFT)
        self.tag_frame = tk.Frame(self.frame)
        self.tag_frame.pack()
        tk.Button(self.tag_frame, text='Add Tag', command=add_tag_dropdown).pack(side=tk.LEFT)

        # INTERPRET
        interpret_frame = tk.Frame(self.frame)
        interpret_frame.pack()
        tk.Label(interpret_frame, text='Interpret:').pack(side=tk.LEFT)
        tk.Entry(interpret_frame, textvariable=self.interpret).pack(side=tk.LEFT)

        # DURATION
        duration_frame = tk.Frame(self.frame)
        duration_frame.pack()
        tk.Label(duration_frame, text='Duration (s):').pack(side=tk.LEFT)
        tk.Entry(duration_frame, textvariable=self.min_duration, width=5).pack(side=tk.LEFT)
        tk.Label(duration_frame, text=' - ').pack(side=tk.LEFT)
        tk.Entry(duration_frame, textvariable=self.max_duration, width=5).pack(side=tk.LEFT)

        # USER RATING
        rating_frame = tk.Frame(self.frame)
        rating_frame.pack()
        tk.Label(rating_frame, text='User Rating:').pack(side=tk.LEFT)
        tk.Entry(rating_frame, textvariable=self.min_userrating, width=5).pack(side=tk.LEFT)
        tk.Label(rating_frame, text=' - ').pack(side=tk.LEFT)
        tk.Entry(rating_frame, textvariable=self.max_userrating, width=5).pack(side=tk.LEFT)

        # SEARCH STRING
        search_frame = tk.Frame(self.frame)
        search_frame.pack()
        tk.Label(search_frame, text='Search:').pack(side=tk.LEFT)
        tk.Entry(search_frame, textvariable=self.search_string).pack(side=tk.LEFT)

        return self.frame

    def is_in_tag_filter(self, card:MusicCard):
      filter_vals = [tag.get() for tag in self.filter_tags if tag.get()]
      if not filter_vals:
        return True
      if 'None' in filter_vals and not card.metadata.get('tags', []):
        return True
      return all(tag in card.metadata.get('tags', []) for tag in filter_vals)
    
    def is_in_rating_filter(self, card:MusicCard):
      if not self.min_userrating.get() and not self.max_userrating.get():
        return True
      try:
        high_enough = not self.min_userrating.get() or card.metadata.get('userrating',0) >= int(self.min_userrating.get())
        low_enough = not self.max_userrating.get() or card.metadata.get('userrating',0) <= int(self.max_userrating.get())
        return low_enough and high_enough
      except:
        return False
    
    def is_in_duration_filter(self, card:MusicCard):
      if not self.min_duration.get() and not self.max_duration.get():
        return True
      try:
        high_enough = not self.min_duration.get() or card.metadata.get('duration',0) >= int(self.min_duration.get())
        low_enough = not self.max_duration.get() or card.metadata.get('duration',0) <= int(self.max_duration.get())
        return low_enough and high_enough
      except:
        return False
      
    def is_in_search_filter(self, card:MusicCard):
      if not self.search_string.get():
        return True
      search = self.search_string.get().lower()
      return search in card.video_name.lower() or search in card.metadata.get('title','').lower() or any(search in a.lower() for a in card.metadata.get('artists',['']))
    
    def is_in_interpret_filter(self, card:MusicCard):
      if not self.interpret.get():
        return True
      return any(self.interpret.get().lower() in a.lower() for a in card.metadata.get('artists',['']))
    
    def passes_filter(self, card: MusicCard):
      return self.is_in_tag_filter(card) and self.is_in_rating_filter(card) and self.is_in_search_filter(card) and self.is_in_interpret_filter(card) and self.is_in_duration_filter(card)