import tkinter as tk
from tkinter import ttk
import os
from movenue.ui_elements.movie_card import MovieCard
from movenue.ui_elements.movie_page import MoviePage
from movenue.ui_elements.music.music_page import MusicPage
from movenue.ui_elements.series_card import SeriesCard
from movenue.ui_elements.series_page import SeriesPage
from movenue.ui_elements.settings.settings_page import SettingsPage
from movenue.ui_elements.shortfilm.shortfilm_page import ShortfilmPage
from movenue.ui_elements.page import Page
from movenue.ui_elements.search_page import SearchPage
from movenue.constants import ui_colors
from movenue.services.settings import settings
from movenue.services.icons import get_app_icon_path

def perform_search(search_text, display_var: tk.StringVar):
    display_var.set(search_text.get())

def identify_genres(movies:list[MovieCard]):
    genres = []
    for m in movies:
        for g in m.genres:
            if not g in genres:
                genres.append(g)
    return genres

def identify_series_genres(movies:list[SeriesCard]):
    genres = []
    for m in movies:
        for g in m.genres:
            if not g in genres:
                genres.append(g)
    return genres

class MainWindow:
    
    def __init__(self, movie_folders=settings.movie_folders, shortfilm_folders = settings.shortfilm_folders, series_base_folders = settings.series_base_folders, music_folders = settings.music_folders):
        self.pages = []
        self.window = tk.Tk()
        self.window.iconbitmap(get_app_icon_path())
        self.window.configure(background=ui_colors.DEFAULT_BACKGROUND)
        self.window.attributes('-fullscreen', True)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.header_frame = tk.Frame(self.window, background=ui_colors.TOP_MENU_BACKGROUND)
        self.header_frame.pack(side=tk.TOP, fill='x')

        self.body_frame = tk.Frame(self.window, background=ui_colors.DEFAULT_BACKGROUND)
        self.body_frame.pack(side=tk.TOP, expand=True, fill='both')

        self.window.title('Movenue')

        self.movie_page = MoviePage(popup_master=self.body_frame, screen_width=screen_width, screen_height=screen_height)
        # self.movie_page.set_master(self.body_frame)
        self.search_page = SearchPage(popup_master=self.body_frame, screen_width=screen_width)
        # self.search_page.set_master(self.body_frame)
        self.shortfilm_page = ShortfilmPage(popup_master=self.body_frame, screen_width=screen_width, screen_height=screen_height)
        # self.shortfilm_page.set_master(self.body_frame)
        self.series_page = SeriesPage(popup_master=self.body_frame, screen_width=screen_width, screen_height=screen_height)
        # self.series_page.set_master(self.body_frame)
        self.music_page = MusicPage(popup_frame=self.body_frame, screen_width=screen_width, screen_height=screen_height, folder_paths=music_folders)
        self.settings_page = SettingsPage()

        def set_page(page:Page, master:tk.Widget):
            for pack_slave in master.pack_slaves():
                pack_slave.pack_forget()
            for loc_slave in master.place_slaves():
                loc_slave.place_forget()
            
            if not page.master_is_set:
                loading = tk.Label(master, text='Setting up...')
                loading.pack()
                master.update_idletasks()
                page.set_master(master)
                loading.pack_forget()
            page.get_ui_element().pack()

        movie_btn = tk.Button(self.header_frame, text='Filme', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.movie_page, self.body_frame))
        movie_btn.pack(side='left')
        search_btn = tk.Button(self.header_frame, text='Suche', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.search_page, self.body_frame))
        search_btn.pack(side='left')
        shortfilm_btn = tk.Button(self.header_frame, text='Shortfilms', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.shortfilm_page, self.body_frame))
        shortfilm_btn.pack(side='left')
        series_btn = tk.Button(self.header_frame, text='Series', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.series_page, self.body_frame))
        series_btn.pack(side='left')
        series_btn = tk.Button(self.header_frame, text='Music', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.music_page, self.body_frame))
        series_btn.pack(side='left')
        exit_btn = tk.Button(self.header_frame, text='Exit', padx=20, background=ui_colors.EXIT_BUTTON_COLOR, foreground='white', command=self.window.destroy)
        exit_btn.pack(side='right')
        settings_btn = tk.Button(self.header_frame, text='Settings', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.settings_page, self.body_frame))
        settings_btn.pack(side='right')

        self.window.bind('<Escape>', lambda e: self.window.destroy())


    def run(self):
        self.window.mainloop()