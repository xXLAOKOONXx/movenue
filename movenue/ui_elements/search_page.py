from movenue.ui_elements.movie_card import MovieCard
from movenue.ui_elements.page import Page
from tkinter import ttk
import tkinter as tk
from movenue.constants import ui_colors

from movenue.ui_elements.series_card import SeriesCard
from movenue.services.card_cache import card_cache

class SearchPage(Page):
    def __init__(self, popup_master, screen_width:int = None):
        super().__init__()
        self.popup_master = popup_master

        self.search_results = []
        self.row_width = 5
        if screen_width:
            self.row_width = int((screen_width - 200) / 110)

    def set_master(self, master):
        self.movies = card_cache.movies(popup_master=self.popup_master)
        self.series = card_cache.series(popup_master=self.popup_master)
        self.frame = ttk.Frame(master)

        self.top_frame = tk.Frame(self.frame, background=ui_colors.DEFAULT_BACKGROUND)
        self.top_frame.pack(fill='x', side=tk.TOP)

        self.results_frame= tk.Frame(self.frame, background=ui_colors.DEFAULT_BACKGROUND)
        self.results_frame.pack(fill='x', side=tk.TOP)

        search_frame = tk.Frame(self.top_frame, background=ui_colors.DEFAULT_BACKGROUND)
        search_frame.pack()
        search_text_frame = tk.Frame(search_frame, width=300)
        search_text_frame.pack_propagate(False)
        search_text_frame.pack(side=tk.LEFT, fill='y')

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_text_frame, width=7, textvariable=self.search_var)
        self.search_entry.pack(expand=True, fill='both')
        self.search_entry.bind('<KeyPress-Return>', lambda e: self.perform_search())
        self.search_button = tk.Button(search_frame, text='Search', command = self.perform_search, background=ui_colors.DEFAULT_BUTTON, foreground='white')
        self.search_button.pack(side=tk.LEFT)
        super().set_master(master)

    def perform_search(self):
        self.refresh_search_results()
        self.refresh_results_ui()

    def refresh_search_results(self):
        # first_check = True
        def is_legit_movie(movie: MovieCard):
            search_text = self.search_var.get() 
            search_fields:list[str] = [movie.movie_name] + movie.titles + movie.genres + movie.actor_names
            return any([search_text.lower() in field.lower() for field in search_fields])
        def is_legit_series(series: SeriesCard):
            search_text = self.search_var.get()
            search_fields:list[str] = [series.series_name] + series.titles + series.genres + series.actor_names
            return any([search_text.lower() in field.lower() for field in search_fields])
        self.search_results = [m for m in card_cache.movies(popup_master=self.popup_master) if is_legit_movie(m)] + [s for s in self.series if is_legit_series(s)]

    def refresh_results_ui(self):
        for pack_slave in self.results_frame.pack_slaves():
            pack_slave.pack_forget()
        for grid_slave in self.results_frame.grid_slaves():
            grid_slave.grid_forget()
        row_idx = 0
        col_idx = 0
        for search_result in self.search_results:
            ui_element = search_result.get_poster(master=self.results_frame)
            ui_element.grid(row=row_idx,column=col_idx)
            col_idx += 1
            if col_idx >= self.row_width:
                col_idx = 0
                row_idx += 1
        if len(self.search_results) == 0:
            lbl = tk.Label(master=self.results_frame, text='No Results')
            lbl.pack(side='top')
