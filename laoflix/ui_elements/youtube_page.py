import os
from laoflix.services.card_cache import card_cache
from laoflix.ui_elements.scroll_row import HeadedScrollRow, get_random_row
from laoflix.constants import ui_sizes, ui_colors
from laoflix.ui_elements.youtube_card import YoutubeCard
from tkinter import ttk
import tkinter as tk
import random
from laoflix.ui_elements.page import Page
from loguru import logger

def identify_yt_genres(movies:list[YoutubeCard]):
    logger.debug(f'Identifying genres for {len(movies)} movies')
    genres = []
    for m in movies:
        for g in m.genres:
            if not g in genres:
                genres.append(g)
    return genres

class YoutubePage(Page):
    def __init__(self, popup_master, genre_shuffle=True, screen_width:int=None, screen_height:int=None):
        super().__init__()
        self.categories = []
        self.genre_shuffle = genre_shuffle
        self.popup_master = popup_master

        self.screen_width = screen_width

        self.genre_pos = 0
        self.y_genre_count = int((screen_height - 80) / 144) if screen_height else 4

    def set_master(self, master):

        logger.debug('Setting master for YoutubePage')
        self.youtubes:list[YoutubeCard] = card_cache.youtubes(popup_master=self.popup_master)
        genres = identify_yt_genres(self.youtubes)
        if self.genre_shuffle:
            random.shuffle(genres)
        self.genres = genres
        
        def get_score(movie: YoutubeCard):
            return movie.score or 0
        logger.debug(f'Sorting {len(self.youtubes)} movies')
        self.youtubes.sort(key=get_score, reverse=True)


        self.frame = tk.Frame(master, background=ui_colors.DEFAULT_BACKGROUND)
        self.up_button = tk.Button(self.frame, background=ui_colors.DEFAULT_BUTTON, text='Up', command=lambda: self.go_up(), foreground='white')
        self.genre_frame = tk.Frame(self.frame, background=ui_colors.DEFAULT_BACKGROUND)
        self.down_button = tk.Button(self.frame, background=ui_colors.DEFAULT_BUTTON, text='Down', command=lambda: self.go_down(), foreground='white')

        self.categories = []
        self.categories.append(
            get_random_row(
                ui_element_lambdas=[m.get_poster for m in self.youtubes],
                max_width=self.screen_width,
                master=self.genre_frame,
                height=ui_sizes.YOUTUBE_HEIGHT,
                element_width=ui_sizes.YOUTUBE_WIDTH
            )
        )
        logger.debug(f'Building {len(self.genres)} categories')
        for g in self.genres:
            self.categories.append(HeadedScrollRow(
                ui_element_lambdas=[m.get_poster for m in self.youtubes if g in m.genres],
                max_width=self.screen_width,
                master=self.genre_frame,
                title=g,
                height=ui_sizes.YOUTUBE_HEIGHT,
                element_width=ui_sizes.YOUTUBE_WIDTH
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
        logger.debug(f'Setting genres with {len(self.categories)} categories')
        if len(self.categories) < self.y_genre_count:
            for cat in self.categories:
                cat.pack(side='top', fill='x')
            return
        logger.debug(f'Setting genres from category {self.genre_pos} to {self.genre_pos + self.y_genre_count}')
        for i in range(self.genre_pos, self.genre_pos + self.y_genre_count):
            cat = self.categories[i]
            cat.pack(side='top', fill='x')

    def update_genres(self):
        logger.debug(f'Updating genres with {len(self.categories)} categories')
        for slave in self.genre_frame.pack_slaves():
            slave.pack_forget()
        self.set_genres()
        logger.debug(f'Updated genres with {len(self.categories)} categories')
