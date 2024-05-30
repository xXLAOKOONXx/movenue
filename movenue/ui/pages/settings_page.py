import json
import os
import tkinter as tk
from tkinter import filedialog

from movenue.models.settings import SEARCH_TYPES, CategorySettings, FolderSetting


class SettingsPage(tk.Frame):
    def __init__(self, master:tk.Widget, cat_settings:list[CategorySettings], **kwargs):
        super().__init__(master=master,**kwargs)
        self.cat_settings = cat_settings

        self.cat_settings_frame = tk.Frame(self)
        self.cat_settings_frame.pack(side='top', fill='both', expand=True)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side='top', fill='both', expand=True)

        self.add_cat_btn = tk.Button(self.buttons_frame, text='Add Category', command=self.add_category)
        self.add_cat_btn.pack(side='left')

        self.remove_category_var = tk.StringVar()
        self.remove_category_entry = tk.Entry(self.buttons_frame, textvariable=self.remove_category_var)
        self.remove_category_entry.pack(side='left')

        self.remove_cat_btn = tk.Button(self.buttons_frame, text='Remove Category', command=self.remove_category)
        self.remove_cat_btn.pack(side='left')

        self.save_settings_btn = tk.Button(self.buttons_frame, text='Save Settings', command=self.save_settings)
        self.save_settings_btn.pack(side='right')

        self.draw_settings()

    def add_category(self):
        self.cat_settings.append(CategorySettings('New Category', [], page_module='category_page'))
        self.get_setting_ui_frame(self.cat_settings[-1]).pack(side='left')
    
    def remove_category(self):
        if not self.remove_category_var.get():
            return
        for cat in self.cat_settings:
            if cat.name == self.remove_category_var.get():
                self.cat_settings.remove(cat)
                self.remove_category_var.set('')
                break
            
    def get_folder_ui_frame(self, folder, folders_frame):
        folder_frame = tk.Frame(folders_frame)
        path_var = tk.StringVar()
        path_var.set(str(folder.path))
        path_label = tk.Label(folder_frame, textvariable=path_var)
        def set_path(path_var, folder):
            get_folder = filedialog.askdirectory()
            if get_folder:
                path_var.set(get_folder)
                folder.path = get_folder
        path_label.bind('<Button-1>', lambda e, path_var=path_var, folder=folder: set_path(path_var, folder))
        path_label.pack()

        search_type_var = tk.StringVar()
        search_type_var.set(folder.search_type)
        def on_searchtype_change(folder, var, *args):
            folder.search_type = var.get()
        search_type_var.trace_add('write', lambda *args, folder=folder, var=search_type_var: on_searchtype_change(folder, var, *args))
        for optional_search_type in ['playables', 'collections']:
            tk.Radiobutton(folder_frame, text=optional_search_type, value=optional_search_type, variable=search_type_var).pack()
        
        tk.Label(folder_frame, text='Include Subfolders').pack()
        include_subfolders_var = tk.BooleanVar()
        include_subfolders_var.set(folder.include_subfolders_for_playables)
        def on_include_subfolders_change(folder, var, *args):
            folder.include_subfolders_for_playables = var.get()
        include_subfolders_var.trace_add('write', lambda *args, folder=folder, var=include_subfolders_var: on_include_subfolders_change(folder, var, *args))
        include_subfolders_entry = tk.Checkbutton(folder_frame, variable=include_subfolders_var)
        include_subfolders_entry.pack()
        return folder_frame
            
    def get_setting_ui_frame(self, setting:CategorySettings):
        setting_frame = tk.Frame(self.cat_settings_frame)
        tk.Label(setting_frame, text='Name').pack()
        name_var = tk.StringVar()
        name_var.set(setting.name)
        name_entry = tk.Entry(setting_frame, textvariable=name_var)
        name_entry.pack()
        tk.Label(setting_frame, text='Page Module').pack()

        folders_frame = tk.Frame(setting_frame)
        folders_frame.pack()
        for folder in setting.folders:
            self.get_folder_ui_frame(folder, folders_frame).pack()

        def add_folder(setting, folders_frame):
            setting.folders.append(FolderSetting('CLICK TO SELECT FOLDER', 'playables', True))
            self.get_folder_ui_frame(setting.folders[-1], folders_frame).pack()
        tk.Button(setting_frame, text='Add Folder', command=lambda setting=setting, folders_frame=folders_frame: add_folder(setting, folders_frame)).pack()



        module_var = tk.StringVar()
        module_var.set(setting.page_module)
        for module in ['category_page', 'search_page', 'filter_page']:
            tk.Radiobutton(setting_frame, text=module, value=module, variable=module_var).pack()

        

        def update_setting(name_entry, module_var, setting):
            setting.name = name_entry.get()
            setting.page_module = module_var.get()
            self.save_settings()
            

        tk.Button(setting_frame, text='Save', command=lambda name_entry=name_entry, module_var=module_var, setting=setting: update_setting(name_entry, module_var, setting)).pack()
        return setting_frame
            
    def draw_settings(self):
        for cat in self.cat_settings:
            self.get_setting_ui_frame(cat).pack(side='left')

    def save_settings(self):
        local_app_data_folder = os.path.join(os.environ['LOCALAPPDATA'], 'movenue')
        settings_path = os.path.join(local_app_data_folder, 'category_settings.json')
        with open(settings_path, 'w') as file:
            json.dump([cat.__to_json__() for cat in self.cat_settings], file)
