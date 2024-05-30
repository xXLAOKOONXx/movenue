

from movenue.models.settings import CategorySettings
from movenue.models.storage import Storage
from movenue.ui.pages.filter_page import FilterPage
from movenue.ui.pages.search_page import SearchPage
from movenue.ui.pages.category_page import CategoryPage
import tkinter as tk


def get_page_frame(settings: CategorySettings, master: tk.Widget, store: Storage, **kwargs):
    kwargs.update(settings.key_word_args)
    if settings.page_module == 'category_page':
        return CategoryPage(master=master, store=store, page_name=settings.name, **kwargs)
    elif settings.page_module == 'search_page':
        return SearchPage(master=master, store=store, page_name=settings.name, **kwargs)
    elif settings.page_module == 'filter_page':
        return FilterPage(master=master, store=store, page_name=settings.name, **kwargs)