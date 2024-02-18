import io
import os
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
from laoflix.constants import ui_sizes
from laoflix.services.mp4_metadata import add_tag_to_mp4, extract_mp4_thumbnail
from laoflix.ui_elements.base_card import BaseCard
from laoflix.services import canvas_helpers
from laoflix.ui_elements.popup_window import PopupWindow
import moviepy.editor as mp
from loguru import logger
from laoflix.services.info_cache import info_cache
from laoflix.services.image_cache import image_cache

class MusicCard(BaseCard):
    THUMBNAIL_WIDTH = ui_sizes.YOUTUBE_WIDTH
    THUMBNAIL_HEIGHT = ui_sizes.YOUTUBE_HEIGHT

    def __init__(self, full_video_path, popup_master=tk.Widget, screen_height=None, screen_width=None):
        logger.debug(f'Creating music card for {full_video_path}')
        self.popup_master = popup_master
        self.video_path = f'{full_video_path}'.replace('/','\\')
        self.metadata = info_cache.get_music_info_json(self.video_path)
        self.video_name = full_video_path.split('\\')[-1]
        self.screen_height = screen_height
        self.screen_width = screen_width
        logger.debug(f'Created music card for {full_video_path}')

    @property
    def thumbnail_image(self):
        if not hasattr(self, '_thumbnail_image') or self._thumbnail_image is None:
            self._thumbnail_image = None
            try:
                self._thumbnail_image = ImageTk.PhotoImage(image_cache.get_music_image(self.video_path))
            except Exception as e:
                logger.debug(f'Exception getting thumbnail for {self.video_name}: {str(e)}')
        return self._thumbnail_image
    
    def get_poster(self, master):
        logger.debug(f'Creating poster for {self.video_name}')
        poster = canvas_helpers.create_image_canvas(
            master=master,
            canvas_width=ui_sizes.YOUTUBE_WIDTH,
            canvas_height=ui_sizes.YOUTUBE_HEIGHT,
            image=self.thumbnail_image,
            image_alt_text=self.video_name,
            on_click_func=lambda ev: self.open_popup(),
            bottom_text=self.video_name.replace('.mp4', ''),
        )
        logger.debug(f'Created poster for {self.video_name}')
        return poster
    
    @property
    def popup_window(self):
        if not hasattr(self, '_popup_window') or self._popup_window is None:
            self._popup_window = PopupWindow(master=self.popup_master, content_lambda=lambda master: self.get_popup_content(master))
        return self._popup_window
    
    def open_popup(self):
        self.popup_window.activate()
    
    def get_popup_content(self, master):
        content = tk.Frame(master,)# height=(self.screen_height or 1000)-200, width=(self.screen_width or 1000)-200)

        frame1 = tk.Frame(content)
        frame1.pack()
        for tag in self.metadata.get('tags', []):
            ttk.Label(frame1, text=tag).pack()

        frame2 = tk.Frame(content)
        frame2.pack()
        for key, value in self.metadata.items():
            if key == 'thumbnail':
                continue
            ttk.Label(frame2, text=f'{key}: {value}').pack()

        frame3 = tk.Frame(content)
        frame3.pack()
        self.tag_var = tk.StringVar()
        self.tag_entry = ttk.Entry(frame3, width=25, textvariable=self.tag_var)
        self.tag_entry.pack(side='left')
        tk.Button(frame3, text='Add Tag', command=lambda: self.add_tag()).pack(side='left')

        frame4 = tk.Frame(content)
        frame4.pack()
        tk.Button(frame4, text='Play', command=lambda: self.play_file()).pack()

        return content
    
    def add_tag(self):
        tag = self.tag_var.get()
        if tag:
            add_tag_to_mp4(self.video_path, tag)
            self.metadata = info_cache.get_music_info_json(self.video_path, refresh=True)
            self.tag_var.set('')

    def play_file(self):
        os.startfile(self.video_path)
    
    def calculate_score(self):
        return 0