import tkinter as tk
from tkinter import ttk

from movenue.models.collection import Collection
from movenue.models.playable import Playable


class ItemFilter:
    def __init__(self):
        self.filter_tags:list[tk.StringVar] = []
        self.min_userrating = tk.StringVar()
        self.max_userrating = tk.StringVar()
        self.min_duration = tk.StringVar()
        self.max_duration = tk.StringVar()
        self.search_string = tk.StringVar()
        self.interpret = tk.StringVar()
        self.file_extension = tk.StringVar()
    
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

        # FILE EXTENSION
        extension_frame = tk.Frame(self.frame)
        extension_frame.pack()
        tk.Label(extension_frame, text='File Extension:').pack(side=tk.LEFT)
        tk.Entry(extension_frame, textvariable=self.file_extension).pack(side=tk.LEFT)


        return self.frame

    def is_in_tag_filter(self, item: Playable | Collection):
      filter_vals = [tag.get() for tag in self.filter_tags if tag.get()]
      if not filter_vals:
        return True
      if isinstance(item, Playable):
        tags = item.tags
      if isinstance(item, Collection):
        tags = item.tags
      if 'None' in filter_vals and not tags:
        return True
      return all(tag in tags for tag in filter_vals)
    
    
    def is_in_rating_filter(self, item: Playable | Collection):
      if not self.min_userrating.get() and not self.max_userrating.get():
        return True
      
      if isinstance(item, Playable):
        rating = item.user_rating
      if isinstance(item, Collection):
        rating = item.user_rating
      
      if not rating:
        return False
      
      return (not self.min_userrating.get() or rating >= int(self.min_userrating.get())) and (not self.max_userrating.get() or rating <= int(self.max_userrating.get()))

    
    def is_in_duration_filter(self, item: Playable | Collection):
      if not self.min_duration.get() and not self.max_duration.get():
        return True
      
      if isinstance(item, Collection):
        return False
      
      if not item.play_duration_ms:
        return False
      
      return (not self.min_duration.get() or item.play_duration_ms >= int(self.min_duration.get())*1000) and (not self.max_duration.get() or item.play_duration_ms <= int(self.max_duration.get())*1000)

      
    def is_in_search_filter(self, item: Playable | Collection):
      if not self.search_string.get():
        return True
      search = self.search_string.get().lower()
      return search in item.title.lower() or any(search in a.lower() for a in item.artists)
    
    def is_in_interpret_filter(self, item: Playable | Collection):
      if not self.interpret.get():
        return True
      return any(self.interpret.get().lower() in a.lower() for a in item.artists)
    
    def is_in_file_extension_filter(self, item: Playable | Collection):
      if not self.file_extension.get():
        return True
      
      if isinstance(item, Collection):
        return False
      
      return item.file_path.endswith(self.file_extension.get().strip('.'))
    
    def passes_filter(self, item: Playable | Collection):
      return self.is_in_tag_filter(item) and self.is_in_rating_filter(item) and self.is_in_search_filter(item) and self.is_in_interpret_filter(item) and self.is_in_duration_filter(item) and self.is_in_file_extension_filter(item)