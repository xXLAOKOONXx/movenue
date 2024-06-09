import math
import os
import tkinter as tk
from tkinter import ttk
from typing import Callable
from PIL import ImageTk

from movenue.models.collection import Collection
from movenue.models.playable import Playable
from movenue.models.storage import Storage
from movenue.services import add_infos
from movenue.services.play import play_playable
from movenue.ui.services import canvas_helpers
from movenue.ui.services.tk_sizes import get_width


def playable_popup(playable: Playable, collection: Collection |None=None, storage:Storage|None=None) -> Callable[[tk.Widget], tk.Widget]:
    def popup_content(master: tk.Widget, **kwargs) -> tk.Widget:
        content = tk.Frame(master)

        title = tk.Label(content, text=playable.title, font=('TkDefaultFont', 20))
        title.pack()

        if playable.poster_image:
          height = 200
          poster_frame = tk.Frame(content)
          poster_frame.pack()
          calc_width = math.floor(playable.poster_image.width * height / playable.poster_image.height)
          img = playable.tkimages.get((calc_width, height))
          if img is None:
            i = playable.poster_image.resize((calc_width, height))
            img = ImageTk.PhotoImage(i)
            playable.tkimages[(calc_width, height)] = img

          poster = canvas_helpers.create_image_canvas(
              master=poster_frame,
              canvas_width=calc_width,
              canvas_height=height,
              image=img,
              image_alt_text='Error displaying Poster',
              on_click_func=None,
              bottom_text=None,
          )
          poster.pack()
           
        if playable.artists:
          artists = tk.Label(content, text=', '.join(playable.artists[:10]), wraplength=get_width(master) / 2 - 20, justify='left')
          artists.pack()
        if playable.playcount:
          playcount = tk.Label(content, text=f'Played {playable.playcount} times')
          playcount.pack()
        if playable.lastplayed:
          lastplayed = tk.Label(content, text=f'Last played on {playable.lastplayed}')
          lastplayed.pack()
        if playable.public_rating:
          public_rating = tk.Label(content, text=f'Public Rating: {playable.public_rating}')
          public_rating.pack()
        if playable.premiere_date:
          premiere_date = tk.Label(content, text=f'Premiere Date: {playable.premiere_date}')
          premiere_date.pack()

        user_rating_row = tk.Frame(content)
        user_rating_row.pack()
        ttk.Label(user_rating_row, text='User Rating:').pack(side='left')
        user_rating = tk.StringVar()
        user_rating.set(playable.user_rating or '')
        ttk.Entry(user_rating_row, textvariable=user_rating).pack(side='left')

        music_start_row = tk.Frame(content)
        music_start_row.pack()
        ttk.Label(music_start_row, text='Music Start (ms):').pack(side='left')
        music_start_var = tk.StringVar()
        music_start_var.set(playable.start_time_ms or '')
        ttk.Entry(music_start_row, textvariable=music_start_var).pack(side='left')


        music_end_row = tk.Frame(content)
        music_end_row.pack()
        ttk.Label(music_end_row, text='Music End (ms):').pack(side='left')
        music_end_var = tk.StringVar()
        music_end_var.set(playable.end_time_ms or '')
        ttk.Entry(music_end_row, textvariable=music_end_var).pack(side='left')

        current_tags_frame = tk.Frame(content)
        current_tags_frame.pack()
        ttk.Label(current_tags_frame, text='Current Tags: ').pack(side='left')
        current_tags_var = tk.StringVar()
        current_tags_var.set(', '.join(playable.tags))
        current_tags_label = ttk.Label(current_tags_frame, textvariable=current_tags_var)
        current_tags_label.pack(side='left')

        remove_tag_frame = tk.Frame(content)
        remove_tag_frame.pack()
        ttk.Label(remove_tag_frame, text='Remove Tag:').pack(side='left')
        remove_tag_var = tk.StringVar()
        remove_tag_entry = ttk.Entry(remove_tag_frame, textvariable=remove_tag_var)
        remove_tag_entry.pack(side='left')
        def remove_tag():
          tag = remove_tag_var.get()
          if tag in playable.tags:
            playable.tags.remove(tag)
            current_tags_var.set(', '.join(playable.tags))
            remove_tag_var.set('')
        ttk.Button(remove_tag_frame, text='Remove Tag', command=remove_tag).pack(side='left')

        add_tag_frame = tk.Frame(content)
        add_tag_frame.pack()
        ttk.Label(add_tag_frame, text='Add Tag:').pack(side='left')
        tag_var = tk.StringVar()
        tag_entry = ttk.Entry(add_tag_frame, textvariable=tag_var)
        tag_entry.pack(side='left')
        def add_tag():
            tag = tag_var.get()
            if tag:
                playable.tags.append(tag)
                current_tags_var.set(', '.join(playable.tags))
                tag_var.set('')
        ttk.Button(add_tag_frame, text='Add Tag', command=add_tag).pack(side='left')

        def save():
            if music_start_var.get():
              playable.start_time_ms = int(music_start_var.get())
            if user_rating.get():
              playable.user_rating = int(user_rating.get())
            if music_end_var.get():
              playable.end_time_ms = int(music_end_var.get())
            add_infos.save_playable_to_file(playable, storage)

        save_button = ttk.Button(content, text='Save', command=save)
        save_button.pack()

        def play_file():
            play_playable(playable, storage, collection)

        play_frame = tk.Frame(content)
        play_frame.pack(side='bottom', pady=10)
        ttk.Button(play_frame, text='Play', command=lambda: play_file()).pack()

        
        return content
    return popup_content
