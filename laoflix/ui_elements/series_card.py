from typing import Callable
from PIL import Image, ImageTk
from tkinter import ttk
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from tkinter import font
from datetime import date, timedelta
import random
import math
from laoflix.services.icons import icons

from laoflix.data_structures.episode import Episode
from laoflix.ui_elements.base_card import BaseCard
from laoflix.ui_elements.scroll_row import ScrollRow
from laoflix.services import canvas_helpers
from laoflix.constants import ui_sizes, ui_colors

class SeriesCard(BaseCard):
    def __init__(self, folder_path, series_folder_name, popup_frame: tk.Frame):
        self.popup_frame = popup_frame
        self.series_full_path = os.path.join(folder_path, series_folder_name)
        self.poster_url = os.path.join(self.series_full_path, 'poster.jpg')
        self.nfo_path = os.path.join(self.series_full_path, 'tvshow.nfo')
        self.video_path = self.series_full_path # TODO Fix
        self.series_name = series_folder_name
        self.interpret_nfo()
        self.score = self.calculate_score()
        self.poster_image = None
        try:
            self.poster_image = ImageTk.PhotoImage(Image.open(self.poster_url).resize((ui_sizes.SEASON_WIDTH, ui_sizes.SERIES_HEIGHT)))
        except FileNotFoundError:
            print(f'No file for {series_folder_name}')
        except Exception as e:
            print(f'Exception for {series_folder_name}: {e}')
        self._episodes = {}
        self._season_posters = {}
        self.current_season = None

    def interpret_nfo(self):
        try:
            xml_tree = ET.parse(self.nfo_path)
        except Exception as e:
            print(self.nfo_path)
            raise e
        xml_root = xml_tree.getroot()
        self.genres = [el.text for el in xml_root if el.tag == 'genre']
        self.titles = [el.text for el in xml_root if el.tag in ['title', 'originaltitle', 'sorttitle']]
        self.playcount = int(xml_root.find('playcount').text) if xml_root.find('playcount') else 0
        last_played_text = xml_root.find('lastplayed').text if xml_root.find('lastplayed') is not None else None
        try:
            y, m, d = last_played_text.split('-')
            self.lastplayed = date(int(y),int(m),int(d))
        except Exception as ex:
            self.lastplayed = None
        try:
            self.userscore = float(xml_root.find('userscore').text)
        except:
            self.userscore = None
        try:
            ratings = [float(el.find('value'))/el.get('max') for el in xml_root.find('ratings') if el.tag == 'rating']
            self.public_rating = sum(ratings) / len(ratings)
        except:
            self.public_rating = None
        self.actor_names = [el.find('name').text for el in xml_root if el.tag == 'actor']


    def get_poster(self, master):
        # card = tk.Canvas(master, width=100, height=200, background='#9da5de', highlightthickness=0)
        # card.pack_propagate(False)

        canvas = canvas_helpers.create_image_canvas(
            master=master,
            canvas_width=ui_sizes.SERIES_WIDTH,
            canvas_height=ui_sizes.SEASON_HEIGHT,
            image=self.poster_image,
            image_alt_text=self.series_name,
            on_click_func=lambda ev: self.poster_click()
        )
        # canvas.pack(fill='both')
        return canvas
    
    def get_season_folder_path(self, no: int):
        return os.path.join(self.series_full_path, f'S{no:02}')
    
    def get_season_poster_path(self, no: int):
        if no > 100:
            path = os.path.join(self.series_full_path, f'season{int(no/100):02}-poster.jpg')
            if os.path.exists(path):
                return path
        return os.path.join(self.series_full_path, f'season{no:02}-poster.jpg')
    
    def get_seasons(self) -> list[int]:
        seasons = []
        subdirs = [name for name in os.listdir(self.series_full_path)
            if os.path.isdir(os.path.join(self.series_full_path, name))]
        for subdir in subdirs:
            if subdir != '.actors':
                no = int(subdir.strip('S'))
                seasons.append(no)
        return seasons
    
    def get_episodes(self, season_no):
        if season_no in self._episodes.keys():
            return self._episodes[season_no]
        episodes = [Episode(os.path.join(self.get_season_folder_path(season_no), name), self.nfo_path) for name in os.listdir(self.get_season_folder_path(season_no)) if name.endswith('.nfo')]
        def get_episode_no(ep: Episode):
            return ep.episode_no
        episodes.sort(key=get_episode_no, reverse=False)
        self._episodes[season_no] = episodes
        return episodes
        
    def build_canvas(self, master:tk.Widget, ep:Episode) -> tk.Widget:
        canvas = canvas_helpers.create_image_canvas(
            master=master,
            canvas_width=ui_sizes.EPISODE_WIDTH,
            canvas_height=ui_sizes.EPISODE_HEIGHT,
            image=ep.poster_image,
            bottom_text=f'Episode {ep.episode_no}',
            seen_validation=ep.playcount,
            on_click_func=lambda ev: ep.play_episode()
        )
        return canvas
    
    def start_random(self):
        l:list[Episode] = []
        for season_no in self.get_seasons():
            eps = self.get_episodes(season_no)
            if eps:
                l += eps
        random.sample(l,1)[0].play_episode()

    def start_random_unseen(self):
        l:list[Episode] = []
        for season_no in self.get_seasons():
            eps = [ep for ep in self.get_episodes(season_no) if ep.playcount == 0 or ep.playcount is None]
            if eps:
                l += eps
        random.sample(l,1)[0].play_episode()
    
    def start_random_from_season(self):
        if self.current_season:
            random.sample(self.get_episodes(self.current_season),1)[0].play_episode()

    def set_current_season(self, season_no):
        self.current_season = season_no
    
    def get_popup_content(self):
        popup_content = tk.Frame(self.popup_frame, background=ui_colors.DEFAULT_BACKGROUND, highlightthickness=0)
        popup_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        popup_head_frame = tk.Frame(popup_content, background=ui_colors.DEFAULT_BACKGROUND)
        popup_head_frame.pack(side='top', fill='x')
        def close_popup():
            popup_content.place_forget()
        exit_btn = tk.Button(popup_head_frame, text='back', padx=20, background=ui_colors.DEFAULT_BUTTON, foreground='white', command=close_popup)
        exit_btn.pack(side='left', padx=10, pady=10)

        lbl = tk.Label(popup_head_frame, text=self.series_name, background=ui_colors.DEFAULT_BACKGROUND, foreground='black', font=font.Font(family='Arial', size=25))
        lbl.pack(side='top', padx=10, pady=10)

        popup_body_frame = tk.Frame(popup_content, background=ui_colors.DEFAULT_BACKGROUND)
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
        random_eps = tk.Label(master=popup_bottom_row, text='Random Episode from Season', background=ui_colors.DEFAULT_BUTTON, foreground='white')
        random_eps.bind('<Button-1>', lambda ev: self.start_random_from_season())
        random_eps.grid(column=1, row=0, padx=10, pady=10, ipadx=10, ipady=10)
        random_eps = tk.Label(master=popup_bottom_row, text='Random unseen Episode', background=ui_colors.DEFAULT_BUTTON, foreground='white')
        random_eps.bind('<Button-1>', lambda ev: self.start_random_unseen())
        random_eps.grid(column=2, row=0, padx=10, pady=10, ipadx=10, ipady=10)
        # EPS
        def add_eps(season_no):
            self.set_current_season(season_no)
            for p in popup_episodes_row.pack_slaves():
                p.pack_forget()
            eps = self.get_episodes(season_no)
            canvas_list = [lambda master, c=e: self.build_canvas(master, c) for e in eps]
            sr = ScrollRow(canvas_list, master=popup_episodes_row, max_width=popup_content.winfo_screenwidth() - 20, height=ui_sizes.EPISODE_HEIGHT, element_width=ui_sizes.EPISODE_WIDTH)
            sr.frame.pack(side='top')

            return
        # SEASON
        def get_season_canvas(season_no, master) -> tk.Canvas:
            try:
                img = ImageTk.PhotoImage(Image.open(self.get_season_poster_path(season_no)).resize((ui_sizes.SEASON_WIDTH, ui_sizes.SEASON_HEIGHT)))
                self._season_posters[season_no] = img
            except Exception as ex:
                img = None
                print(ex)
            
            eps = self.get_episodes(season_no)
            canvas = canvas_helpers.create_image_canvas(
                master=master,
                canvas_height=ui_sizes.SEASON_HEIGHT,
                canvas_width=ui_sizes.SEASON_WIDTH,
                image=img,
                image_alt_text=f'Season {season_no}',
                seen_validation=all([ep.playcount for ep in eps]),
                on_click_func=lambda ev, season_no=season_no: add_eps(season_no)
            )
            canvas_helpers.add_started_tag(
                canvas=canvas,
                canvas_width=ui_sizes.SEASON_WIDTH,
                validation=eps and any([ep.playcount for ep in eps]) and not all([ep.playcount for ep in eps])
            )
            canvas_helpers.add_error_tag(
                canvas=canvas,
                canvas_width=ui_sizes.SEASON_WIDTH,
                validation=not eps
            )
            return canvas
        
        sr = ScrollRow(
            ui_element_lambdas=[lambda master, season_no=season_no: get_season_canvas(season_no, master) for season_no in self.get_seasons()],
            master=popup_season_row,
            max_width=popup_content.winfo_screenwidth() - 20,
            element_width=ui_sizes.SEASON_WIDTH,
            height=ui_sizes.SEASON_HEIGHT
        )
        sr.frame.pack(side='top')
    
    def poster_click(self):
        self.get_popup_content()
        
        # canvas = tk.Canvas(self.popup_frame, bg='white', highlightthickness=0, width=400, height=200) 
        # canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
        return


    def calculate_score(self) -> int:
        # base score = 1000
        score = 1000

        # random range = 500
        today = date.today()
        # 100 weekly
        random.seed(f'{self.series_full_path}_{today.year}_{today.month}')
        score += random.randint(0, 100)

        # 100 monthly
        random.seed(f'{self.series_full_path}_{today.year}_{today.month}_{today.isocalendar().week}')
        score += random.randint(0, 100)

        # 300 daily
        random.seed(f'{self.series_full_path}_{today.year}_{today.month}_{today.isocalendar().week}_{today.isocalendar().weekday}')
        score += random.randint(0, 300)

        # reset seed
        random.seed()

        # recency watched
        # today = -1000
        # yesterday = -500
        # this week = -300
        # this month = -200
        # this year = -100
        # two years ago = -50
        # five years ago = -10
        if self.lastplayed:
            time_past = today - self.lastplayed
            if time_past <= timedelta(days=0):
                score += -1000
            if time_past <= timedelta(days=1):
                score += -500
            if time_past <= timedelta(weeks=1):
                score += -300
            if time_past <= timedelta(days=30):
                score += -200
            if time_past <= timedelta(days=360):
                score += -100
            if time_past <= timedelta(days=720):
                score += -50
            if time_past <= timedelta(days=1800):
                score += -10

        # private score
        if self.userscore:
        # expectation: userscore from 0-10
        # 6 being average
            personal_score_factor = -10 if self.userscore < 6 else 10
            score += personal_score_factor * math.pow(2, personal_score_factor * (self.userscore - 6))

        # public score
        if self.public_rating:
        # expectation: public rating is between 0 and 1
        # 6 being average
            personal_score_factor = -3 if self.public_rating * 10 < 6 else 3
            score += personal_score_factor * math.pow(2, personal_score_factor * (self.public_rating * 10 - 6))

        # multi-watched
        # watched once: +10
        # watched twice: +30
        # watched 3-5: +60
        # watched 6-10: +150
        # watched 10+: 150 + watched-10 x 5
        if self.playcount:
            if self.playcount == 1:
                score += 10
            elif self.playcount <= 2:
                score += 30
            elif self.playcount <= 5:
                score += 60
            elif self.playcount <= 10:
                score += 150
            else:
                score += 150 + (self.playcount * 5)

        return score
