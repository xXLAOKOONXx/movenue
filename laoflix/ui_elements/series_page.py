from datetime import date
from laoflix.ui_elements.scroll_row import HeadedScrollRow, get_random_row
from laoflix.constants import ui_sizes, ui_colors
from laoflix.ui_elements.series_card import SeriesCard
from tkinter import ttk
import tkinter as tk
import random
from laoflix.ui_elements.page import Page
from laoflix.services.card_cache import card_cache


def identify_series_genres(movies:list[SeriesCard]):
    genres = []
    for m in movies:
        for g in m.genres:
            if not g in genres:
                genres.append(g)
    return genres

class SeriesPage(Page):
    def __init__(self, popup_master, genre_shuffle=True, screen_width:int=None, screen_height:int=None):
        super().__init__()
        self.genre_shuffle = genre_shuffle
        self.popup_master = popup_master
        self.screen_width = screen_width
        self.genre_pos = 0
        self.y_genre_count = int((screen_height - 80) / 240) if screen_height else 4

    def set_master(self, master):    
        self.movies = card_cache.series(popup_master=self.popup_master)
        self.genres = identify_series_genres(self.movies)
        if self.genre_shuffle:
            random.shuffle(self.genres)
        def get_score(movie: SeriesCard):
            return movie.score or 0
        self.movies.sort(key=get_score, reverse=True)

        self.frame = tk.Frame(master, background=ui_colors.DEFAULT_BACKGROUND)
        self.up_button = tk.Button(self.frame, background=ui_colors.DEFAULT_BUTTON, text='Up', command=lambda: self.go_up(), foreground='white')
        self.genre_frame = tk.Frame(self.frame, background=ui_colors.DEFAULT_BACKGROUND)
        self.down_button = tk.Button(self.frame, background=ui_colors.DEFAULT_BUTTON, text='Down', command=lambda: self.go_down(), foreground='white')

        self.categories = []

        recent_watched = self.movies
        def get_recency(movie: SeriesCard):
            return movie.lastplayed or date.min
        recent_watched.sort(key=get_recency, reverse=True)
        recent_watched = [m.get_poster for m in recent_watched if m.lastplayed is not None][:10]
        if recent_watched:
            self.categories.append(HeadedScrollRow(
                title='Last Watched',
                ui_element_lambdas=recent_watched,
                max_width=self.screen_width,
                master=self.genre_frame,
                height=ui_sizes.SERIES_HEIGHT,
                element_width=ui_sizes.SERIES_WIDTH
            ))

        self.categories.append(
            get_random_row(
                ui_element_lambdas=[m.get_poster for m in self.movies],
                max_width=self.screen_width,
                master=self.genre_frame,
                height=ui_sizes.SERIES_HEIGHT,
                element_width=ui_sizes.SERIES_WIDTH
            )
        )
        for g in self.genres:
            self.categories.append(HeadedScrollRow(
                ui_element_lambdas=[m.get_poster for m in self.movies if g in m.genres],
                max_width=self.screen_width,
                master=self.genre_frame,
                title=g,
                height=ui_sizes.SERIES_HEIGHT,
                element_width=ui_sizes.SERIES_WIDTH
            ))

        self.up_button.pack(ipadx=20, ipady=10, pady=4)
        self.genre_frame.pack()
        self.down_button.pack(ipadx=20, ipady=10, pady=4)
        self.update_genres()
        super().set_master(master)

    def go_down(self):
        if self.genre_pos + self.y_genre_count < len(self.categories):
            self.genre_pos = self.genre_pos + 1
            self.update_genres()

    def go_up(self):
        if self.genre_pos > 0:
            self.genre_pos = self.genre_pos - 1
            self.update_genres()

    def set_genres(self):
        if len(self.categories) < self.y_genre_count:
            for cat in self.categories:
                cat.pack(side='top', fill='x')
            return
        for i in range(self.genre_pos, self.genre_pos + self.y_genre_count):
            cat = self.categories[i]
            cat.pack(side='top', fill='x')

    def update_genres(self):
        for slave in self.genre_frame.pack_slaves():
            slave.pack_forget()
        self.set_genres()


        

    # def sort_by_priority(movies:list[MovieCard]) -> list[MovieCard]:
    #     unseen_movies = [m for m in movies if not m.playcount]
    #     seen_movies = [m for m in movies if m.playcount]

    # def score_movie(movie: MovieCard):
    #     movie_seen = movie.playcount > 0
    #     movie_seen_often = movie.playcount > 3
    #     seen_this_week = movie.lastplayed and movie.