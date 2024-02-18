import tkinter as tk
from laoflix.services.settings import settings

from laoflix.ui_elements.page import Page
from tkinter import filedialog
from laoflix.services.info_cache import info_cache


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
        self.button_youtube = tk.Button(self.frame, text='Add Youtube folder', command=self.add_youtube_folder)
        self.button_youtube.pack()
        self.button_series = tk.Button(self.frame, text='Add Series folder', command=self.add_series_folder)
        self.button_series.pack()
        self.button_music = tk.Button(self.frame, text='Add Music folder', command=self.add_music_folder)
        self.button_music.pack()
        tk.Button(self.frame, text='Recache Music', command=info_cache.rebuild_music_info_jsons).pack()
        tk.Button(self.frame, text='Recache Youtubes', command=info_cache.rebuild_youtube_info_jsons).pack()
        
    def add_movie_folder(self):
        settings.add_movie_folder(filedialog.askdirectory(title='Select Movie Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_youtube_folder(self):
        settings.add_youtube_folder(filedialog.askdirectory(title='Select Youtube Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_series_folder(self):
        settings.add_series_base_folder(filedialog.askdirectory(title='Select Series Base Folder'))
        self.label.config(text=str(settings.settings))

    def add_music_folder(self):
        settings.add_music_folder(filedialog.askdirectory(title='Select Music Base Folder'))
        self.label.config(text=str(settings.settings))

    