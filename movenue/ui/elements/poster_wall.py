from tkinter import ttk
import tkinter as tk
from typing import Callable, Tuple
from movenue.ui.constants import ui_colors

class PosterWall(ttk.Frame):
    """
    A scrollable frame that contains multiple rows.
    """
    def __init__(self, master:tk.Widget, poster_lambdas: list[Callable[[tk.Widget, int], Tuple[tk.Widget, int]]], poster_height:int=200, **kwargs):
        super().__init__(master, **kwargs)

        self.rows:list[tk.Widget] = []
        self.processed_posters:int = 0
        self.poster_lambdas = poster_lambdas
        self.poster_height = poster_height
        
        self.row_position = 0
        self.row_view_count = int((master.winfo_height() - 120) / poster_height) if master.winfo_height() > 1 else 4
        
        self.up_button = tk.Button(self, background=ui_colors.DEFAULT_BUTTON, text='Up', command=lambda: self.go_up(), foreground='white')
        self.wall_frame = tk.Frame(self, background=ui_colors.DEFAULT_BACKGROUND)
        self.down_button = tk.Button(self, background=ui_colors.DEFAULT_BUTTON, text='Down', command=lambda: self.go_down(), foreground='white')
    
        self.up_button.pack(ipadx=20, ipady=10, pady=4)
        self.wall_frame.pack()
        self.down_button.pack(ipadx=20, ipady=10, pady=4)
        self.update_rows()

    def go_down(self):
        if (self.row_position + self.row_view_count < len(self.rows)) or (self.processed_posters < len(self.poster_lambdas)):
            self.row_position = self.row_position + 1
            self.update_rows()

    def go_up(self):
        if self.row_position > 0:
            self.row_position = self.row_position - 1
            self.update_rows()

    def set_rows(self):
        for i in range(self.row_position, self.row_position + self.row_view_count):
            if i >= len(self.rows):
                if self.processed_posters >= len(self.poster_lambdas):
                    break
                max_row_width = self.wall_frame.winfo_screenwidth()
                cur_row_width = 0
                row_element = tk.Frame(self.wall_frame)
                for _ in range(len(self.poster_lambdas) - self.processed_posters):
                    poster, width = self.poster_lambdas[self.processed_posters](row_element, self.poster_height)
                    if cur_row_width + width > max_row_width:
                        break
                    cur_row_width += width
                    poster.pack(side='left')
                    self.processed_posters += 1
                self.rows.append(row_element)
            cat = self.rows[i]
            cat.pack(side='top', fill='x')

    def update_rows(self):
        for slave in self.wall_frame.pack_slaves():
            slave.pack_forget()
        self.set_rows()