import tkinter as tk
import os

from loguru import logger
from movenue.services.mp4_metadata import extract_mp4_metadata
from movenue.services.create_xspf import build_xml_playlist, default_playlist_location, PlaylistItem, weight_playlist_items
from movenue.ui_elements.music.music_filter import MusicFilter
from movenue.ui_elements.page import Page
from movenue.ui_elements.music.music_card import MusicCard
from movenue.constants import ui_sizes
from tkinter import filedialog

class MusicPage(Page):
  def __init__(self, popup_frame: tk.Widget, folder_paths=[], screen_width=None, screen_height=None):
    super().__init__()
    self.popup_frame = popup_frame
    self.folder_paths = folder_paths
    self.music_cards = []
    self.filtered_music_cards = []
    self.filters:list[MusicFilter] = []
    self.row_width = 5
    if screen_width:
        self.row_width = int((screen_width - 200) / ui_sizes.SHORTFILM_WIDTH)
    self.row_count = 5
    if screen_height:
        self.row_count = int((screen_height - 200) / ui_sizes.SHORTFILM_HEIGHT)
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.min_userrating = tk.StringVar()
    self.search_string = tk.StringVar()
    self.weight_playlist_active = tk.IntVar()

  def set_master(self, master: tk.Widget):
    super().set_master(master)
    self.frame = tk.Frame(master)

    # Create the first frame
    self.filter_frame = tk.Frame(self.frame)
    self.filter_frame.pack()

    # Create the second frame
    self.frame2 = tk.Frame(self.frame)
    self.frame2.pack()

    # Create the third frame
    self.cards_frame = tk.Frame(self.frame)
    self.cards_frame.pack()

    # Create the create xsfp file button
    self.weight_playlist_toggle = tk.Checkbutton(self.frame2, text="Apply weighting", variable=self.weight_playlist_active)
    self.weight_playlist_toggle.pack()
    self.create_xsfp_button = tk.Button(self.frame2, text="Run Playlist", command=self.start_playlist)
    self.create_xsfp_button.pack()
    self.save_xsfp_button = tk.Button(self.frame2, text="Save Playlist", command=self.save_playlist)
    self.save_xsfp_button.pack()

    self.update_music_cards()
    self.update_available_tags()
    self.update_filtered_music_cards()
    self.build_filter_elements()
    self.refresh_cards()

  def start_playlist(self):
    # Get the filtered mp4 files
    filtered_files = [PlaylistItem(card.video_path, music_start=card.music_start, music_end=card.music_end, score=card.metadata.get('userrating')) for card in self.filtered_music_cards]

    if self.weight_playlist_active:
      filtered_files = weight_playlist_items(filtered_files)

    # Create the xsfp file
    build_xml_playlist(filtered_files)

    os.startfile(default_playlist_location())

  def save_playlist(self):
    target_location = filedialog.asksaveasfilename(defaultextension='.xspf', filetypes=[('XSPF files', '*.xspf')])
    if not target_location:
      return

    # Get the filtered mp4 files
    filtered_files = [PlaylistItem(card.video_path, music_start=card.music_start, music_end=card.music_end, score=card.metadata.get('userrating')) for card in self.filtered_music_cards]

    if self.weight_playlist_active:
      filtered_files = weight_playlist_items(filtered_files)

    # Create the xsfp file
    build_xml_playlist(filtered_files, target_location=target_location)
     

  def update_music_cards(self):
    logger.debug(f'Updating music cards')
    self.music_cards:list[MusicCard] = []
    for folder_path in self.folder_paths:
      for root, dirs, files in os.walk(folder_path):
        for file in files:
          if file.endswith('.mp4') or file.endswith('.mp3'):
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
    filters_frame = tk.Frame(self.filter_frame)
    filters_frame.pack()
    def add_filter():
      filter = MusicFilter()
      self.filters.append(filter)
      filter.get_ui_element(filters_frame, self.available_tags).pack()
    tk.Button(self.filter_frame, text='Add Filter', command=add_filter).pack()
    tk.Button(self.filter_frame, text='Apply Filters', command=self.apply_update_and_refresh_cards).pack()

  def apply_update_and_refresh_cards(self):
    self.update_filtered_music_cards()
    self.refresh_cards()

  def update_filtered_music_cards(self):
    logger.debug(f'Updating filtered music cards')
    if not self.filters:
      self.filtered_music_cards = self.music_cards
    else:
      self.filtered_music_cards = [card for card in self.music_cards if any(filter.passes_filter(card) for filter in self.filters)]



# Filtering:
# n Filtergroups
# options in filtergroup:
# - at least one of the following tags []
# - minimum user rating
# - search string
# - minimum duration in s
# - maximum duration in s
# - interpret
