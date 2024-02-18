import tkinter as tk
import os

from loguru import logger
from laoflix.services.mp4_metadata import extract_mp4_metadata
from laoflix.services.create_xsfp import build_xml_playlist, default_playlist_location
from laoflix.ui_elements.page import Page
from laoflix.ui_elements.music.music_card import MusicCard
from laoflix.constants import ui_sizes

class MusicPage(Page):
  def __init__(self, popup_frame: tk.Widget, folder_paths=['//mynas/Daten/Musik/Videos'], screen_width=None, screen_height=None):
    super().__init__()
    self.popup_frame = popup_frame
    self.folder_paths = folder_paths
    self.music_cards = []
    self.filtered_music_cards = []
    self.filters = []
    self.row_width = 5
    if screen_width:
        self.row_width = int((screen_width - 200) / ui_sizes.YOUTUBE_WIDTH)
    self.row_count = 5
    if screen_height:
        self.row_count = int((screen_height - 200) / ui_sizes.YOUTUBE_HEIGHT)
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.min_userrating = tk.StringVar()
    self.search_string = tk.StringVar()

  def set_master(self, master: tk.Widget):
    super().set_master(master)
    self.frame = tk.Frame(master)

    # Create the first frame
    self.frame1 = tk.Frame(self.frame)
    self.frame1.pack()

    # Create the second frame
    self.frame2 = tk.Frame(self.frame)
    self.frame2.pack()

    # Create the third frame
    self.cards_frame = tk.Frame(self.frame)
    self.cards_frame.pack()

    # Create the create xsfp file button
    self.create_xsfp_button = tk.Button(self.frame2, text="Run Playlist", command=self.start_playlist)
    self.create_xsfp_button.pack()

    self.update_music_cards()
    self.update_available_tags()
    self.update_filtered_music_cards()
    self.build_filter_elements()
    self.refresh_cards()

  def start_playlist(self):
    # Get the filtered mp4 files
    filtered_files = [card.video_path for card in self.filtered_music_cards]

    # Create the xsfp file
    build_xml_playlist(filtered_files)

    os.startfile(default_playlist_location())

  def update_music_cards(self):
    logger.debug(f'Updating music cards')
    self.music_cards:list[MusicCard] = []
    for folder_path in self.folder_paths:
      for root, dirs, files in os.walk(folder_path):
        for file in files:
          if file.endswith('.mp4'):
            self.music_cards.append(MusicCard(os.path.join(root, file), self.popup_frame, screen_height=self.screen_height, screen_width=self.screen_width))

  def refresh_cards(self):
    # Clear the existing cards  
    logger.debug(f'Refreshing music cards')    
    for pack_slave in self.cards_frame.pack_slaves():
        pack_slave.pack_forget()
    for grid_slave in self.cards_frame.grid_slaves():
        grid_slave.grid_forget()
    row_idx = 0
    col_idx = 0
    for card in self.filtered_music_cards:
        ui_element = card.get_poster(master=self.cards_frame)
        ui_element.grid(row=row_idx,column=col_idx)
        col_idx += 1
        if col_idx >= self.row_width:
            col_idx = 0
            row_idx += 1
        if row_idx > self.row_count:
            break
    if len(self.filtered_music_cards) == 0:
        lbl = tk.Label(master=self.cards_frame, text='No Results')
        lbl.pack(side='top')

  def update_available_tags(self):
      logger.debug(f'Updating available tags')

      # Get all unique tags from mp4 files
      tags = set()
      for card in self.music_cards:
        file_tags = card.metadata.get('tags', [])
        tags.update(file_tags)
      tags.update(['None'])
      self.available_tags = list(tags)

  def build_filter_elements(self):
      logger.debug(f'Building clickable tags')
      # Clear the existing widgets in frame1
      for widget in self.frame1.winfo_children():
        widget.destroy()
      tags_frame = tk.Frame(self.frame1)
      tags_frame.pack(side='top')
      # Create clickable widgets for each tag
      for tag in self.available_tags:
        if tag in self.filters:
          widget = tk.Button(tags_frame, text=tag, command=lambda t=tag: self.remove_filter(t), foreground='white', background='black')
          widget.pack(side='left')
        else:
          widget = tk.Button(tags_frame, text=tag, command=lambda t=tag: self.add_filter(t))
          widget.pack(side='left')
      min_rating_frame = tk.Frame(self.frame1)
      min_rating_frame.pack(side='top')
      lbl = tk.Label(min_rating_frame, text='Min User Rating:')
      lbl.pack(side='left')
      min_entry = tk.Entry(min_rating_frame, textvariable=self.min_userrating)
      min_entry.pack(side='left')

      search_frame = tk.Frame(self.frame1)
      search_frame.pack(side='top')
      lbl = tk.Label(search_frame, text='Search:')
      lbl.pack(side='left')
      search_entry = tk.Entry(search_frame, textvariable=self.search_string)
      search_entry.pack(side='left')

      refresh_frame = tk.Frame(self.frame1)
      refresh_frame.pack(side='top')
      refresh_button = tk.Button(refresh_frame, text='Refresh', command=self.apply_update_and_refresh_cards)
      refresh_button.pack(side='left')

  def apply_update_and_refresh_cards(self):
    self.update_filtered_music_cards()
    self.refresh_cards()

  def update_filtered_music_cards(self):
    logger.debug(f'Updating filtered music cards')
    if not self.filters and not self.min_userrating.get() and not self.search_string.get():
      self.filtered_music_cards = self.music_cards
    else:
      self.filtered_music_cards = [card for card in self.music_cards if self.is_filtered(card)]

  def is_filtered(self, card):
    return self.is_in_tag_filter(card) and self.is_in_rating_filter(card) and self.is_in_search_filter(card)

  def is_in_tag_filter(self, card:MusicCard):
    if not self.filters:
      return True
    if 'None' in self.filters and not card.metadata.get('tags', []):
      return True
    return any(tag in card.metadata.get('tags', []) for tag in self.filters)
  
  def is_in_rating_filter(self, card:MusicCard):
    if not self.min_userrating.get():
      return True
    try:
      return card.metadata.get('userrating',0) >= int(self.min_userrating.get())
    except:
      return False
    
  def is_in_search_filter(self, card:MusicCard):
    if not self.search_string.get():
      return True
    return self.search_string.get().lower() in card.video_name.lower()

  def remove_filter(self, tag):
    # Remove the tag from the list of filters
    self.filters.remove(tag)
    self.update_filtered_music_cards()
    self.refresh_cards()
    self.build_filter_elements()

  def add_filter(self, tag):
    # Add the tag to the list of filters
    self.filters.append(tag)
    self.update_filtered_music_cards()
    self.refresh_cards()
    self.build_filter_elements()

