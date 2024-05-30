from tkinter import ttk
import tkinter as tk
from typing import Callable
from movenue.ui.constants import ui_colors

from movenue.ui.elements.row import HeadedScrollRow

class RowScrollBox(ttk.Frame):
    """
    A scrollable frame that contains multiple rows.
    """
    def __init__(self, master, rows: Callable[[tk.Widget], HeadedScrollRow], **kwargs):
        super().__init__(master, **kwargs)

        
        self.genre_pos = 0
        self.y_genre_count = int((self.winfo_screenheight() - 120) / 240) if self.winfo_screenheight() else 4
        
        self.up_button = tk.Button(self, background=ui_colors.DEFAULT_BUTTON, text='Up', command=lambda: self.go_up(), foreground='white')
        self.genre_frame = tk.Frame(self, background=ui_colors.DEFAULT_BACKGROUND)


        self.down_button = tk.Button(self, background=ui_colors.DEFAULT_BUTTON, text='Down', command=lambda: self.go_down(), foreground='white')
        
        row_els = []
        for row in rows:
            row_els.append(row(self.genre_frame))
        self.rows = row_els
    
        self.up_button.pack(ipadx=20, ipady=10, pady=4)
        self.genre_frame.pack()
        self.down_button.pack(ipadx=20, ipady=10, pady=4)
        self.update_genres()

    def go_down(self):
        if self.genre_pos + self.y_genre_count < len(self.rows):
            self.genre_pos = self.genre_pos + 1
            self.update_genres()

    def go_up(self):
        if self.genre_pos > 0:
            self.genre_pos = self.genre_pos - 1
            self.update_genres()

    def set_genres(self):
        for i in range(self.genre_pos, self.genre_pos + self.y_genre_count):
            if i >= len(self.rows):
                break
            cat = self.rows[i]
            cat.pack(side='top', fill='x')
            # cat.get_ui_element(self.genre_frame)

    def update_genres(self):
        for slave in self.genre_frame.pack_slaves():
            slave.pack_forget()
        self.set_genres()