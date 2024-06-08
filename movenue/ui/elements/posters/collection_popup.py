import os
import tkinter as tk
from tkinter import font
from typing import Callable

from loguru import logger
from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.ui.elements.popup_window import PopupWindow
from movenue.ui.constants import ui_colors
from movenue.ui.elements.row import ScrollRow
from movenue.ui.elements import poster
import random
from movenue.services.play import play_playable

class CollectionPopup(tk.Frame):
    def __init__(self, master: tk.Widget, collection: Collection, width:int|None =None, height:int|None =None, storage:Storage|None=None):
        super().__init__(master)
        self.collection = collection
        self.current_season:Collection | None = None
        self.width = width
        self.height = height
        self.storage = storage
    @staticmethod
    def get_collection_playables(collection: Collection):
        playables:list[Playable] = []
        for c in collection.collectables:
            if isinstance(c, Collection):
                playables += CollectionPopup.get_collection_playables(c)
            if isinstance(c, Playable):
                playables.append(c)
        return playables
    
    def get_all_playables(self):
        return CollectionPopup.get_collection_playables(self.collection)
    
    def is_traditional_series(self):
        '''Returns True if the collection is a traditional series, False otherwise.
        A traditional series is a collection that contains only collections that contain only playables.'''
        return all([isinstance(c, Collection) and all([isinstance(p, Playable) for p in c.collectables]) for c in self.collection.collectables])
        
    def start_random(self):
        random_selector = random.sample(self.get_all_playables(),1)[0]
        play_playable(random_selector, self.storage)

    def start_random_unseen(self):
        playbles = self.get_all_playables()
        unseen_playables = [p for p in playbles if p.playcount == 0 or p.playcount is None]
        random_selector = random.sample(unseen_playables,1)[0]
        play_playable(random_selector, self.storage)
    
    def start_random_from_season(self):
        if not self.current_season:
            return
        random_selector = random.sample(self.get_collection_playables(self.current_season),1)[0]
        play_playable(random_selector, self.storage)

    def build_up(self):
        if not self.collection.collectables:
          self.storage.recache(self.collection)
        if not self.collection.collectables:
            return

        traditional_series_flag = self.is_traditional_series()

        popup_head_frame = tk.Frame(self, background=ui_colors.DEFAULT_BACKGROUND)
        popup_head_frame.pack(side='top', fill='x')

        lbl = tk.Label(popup_head_frame, text=self.collection.title, background=ui_colors.DEFAULT_BACKGROUND, foreground='black', font=font.Font(family='Arial', size=25))
        lbl.pack(side='top', padx=10, pady=10)

        popup_body_frame = tk.Frame(self, background=ui_colors.DEFAULT_BACKGROUND)
        popup_body_frame.pack(side=tk.TOP, expand=True, fill='both')
        popup_season_row = tk.Frame(popup_body_frame, background=ui_colors.DEFAULT_BACKGROUND)
        popup_season_row.pack(side=tk.TOP)
        popup_episodes_row = tk.Frame(popup_body_frame, background=ui_colors.DEFAULT_BACKGROUND)
        popup_episodes_row.pack(side=tk.TOP)
        popup_bottom_row = tk.Frame(popup_body_frame, background=ui_colors.DEFAULT_BACKGROUND)
        popup_bottom_row.pack(side=tk.TOP)
        random_eps = tk.Label(master=popup_bottom_row, text='Fully Random Episode', background=ui_colors.DEFAULT_BUTTON, foreground='white')
        random_eps.bind('<Button-1>', lambda ev: self.start_random())
        random_eps.grid(column=0, row=0, padx=10, pady=10, ipadx=10, ipady=10)
        if traditional_series_flag:
          random_eps = tk.Label(master=popup_bottom_row, text='Random Episode from Season', background=ui_colors.DEFAULT_BUTTON, foreground='white')
          random_eps.bind('<Button-1>', lambda ev: self.start_random_from_season())
          random_eps.grid(column=1, row=0, padx=10, pady=10, ipadx=10, ipady=10)
        random_eps = tk.Label(master=popup_bottom_row, text='Random unseen Episode', background=ui_colors.DEFAULT_BUTTON, foreground='white')
        random_eps.bind('<Button-1>', lambda ev: self.start_random_unseen())
        random_eps.grid(column=2, row=0, padx=10, pady=10, ipadx=10, ipady=10)

        
        if traditional_series_flag:

            def build_eps_row(season: Collection):
                for p in popup_episodes_row.pack_slaves():
                    p.pack_forget()

                episode_poster_lambdas = [poster.playable_poster_lambda(p, self, parent_collection=self.collection, show_title=True) for p in season.collectables]
                sr = ScrollRow(episode_poster_lambdas, master=popup_episodes_row, max_width=(self.width or self.master.winfo_screenwidth) - 20, height=200)
                sr.frame.pack(side='top')

            season_poster_lambdas = [poster.collection_poster_lambda(c, self, on_click=lambda season=c:build_eps_row(season)) for c in self.collection.collectables]
            row = ScrollRow(season_poster_lambdas, master=popup_season_row, max_width=(self.width or self.master.winfo_screenwidth) - 20, height=200)
            row.frame.pack(side='top')
            
        
        elif isinstance(self.collection.collectables[0], Collection):
            season_poster_lambdas = [poster.collection_poster_lambda(c, self) for c in self.collection.collectables]
            row = ScrollRow(season_poster_lambdas, master=popup_season_row, max_width=(self.width or self.master.winfo_screenwidth) - 20, height=200)
            row.frame.pack(side='top')
        elif isinstance(self.collection.collectables[0], Playable):
            build_posters = [poster.playable_poster_lambda(c, self) for c in self.collection.collectables]
            row = ScrollRow(build_posters, master=popup_season_row, max_width=(self.width or self.master.winfo_screenwidth) - 20, height=200)
            row.frame.pack(side='top')
            

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.build_up()

    def grid(self, **kwargs): 
        super().grid(**kwargs)
        self.build_up()

    def place(self, **kwargs):
        super().place(**kwargs)
        self.build_up()



def collection_popup(collection: Collection, storage:Storage|None=None) -> Callable[[tk.Widget], tk.Widget]:
    def popup_content(master: tk.Widget, width=None, **kwargs) -> tk.Widget:
        return CollectionPopup(master, collection, width=width, storage=storage, **kwargs)
    return popup_content