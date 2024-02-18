import logging
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from laoflix.ui_elements.movie_card import MovieCard
from laoflix.ui_elements.main_window import MainWindow
from loguru import logger


if __name__ == '__main__':

    # Setup local files and logging
    
    # create folder if not present
    folder_path = os.path.join(os.environ['LOCALAPPDATA'], 'laoflix')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    logging_path = os.path.join(folder_path, 'logs')
    if not os.path.exists(logging_path):
        os.makedirs(logging_path)
    # setup logging
    logger.add(os.path.join(logging_path, 'laoflix.log'), format="{time} {level} {message}", level="INFO", rotation="5 MB", compression="zip", serialize=False)


    main_window = MainWindow()
    main_window.run()