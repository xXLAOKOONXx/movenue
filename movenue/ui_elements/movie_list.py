
from tkinter import ttk
import tkinter as tk
from movenue.ui_elements.movie_card import MovieCard
import os



class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)

class MovieList:
    def __init__(self, movie_folder='//myNAS/Daten/Videos/Filme/'):
        available_movie_types = ['nfo']
        movie_files = os.listdir(movie_folder)
        movie_files = [file_name for file_name in movie_files if file_name.split('.')[-1] in available_movie_types]
        self.movies = [MovieCard(movie_folder, '.'.join(file_name.split('.')[0:-1])) for file_name in movie_files]

    def get_ui_element(self, master):
        # dynamic_grid = DynamicGrid(master)
        my_frame = tk.Frame(master)
        my_frame.pack()

        for m in self.movies:
            poster = m.get_poster(my_frame)
            poster.pack()
            # dynamic_grid.configure(state='normal')
            # dynamic_grid.window_create('end', window=box)
            # dynamic_grid.configure(state='disabled')
        return my_frame