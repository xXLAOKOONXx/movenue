from tkinter import filedialog
from loguru import logger
from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.ui.elements.poster_wall import PosterWall
import tkinter as tk
from tkinter import ttk
from movenue.ui.elements.poster import build_poster
from movenue.ui.elements.filter import ItemFilter
from movenue.services import playlists
import os


class FilterPage(tk.Frame):
    def __init__(self, master, store: Storage, page_name: str, **kwargs):
        super().__init__(master, **kwargs)

        self.store = store
        self.page_name = page_name
        self.popup_master = master

        self.weight_playlist_active = tk.IntVar()

        self.available_tags = []
        self.item_filters:list[ItemFilter] = []

        self.filter_frame_wrapper = tk.Frame(self)
        self.filter_frame_wrapper.pack(side='top', fill='x')

        self.filter_frame = tk.Frame(self.filter_frame_wrapper)
        self.filter_frame.pack(side='top', fill='x')

        self.filter_buttons_frame = tk.Frame(self.filter_frame_wrapper)
        self.filter_buttons_frame.pack(side='top')

        self.add_filter_button = tk.Button(self.filter_buttons_frame, text='Add Filter', command=self.add_filter)
        self.add_filter_button.pack(side='left')

        self.remove_filter_button = tk.Button(self.filter_buttons_frame, text='Remove Filter', command=self.remove_filter)
        self.remove_filter_button.pack(side='left')

        self.apply_filter_button = tk.Button(self.filter_buttons_frame, text='Apply Filter', command=self.update_poster_wall)
        self.apply_filter_button.pack(side='left')

        self.additional_options_frame = tk.Frame(self)
        self.additional_options_frame.pack(side='top', fill='x')
        
        self.weight_playlist_toggle = tk.Checkbutton(self.additional_options_frame, text="Apply weighting", variable=self.weight_playlist_active)
        self.weight_playlist_toggle.pack()

        self.actions_frame = tk.Frame(self)
        self.actions_frame.pack(side='top', fill='x')

        self.start_playlist_button = tk.Button(self.actions_frame, text='Start Playlist', command=self.start_playlist)
        self.start_playlist_button.pack(side='left')

        self.save_playlist_button = tk.Button(self.actions_frame, text='Save Playlist', command=self.save_playlist)
        self.save_playlist_button.pack(side='left')

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side='top', fill='both', expand=True)

    def add_filter(self):
        self.item_filters.append(ItemFilter())
        self.update_filters()

    def remove_filter(self):
        if len(self.item_filters) > 0:
            self.item_filters.pop()
            self.update_filters()

    def start_playlist(self):
        filtered_items = self.get_filtered_items()
        if self.weight_playlist_active.get():
            filtered_items = playlists.weight_playlist_items(filtered_items)

        playlists.build_xml_playlist(filtered_items)
        os.startfile(playlists.default_playlist_location())
    
    def save_playlist(self):
        target_location = filedialog.asksaveasfilename(defaultextension='.xspf', filetypes=[('XSPF files', '*.xspf')])
        if not target_location:
          return
        filtered_items = self.get_filtered_items()
        if self.weight_playlist_active.get():
            filtered_items = playlists.weight_playlist_items(filtered_items)

        playlists.build_xml_playlist(filtered_items, target_location=target_location)

    def update_poster_wall(self):
        for slave in self.result_frame.pack_slaves():
            slave.pack_forget()
        self.poster_wall = PosterWall(self.result_frame, self.get_poster_lambdas(), poster_height=200)
        self.poster_wall.pack(side='top', fill='both', expand=True)

    def get_filtered_items(self):
        playables = self.store.get_playables(self.page_name)
        collections = self.store.get_collections(self.page_name)
        
        items = playables + collections
        filtered_items = [item for item in items if all([item_filter.passes_filter(item) for item_filter in self.item_filters])]
        return filtered_items

    def get_poster_lambdas(self):
        return [build_poster(filtered_element, self.popup_master) for filtered_element in self.get_filtered_items()]
    
    def pack(self, **kwargs):
        self.update_available_tags()
        self.update_filters()
        self.update_poster_wall()
        super().pack(**kwargs)

    def grid(self, **kwargs):
        self.update_available_tags()
        self.update_filters()
        self.update_poster_wall()
        super().grid(**kwargs)

    def place(self, **kwargs):
        self.update_available_tags()
        self.update_filters()
        self.update_poster_wall()
        super().place(**kwargs)

    
    def update_filters(self):
        for slave in self.filter_frame.pack_slaves():
            slave.pack_forget()
        for item_filter in self.item_filters:
            filter_ui = item_filter.get_ui_element(self.filter_frame, self.available_tags)
            filter_ui.pack(side='left')


    def update_available_tags(self):
        playables = self.store.get_playables(self.page_name)
        collections = self.store.get_collections(self.page_name)
        items = playables + collections
        tags = set()
        for item in items:
            tags.update(item.tags)
        self.available_tags = list(tags)