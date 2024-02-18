import tkinter as tk
from typing import Callable
from movenue.ui_elements.popup_window import PopupWindow
from movenue.constants import ui_colors

class RatingDialog(tk.Frame):
    def __init__(self, master: tk.Widget, rating_call: Callable[[int], None], max_rating:int=10, marked_rating:int|None=None):
        super().__init__(master, background=ui_colors.POPUP_FOREGROUND)
        head = tk.Frame(self, background=ui_colors.POPUP_FOREGROUND)
        head.pack(side='top')

        title = tk.Label(head, text='Rating', background=ui_colors.POPUP_FOREGROUND)
        title.pack()

        body = tk.Frame(self, background=ui_colors.POPUP_FOREGROUND)
        body.pack(side='top')
        rating_colors = ui_colors.rating_colors()
        for i in range(1, max_rating + 1):
            highlight_color = ui_colors.POPUP_FOREGROUND
            if i == marked_rating:
                highlight_color = ui_colors.HIGHLIGHT_COLOR
            element = tk.Label(body, text=f'{i}', padx=10, pady=10, borderwidth=2, background=rating_colors[i], highlightthickness=5, highlightbackground=highlight_color)
            element.bind('<Button-1>', lambda ev,i=i: rating_call(i))
            element.pack(side='left', ipadx=20, ipady=20)

class RatingPopup(PopupWindow):
    def __init__(self, master: tk.Widget, rating_call: Callable[[int], None], max_rating:int=10, marked_rating:int|None=None):
        def add_scoring(score:int):
            self.deactivate()
            rating_call(score)
        content_lambda = lambda master: RatingDialog(master, add_scoring, max_rating=max_rating, marked_rating=marked_rating)
        super().__init__(master, content_lambda)
