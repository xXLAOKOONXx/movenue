from movenue.ui.constants import ui_colors
from movenue.ui.pages.category_page import CategoryPage
from movenue.ui.pages.settings_page import SettingsPage
from movenue.models.settings import CategorySettings, FolderSetting
from movenue.models.storage import Storage
from movenue.ui.services.icons import get_app_icon_path
from movenue.ui.services.page_modul_integration import get_page_frame
import tkinter as tk

class MainWindow:
    
    def __init__(self, cat_settings:list[CategorySettings] = []):
        self.pages = []
        self.window = tk.Tk()
        self.window.winfo_screen
        self.window.iconbitmap(get_app_icon_path())
        self.window.configure(background=ui_colors.DEFAULT_BACKGROUND)
        self.window.attributes('-fullscreen', True)

        store = Storage(cat_settings)

        self.header_frame = tk.Frame(self.window, background=ui_colors.TOP_MENU_BACKGROUND)
        self.header_frame.pack(side=tk.TOP, fill='x')

        self.body_frame = tk.Frame(self.window, background=ui_colors.DEFAULT_BACKGROUND)
        self.body_frame.pack(side=tk.TOP, expand=True, fill='both')

        self.window.title('Movenue')

        self.selected_page:str|None = None
        
        def set_page(page:tk.Widget, master:tk.Widget, page_name:str|None=None):
            for pack_slave in master.pack_slaves():
                pack_slave.pack_forget()
            loading = tk.Label(master, text='Setting up...')
            loading.pack()
            master.update_idletasks()
            page.pack(side='top', fill='both', expand=True)
            self.selected_page = page_name
            loading.pack_forget()

        def refresh_page():         
            if self.selected_page:
                store.refresh_category(self.selected_page)   
            for pack_slave in self.body_frame.pack_slaves():
                pack_slave.pack_forget()
                pack_slave.pack(side='top', fill='both', expand=True)

        for setting in cat_settings:
            page = get_page_frame(settings=setting, store=store, master=self.body_frame)
            btn = tk.Button(self.header_frame, text=setting.name, padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda page_name=setting.name,page=page: set_page(page, self.body_frame, page_name))
            btn.pack(side='left')

        exit_btn = tk.Button(self.header_frame, text='Exit', padx=20, background=ui_colors.EXIT_BUTTON_COLOR, foreground='white', command=self.window.destroy)
        exit_btn.pack(side='right')

        self.settings_page = SettingsPage(master=self.body_frame, cat_settings=cat_settings)

        settings_btn = tk.Button(self.header_frame, text='Settings', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: set_page(self.settings_page, self.body_frame))
        settings_btn.pack(side='right')

        refresh_btn = tk.Button(self.header_frame, text='Refresh', padx=20, background=ui_colors.MENU_BUTTON_COLOR, foreground='white', command=lambda: refresh_page())
        refresh_btn.pack(side='right')

        self.window.bind('<Escape>', lambda e: self.window.destroy())
    
    def start(self):
        self.window.mainloop()