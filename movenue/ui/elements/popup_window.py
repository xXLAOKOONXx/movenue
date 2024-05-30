import tkinter as tk
from typing import Callable
from movenue.ui.constants import ui_colors

class PopupWindow(tk.Frame):
    def __init__(self, master: tk.Widget, content_lambda: Callable[[tk.Widget], tk.Widget]):
        super().__init__(master)
        background = tk.Frame(self, background=ui_colors.POPUP_BACKGROUND)
        background.place(relx=0.5,rely=0.5,relwidth=1,relheight=1,anchor='center')
        foreground = tk.Frame(background, background=ui_colors.POPUP_FOREGROUND)
        foreground.place(relx=0.5,rely=0.5,relheight=0.8,relwidth=0.8,anchor='center')
        background.bind('<Button-1>', func=lambda ev: self.deactivate())
        content=content_lambda(foreground, width=master.winfo_width() * 0.8, height=master.winfo_height() * 0.8)
        content.pack(expand=True, fill='both')

    def activate(self):
        self.place(relx=0.5,rely=0.5,relwidth=1,relheight=1,anchor='center')

    def deactivate(self):
        self.place_forget()