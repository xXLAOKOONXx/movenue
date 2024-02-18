
import tkinter as tk
from typing import Callable
from movenue.services.icons import icons
from PIL import ImageTk

def add_seen_tag(canvas:tk.Canvas, canvas_width:int, validation:bool=True, size:int=30):
    '''
    Function to add a 'seen' tag to a canvas.
    '''
    if not validation:
        return
    canvas.create_polygon(canvas_width - size,0,canvas_width,size,canvas_width,0,fill='green')
    try:
        canvas.create_image(canvas_width - 1 - int(size/4), int(size/4), image=icons.eye_icon(int(size/2)))
    except Exception as ex:
        print(f'error adding eye icon {ex=}')

def add_started_tag(canvas:tk.Canvas, canvas_width:int, validation:bool=True, size:int=30):
    '''
    Function to add a 'seen' tag to a canvas.
    '''
    if not validation:
        return
    canvas.create_polygon(canvas_width - size,0,canvas_width,size,canvas_width,0,fill='yellow')

def add_error_tag(canvas:tk.Canvas, canvas_width:int, validation:bool=True, size:int=30):
    '''
    Function to add a 'seen' tag to a canvas.
    '''
    if not validation:
        return
    canvas.create_polygon(canvas_width - size,0,canvas_width,size,canvas_width,0,fill='red')

def add_bottom_text(canvas:tk.Canvas, canvas_width:int, canvas_height:int, text:str):
    if not text:
        return
    canvas.create_rectangle(10, canvas_height - 25, canvas_width - 10, canvas_height - 5, fill='white')
    canvas.create_text(canvas_width/2, canvas_height - 15, text=text, fill='black')

def add_on_click(canvas:tk.Canvas, func:Callable[[tk.Event], object] | None):
    if func is None:
        return
    canvas.bind('<Button-1>', func)


def create_image_canvas(master:tk.Widget, canvas_width:int, canvas_height:int, image:ImageTk.PhotoImage|None, bottom_text:str='', image_alt_text:str='', seen_validation:bool=False, seen_size:int=30,
                        on_click_func:Callable[[tk.Event], object] | None = None):
    canvas = tk.Canvas(master=master, width=canvas_width, height=canvas_height, highlightthickness=0)
    try:
        if not image:
            raise ValueError('No Image')
        canvas.create_image(canvas_width/2, canvas_height/2, image=image)
    except Exception:
        canvas.create_text(canvas_width/2, canvas_height/2, text=image_alt_text, width=canvas_width)
    add_bottom_text(canvas=canvas, canvas_width=canvas_width, canvas_height=canvas_height, text=bottom_text)
    add_seen_tag(canvas=canvas, canvas_width=canvas_width, validation=seen_validation, size=seen_size)
    add_on_click(canvas=canvas, func=on_click_func)
    return canvas