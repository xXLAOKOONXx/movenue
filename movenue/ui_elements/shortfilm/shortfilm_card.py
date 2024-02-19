from PIL import Image, ImageTk
from tkinter import ttk
import os
import tkinter as tk
from datetime import date, timedelta
import random
import math
import json

from loguru import logger
from movenue.services.mp4_metadata import extract_mp4_thumbnail

from movenue.ui_elements.rating_dialog import RatingPopup
from movenue.services.info_cache import info_cache
import moviepy.editor as mp
from movenue.constants import ui_sizes

class ShortfilmCard:
    def __init__(self, folder_path, movie_name:str, popup_master:tk.Widget):
        logger.debug(f'Creating ShortfilmCard for {movie_name}')
        # TODO Add optional cached data
        self.popup_master = popup_master
        self.folder_path = folder_path
        self.poster_url = os.path.join(folder_path, f'{movie_name}.jpg')
        self.info_json_path = os.path.join(folder_path, f'{movie_name}.info.json')
        self.video_path = f'''{os.path.join(folder_path, f'{movie_name}.mp4')}'''.replace('/','\\')
        self.movie_name = movie_name
        self.interpret_nfo()
        self.score = self.calculate_score()

    @property
    def display_name(self):
        name = self.movie_name
        if 'film' in name.lower():
            if '“' in name:
                name = name.split('“')[1]
                if '”' in name:
                    return name.split('”')[0]
                name = name.split('_')[0]
                return name.strip()
            for seperator in ["'", '"']:
                s = name.split(seperator)
                if len(s) == 3:
                    return s[1]
        return name

    @property
    def poster_image(self):
        if not hasattr(self, '_poster_image'):
            logger.debug(f'Creating poster image for {self.movie_name}')
            try:
                self._poster_image = ImageTk.PhotoImage(Image.open(self.poster_url).resize((256,144)))
            except FileNotFoundError:
                logger.debug(f'No file {self.poster_url} for {self.movie_name}')
                alt_poster_image_loc = os.path.join(self.folder_path, f'{self.movie_name}.webp')
                try:
                    self._poster_image = ImageTk.PhotoImage(Image.open(alt_poster_image_loc).resize((ui_sizes.SHORTFILM_WIDTH, ui_sizes.SHORTFILM_HEIGHT)))
                    self.poster_url = alt_poster_image_loc
                except FileNotFoundError:
                    logger.warning(f'No image file for {self.movie_name}')
                    try:
                        self._poster_image = ImageTk.PhotoImage(Image.open(extract_mp4_thumbnail(self.video_path)).resize((ui_sizes.SHORTFILM_WIDTH, ui_sizes.SHORTFILM_HEIGHT)))
                    except Exception as e:
                        logger.warning(f'Failed extracting thumbnail for {self.movie_name} due to {str(e)}')

                        try:
                            video = mp.VideoFileClip(self.video_path)
                            snapshot = video.get_frame(3)  # Get the third frame of the video as a snapshot
                            self._poster_image = ImageTk.PhotoImage(Image.fromarray(snapshot).resize((ui_sizes.SHORTFILM_WIDTH, ui_sizes.SHORTFILM_HEIGHT)))
                        except Exception as e:
                            logger.info(f'Exception creating thumbnail from videoclip for {self.video_path}: {str(e)}')
            except Exception as e:
                logger.warning(f'Exception for {self.movie_name}')
            logger.debug(f'Created poster image for {self.movie_name}')
        return self._poster_image
    
    def add_user_rating(self, rating:int):
        with open(self.info_json_path, 'r') as f:
            json_tree = json.load(f)
            json_tree['userrating'] = str(rating)
        with open(self.info_json_path, 'w') as f:
            json.dump(json_tree, f)

        self.interpret_nfo()

    def show_rating(self):
        popup = RatingPopup(self.popup_master, rating_call=lambda rating:self.add_user_rating(rating), marked_rating=self.userscore)
        popup.activate()

    def interpret_nfo(self):
        logger.debug(f'Interpreting nfo for {self.movie_name}')
        # TODO Add optional cached data
        logger.debug(f'Getting info for {self.movie_name}')
        json_tree = info_cache.get_shortfilm_info_json(self.info_json_path)
        logger.debug(f'Got info for {self.movie_name}')
        self.titles = [json_tree['title']]
        def interpret_tags_to_genres(tags):
            genres = []
            for tag in tags:
                if 'science fiction' in tag:
                    genres.append('Science Fiction')
                if 'horror' in tag:
                    genres.append('Horror')
            return list(set(genres))
        logger.debug(f'Interpreting tags for {self.movie_name}')
        self.genres = interpret_tags_to_genres(json_tree.get('tags', []))
        logger.debug(f'Interpreted tags for {self.movie_name}')
        if json_tree.get('playlist_title'):
            self.genres.append(json_tree.get('playlist_title'))
        if json_tree.get('uploader'):
            self.genres.append(json_tree.get('uploader'))
        self.playcount = int(json_tree.get('playcount', 0))
        self.public_rating = None
        logger.debug(f'Setting lastplayed for {self.movie_name}')
        last_played_text = json_tree.get('lastplayed', '')
        try:
            y, m, d = last_played_text.split('-')
            self.lastplayed = date(int(y),int(m),int(d))
        except Exception:
            self.lastplayed = None
        logger.debug(f'Set lastplayed for {self.movie_name}')
        self.userscore = int(json_tree.get('userrating', 0))


    def get_poster(self, master):
        card = tk.Canvas(master, width=256, height=144, background='#9da5de', highlightthickness=0)
        card.pack_propagate(False)
        canvas = tk.Canvas(card, bg='white', highlightthickness=0) 
        canvas.pack(fill='both')
        canvas.bind('<Button-1>', lambda ev: self.play_movie())

        try:            
            canvas.create_image(128, 72, image=self.poster_image)
        except Exception:
            pass
        canvas.create_rectangle(8,5,248,25, fill='white')
        pretty_name = self.display_name
        if len(pretty_name) > 40:
            pretty_name = pretty_name[0:40] + '...'
        canvas.create_text(128, 15,text=pretty_name, width=240, fill='black', justify='left')           
        if self.playcount:
            canvas.create_polygon([226,0,256,30,256,0], fill='green')
        return card
        
    def play_movie(self):
        with open(self.info_json_path, 'r') as f:
            json_tree = json.load(f)
            json_tree['lastplayed'] = str(date.today())
            json_tree['playcount'] = str(int(json_tree.get('playcount', 0)) + 1)
        with open(self.info_json_path, 'w') as f:
            json.dump(json_tree, f)

        self.interpret_nfo()

        self.show_rating()
        os.startfile(self.video_path)

    def calculate_score(self) -> int:
        logger.debug(f'Calculating score for {self.movie_name}')
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
            personal_score_factor = -2 if self.userscore < 6 else 2
            score += personal_score_factor * math.pow(2, personal_score_factor * (self.userscore - 6))

        # public score
        if self.public_rating:
        # expectation: public rating is between 0 and 1
        # 6 being average
            personal_score_factor = -1 if self.public_rating * 10 < 6 else 1
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
