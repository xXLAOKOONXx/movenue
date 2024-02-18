import tkinter as tk
from movenue.services.settings import settings

from movenue.ui_elements.page import Page
from tkinter import filedialog
from movenue.services.info_cache import info_cache


class SettingsPage(Page):
    def __init__(self):
        super().__init__()

    def set_master(self, master):
        super().set_master(master)
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.header = tk.Label(self.frame, text='Settings')
        self.header.pack()
        self.label = tk.Label(self.frame, text=str(settings.settings))
        self.label.pack()
        self.button_movie = tk.Button(self.frame, text='Add Movie folder', command=self.add_movie_folder)
        self.button_movie.pack()
        self.button_shortfilm = tk.Button(self.frame, text='Add Shortfilm folder', command=self.add_shortfilm_folder)
        self.button_shortfilm.pack()
        self.button_series = tk.Button(self.frame, text='Add Series folder', command=self.add_series_folder)
        self.button_series.pack()
        self.button_music = tk.Button(self.frame, text='Add Music folder', command=self.add_music_folder)
        self.button_music.pack()
        self.cache_flip = tk.Button(self.frame, text='Flip Cache', command=self.flip_cache)
        self.cache_flip.pack()
        self.optional_cache_frame = tk.Frame(self.frame)
        tk.Button(self.optional_cache_frame, text='Recache Music', command=info_cache.rebuild_music_info_jsons).pack()
        tk.Button(self.optional_cache_frame, text='Recache Shortfilms', command=info_cache.rebuild_shortfilm_info_jsons).pack()
        self.update_cache_flip_ui()

    def update_cache_flip_ui(self):
        self.cache_flip.config(text='cache enabled' if settings.get('cache_enabled') else 'cache disabled')
        if settings.get('cache_enabled'):
            self.optional_cache_frame.pack()
        else:
            self.optional_cache_frame.pack_forget()

    def flip_cache(self):
        settings.set('cache_enabled', not settings.get('cache_enabled'))
        self.update_cache_flip_ui()
        
    def add_movie_folder(self):
        settings.add_movie_folder(filedialog.askdirectory(title='Select Movie Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_shortfilm_folder(self):
        settings.add_shortfilm_folder(filedialog.askdirectory(title='Select Shortfilm Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_series_folder(self):
        settings.add_series_base_folder(filedialog.askdirectory(title='Select Series Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_music_folder(self):
        settings.add_music_folder(filedialog.askdirectory(title='Select Music Base Folder'))
        self.label.config(text=str(settings.settings))

    