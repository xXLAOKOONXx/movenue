from typing import Callable, Tuple
from PIL import Image, ImageTk
import tkinter as tk
from movenue.models.collection import Collection
from movenue.ui.elements.popup_window import PopupWindow
from movenue.ui.elements.posters.collection_popup import collection_popup
from movenue.ui.elements.posters.playable_popup import playable_popup
from movenue.ui.services import canvas_helpers
from movenue.services import image_builder
import math

from loguru import logger

from movenue.models.playable import Playable

def build_poster(displayable:Playable | Collection, popup_master: tk.Widget, show_title: bool = True, show_played:bool = True, default_width:int=100) -> Callable[[tk.Widget, int], Tuple[tk.Widget, int]]:
  if isinstance(displayable, Playable):
    return playable_poster_lambda(displayable, popup_master, show_title, show_played, default_width)
  if isinstance(displayable, Collection):
    return collection_poster_lambda(displayable, popup_master, show_title, show_played, default_width)

def playable_poster_lambda(playable: Playable, popup_master: tk.Widget, show_title: bool = True, show_played:bool = True, default_width:int=100, include_index_number:bool = True, parent_collection:Collection|None=None) -> Callable[[tk.Widget, int], Tuple[tk.Widget, int]]:
  """
  Returns a lambda function that creates a playable poster and returns the poster and its width.
  """
  def lambda_function(master: tk.Widget, height: int) -> Tuple[tk.Widget, int]:
    def open_popup():
      popup = PopupWindow(popup_master, playable_popup(playable, collection=parent_collection))
      popup.activate()
    pretty_name = ''
    if show_title:
      pretty_name = playable.title
      if playable.index_number and include_index_number:
        pretty_name = f'{playable.index_number} - {pretty_name}'

    calc_width = default_width
    img = None
    image_builder.populate_playable_image(playable)
    if playable.poster_image is not None:
      calc_width = math.floor(playable.poster_image.width * height / playable.poster_image.height)
      img = playable.tkimages.get((calc_width, height))
      if img is None:
        i = playable.poster_image.resize((calc_width, height))
        img = ImageTk.PhotoImage(i)
        playable.tkimages[(calc_width, height)] = img

    poster = canvas_helpers.create_image_canvas(
        master=master,
        canvas_width=calc_width,
        canvas_height=height,
        image=img,
        image_alt_text=playable.title,
        on_click_func=lambda ev: open_popup(),
        bottom_text=pretty_name,
    )

    if playable.playcount and show_played:
      canvas_helpers.add_seen_tag(poster, calc_width, validation=True, size=30)
    return poster, calc_width

  return lambda_function

def collection_poster_lambda(collection: Collection, popup_master: tk.Widget, show_title: bool = True, show_played:bool = True, default_width:int=100, on_click:Callable | None=None) -> Callable[[tk.Widget, int], Tuple[tk.Widget, int]]:
  """
  Returns a lambda function that creates a playable poster and returns the poster and its width.
  """
  def lambda_function(master: tk.Widget, height: int) -> Tuple[tk.Widget, int]:
    def open_popup():
      popup = PopupWindow(popup_master, collection_popup(collection))
      popup.activate()
    nonlocal on_click
    if not on_click:
      on_click = open_popup

    pretty_name = collection.title
    calc_width = default_width
    img = None
    image_builder.populate_collection_image(collection)
    if collection.poster_image is not None:
      calc_width = math.floor(collection.poster_image.width * height / collection.poster_image.height)
      img = collection.tkimages.get((calc_width, height))
      if img is None:
        i = collection.poster_image.resize((calc_width, height))
        img = ImageTk.PhotoImage(i)
        collection.tkimages[(calc_width, height)] = img

    poster = canvas_helpers.create_image_canvas(
        master=master,
        canvas_width=calc_width,
        canvas_height=height,
        image=img,
        image_alt_text=collection.title,
        on_click_func=lambda ev: on_click(),
        bottom_text=pretty_name,
    )
    return poster, calc_width

  return lambda_function