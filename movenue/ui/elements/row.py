import random
import tkinter as tk
from tkinter import ttk
from typing import Callable, Tuple

from loguru import logger
from movenue.ui.constants import ui_colors

class ScrollRow(object):
    base_width = 100
    def __init__(self, ui_element_lambdas: list[Callable[[tk.Widget, int], Tuple[tk.Widget, int]]], max_width:int, master:tk.Widget, height:int = 200) -> None:
        logger.debug(f'Creating scroll row with {len(ui_element_lambdas)} elements')
        self.max_width = max_width
        self.height = height
        self.frame = tk.Frame(master, background=ui_colors.DEFAULT_BACKGROUND)
        self.wrapper = tk.Frame(self.frame, background=ui_colors.DEFAULT_BACKGROUND)
        self.wrapper.pack()
        self._previous_container = tk.Frame(self.wrapper, width=50, height=self.height, background=ui_colors.DEFAULT_BACKGROUND)
        self._previous_container.pack(side=tk.LEFT)
        self.card_container = tk.Frame(self.wrapper, background=ui_colors.DEFAULT_BACKGROUND)
        self.card_container.pack(side=tk.LEFT, expand=True, padx=0, ipadx=0)
        self._next_container = tk.Frame(self.wrapper, width=50, height=self.height, background=ui_colors.DEFAULT_BACKGROUND)
        self._next_container.pack(side=tk.LEFT)
        self.next_button = tk.Canvas(self._next_container, background=ui_colors.DEFAULT_BACKGROUND, width=50,height=self.height, highlightthickness=0)
        self.next_button.bind('<Button-1>', lambda ev: self.rotate_to_next())
        self.next_button.create_polygon(0,0,50,self.height/2,0,self.height, fill=ui_colors.DEFAULT_BUTTON)
        self.previous_button = tk.Canvas(self._previous_container, background=ui_colors.DEFAULT_BACKGROUND, width=50,height=self.height, highlightthickness=0)
        self.previous_button.bind('<Button-1>', lambda ev: self.rotate_to_previous())
        self.previous_button.create_polygon(50,0,0,self.height/2,50,self.height, fill=ui_colors.DEFAULT_BUTTON)
        self.ui_element_lambdas = ui_element_lambdas
        self.current_posters = []
        self.current_index = 0
        self.pack_posters()
        self.populate_buttons()
        logger.debug(f'Created scroll row with {len(ui_element_lambdas)} elements')

    def rotate_to_previous(self):
        for poster in self.current_posters:
            poster.pack_forget()

        current_width = self.base_width
        current_index = self.current_index

        els = []
        prev_lambdas = self.ui_element_lambdas[:current_index]
        prev_lambdas.reverse()
        for lamda_function in prev_lambdas:
            el, el_width = lamda_function(self.card_container, self.height)
            if current_width + el_width > self.max_width:
                break
            els.append(el)
            current_width += el_width
        
            if self.current_index == 0:
                els.reverse()
                # populate additional posters
                internal_index = len(els)
                while len(els) < len(self.ui_element_lambdas):
                    el, el_width = self.ui_element_lambdas[internal_index](self.card_container, self.height)
                    internal_index += 1
                    internal_index += el_width
                    if current_width > self.max_width:
                        break
                    els.append(el)
                els.reverse()
                break
            self.current_index -= 1

        els.reverse()

        for el in els:
            el.pack(side='left', padx=0, ipadx=0)
        self.current_posters = els
        self.populate_buttons()
        

    def rotate_to_next(self):
        new_index = self.current_index + len(self.current_posters)
        for poster in self.current_posters:
            poster.pack_forget()
        els = []
        current_width = self.base_width
        internal_index = new_index
        while len(els) < len(self.ui_element_lambdas) - new_index:
            el, el_width = self.ui_element_lambdas[internal_index](self.card_container, self.height)
            internal_index += 1
            if current_width + el_width > self.max_width:
                break
            current_width += el_width
            els.append(el)

        if len(els) == len(self.ui_element_lambdas) - new_index:
            prev_lambdas = self.ui_element_lambdas[:new_index]
            prev_lambdas.reverse()
            els.reverse()
            for lamda_function in prev_lambdas:
                el, el_width = lamda_function(self.card_container, self.height)
                if current_width + el_width > self.max_width:
                    break
                els.append(el)
                current_width += el_width
                new_index -= 1
            els.reverse()

        
        for el in els:
            el.pack(side='left', padx=0, ipadx=0)
        self.current_posters = els
        self.current_index = new_index
        self.populate_buttons()

    def populate_buttons(self):
        self.previous_button.pack_forget()
        self.next_button.pack_forget()
        if self.current_index > 0:            
            self.previous_button.pack()
        if self.current_index + len(self.current_posters) < len(self.ui_element_lambdas):
            self.next_button.pack()


    def pack_posters(self):
        logger.debug(f'Packing posters from index {self.current_index}')
        current_width = self.base_width
        self.current_posters = []

        for idx, el in enumerate(self.ui_element_lambdas[self.current_index:]):
            el, el_width = el(self.card_container, self.height)
            if current_width + el_width > self.max_width:
                break
            el.pack(side='left', padx=0, ipadx=0)
            current_width += el_width
            self.current_posters.append(el)
        logger.debug(f'Packed {len(self.current_posters)} posters')


class HeadedScrollRow(tk.Frame):
    def __init__(self, ui_element_lambdas: list[Callable[[tk.Widget, int], Tuple[tk.Widget, int]]], max_width:int, master:tk.Widget, title:str, height:int = 200) -> None:
        logger.debug(f'Creating headed scroll row with {len(ui_element_lambdas)} elements')
        super().__init__(master)
        title = title.strip().replace('\n', ' ')
        header = tk.Frame(self, background=ui_colors.SCROLL_ROW_TITLE_BACKGROUND)
        header.pack(side='top', fill='x')
        title_lbl = ttk.Label(header, text=title, background=ui_colors.SCROLL_ROW_TITLE_BACKGROUND, foreground='white')
        title_lbl.pack(side='top')
        logger.debug(f'Creating scroll row with {len(ui_element_lambdas)} elements')
        scroll_row = ScrollRow(ui_element_lambdas, max_width, self, height)
        scroll_row.frame.pack(side='top', fill='x')
        logger.debug(f'Created headed scroll row with {len(ui_element_lambdas)} elements')