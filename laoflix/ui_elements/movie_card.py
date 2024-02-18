from PIL import Image, ImageTk
from tkinter import ttk
import xml.etree.ElementTree as ET
import os
import tkinter as tk
from datetime import date, timedelta
import random
import math
from laoflix.services import canvas_helpers
from laoflix.constants import ui_sizes
from laoflix.ui_elements.base_card import BaseCard
from laoflix.ui_elements.popup_window import PopupWindow
from laoflix.ui_elements.rating_dialog import RatingPopup

class MovieCard(BaseCard):
    POSTER_WIDTH = ui_sizes.MOVIE_WIDTH
    POSTER_HEIGHT = ui_sizes.MOVIE_HEIGHT
    def __init__(self, folder_path, movie_name, popup_master=tk.Widget):
        self.popup_master = popup_master
        self.poster_url = os.path.join(folder_path,f'{movie_name}-poster.jpg')
        self.nfo_path = os.path.join(folder_path, f'{movie_name}.nfo')
        self.video_path = f'''{os.path.join(folder_path, f'{movie_name}.mp4')}'''.replace('/','\\')
        self.interpret_nfo()
        self.score = self.calculate_score()
        self.movie_name = movie_name
    
    @property
    def poster_image(self):
        if not hasattr(self, '_poster_image'):        
            self._poster_image = None
            try:
                self._poster_image = ImageTk.PhotoImage(Image.open(self.poster_url).resize((self.POSTER_WIDTH,self.POSTER_HEIGHT)))
            except FileNotFoundError:
                print(f'No file for {self.movie_name}')
            except Exception as e:
                print(f'Exception for {self.movie_name}')
        return self._poster_image

    def interpret_nfo(self):
        try:
            xml_tree = ET.parse(self.nfo_path)
        except Exception as e:
            print(self.nfo_path)
            raise e
        xml_root = xml_tree.getroot()
        self.genres = [el.text for el in xml_root if el.tag == 'genre']
        self.titles = [el.text for el in xml_root if el.tag in ['title', 'originaltitle', 'sorttitle']]
        self.playcount = int(xml_root.find('playcount').text)
        last_played_text = xml_root.find('lastplayed').text
        try:
            y, m, d = last_played_text.split('-')
            self.lastplayed = date(int(y),int(m),int(d))
        except Exception:
            self.lastplayed = None
        try:
            self.userscore = float(xml_root.find('userrating').text)
        except:
            self.userscore = None
        try:
            ratings = [float(el.find('value'))/el.get('max') for el in xml_root.find('ratings') if el.tag == 'rating']
            self.public_rating = sum(ratings) / len(ratings)
        except:
            self.public_rating = None
        self.actor_names = [el.find('name').text for el in xml_root if el.tag == 'actor']


    def get_poster(self, master):
        poster = canvas_helpers.create_image_canvas(
            master=master,
            canvas_width=ui_sizes.MOVIE_WIDTH,
            canvas_height=ui_sizes.MOVIE_HEIGHT,
            image=self.poster_image,
            image_alt_text=self.movie_name,
            seen_validation=self.playcount,
            on_click_func=lambda ev: self.play_movie()
        )
        return poster
    
    def show_rating(self):
        popup = RatingPopup(self.popup_master, rating_call=lambda rating:self.add_user_rating(rating), marked_rating=self.userscore)
        popup.activate()
        
    def play_movie(self):
        try:
            xml_tree = ET.parse(self.nfo_path)
        except Exception as e:
            print(self.nfo_path)
            raise e
        xml_root = xml_tree.getroot()

        xml_root.find('lastplayed').text = str(date.today())
        xml_root.find('playcount').text = str(int(xml_root.find('playcount').text) + 1)

        xml_tree.write(self.nfo_path)

        self.interpret_nfo()

        self.show_rating()

        os.startfile(self.video_path)

    def add_user_rating(self, rating:int):
        try:
            xml_tree = ET.parse(self.nfo_path)
        except Exception as e:
            print(self.nfo_path)
            raise e
        xml_root = xml_tree.getroot()

        xml_root.find('userrating').text = str(rating)

        xml_tree.write(self.nfo_path)

        self.interpret_nfo()


    def calculate_score(self) -> int:
        # base score = 1000
        score = 1000

        # random range = 500
        today = date.today()
        # 100 weekly
        random.seed(f'{self.video_path}_{today.year}_{today.month}')
        score += random.randint(0, 100)

        # 100 monthly
        random.seed(f'{self.video_path}_{today.year}_{today.month}_{today.isocalendar().week}')
        score += random.randint(0, 100)

        # 300 daily
        random.seed(f'{self.video_path}_{today.year}_{today.month}_{today.isocalendar().week}_{today.isocalendar().weekday}')
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
            personal_score_factor = -1 if self.userscore < 6 else 1
            score += 10 * personal_score_factor * math.pow(2, personal_score_factor * (self.userscore - 6))

        # public score
        if self.public_rating:
        # expectation: public rating is between 0 and 1
        # 6 being average
            personal_score_factor = -1 if self.public_rating * 10 < 6 else 1
            score += 3 * personal_score_factor * math.pow(2, personal_score_factor * (self.public_rating * 10 - 6))

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
