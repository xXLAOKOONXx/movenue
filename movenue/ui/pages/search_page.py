from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.ui.elements.poster_wall import PosterWall
import tkinter as tk
from tkinter import ttk
from movenue.ui.elements.poster import build_poster


class SearchPage(tk.Frame):
    def __init__(self, master, store: Storage, page_name: str, **kwargs):
        super().__init__(master, **kwargs)

        self.store = store
        self.page_name = page_name
        self.popup_master = master

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(side='top', fill='x')

        self.search_button = ttk.Button(self, text='Search', command=self.search)
        self.search_button.pack(side='top')

        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side='top', fill='both', expand=True)

    def search(self, *args):
        self.update_poster_wall()

    def update_poster_wall(self):
        for slave in self.result_frame.pack_slaves():
            slave.pack_forget()
        self.poster_wall = PosterWall(self.result_frame, self.get_poster_lambdas(), poster_height=200)
        self.poster_wall.pack(side='top', fill='both', expand=True)

    def get_poster_lambdas(self):
        playables = self.store.get_playables(self.page_name)
        collections = self.store.get_collections(self.page_name)
        def is_searchable_playable(playable:Playable):
            return self.search_var.get().lower() in playable.title.lower()
        def is_searchable_collection(collection:Collection):
            return self.search_var.get().lower() in collection.title.lower()
        filtered_playables = [playable for playable in playables if is_searchable_playable(playable)]
        filtered_collections = [collection for collection in collections if is_searchable_collection(collection)]
        filtered_elements = filtered_playables + filtered_collections
        return [build_poster(filtered_element, self.popup_master) for filtered_element in filtered_elements]
    
    def pack(self, **kwargs):
        self.update_poster_wall()
        super().pack(**kwargs)

    def grid(self, **kwargs):
        self.update_poster_wall()
        super().grid(**kwargs)

    def place(self, **kwargs):
        self.update_poster_wall()
        super().place(**kwargs)