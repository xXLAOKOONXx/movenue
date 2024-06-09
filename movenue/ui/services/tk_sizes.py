import tkinter as tk

def get_width(widget: tk.Widget) -> int:
  """
  Get the width of a widget.
  """
  return widget.winfo_width() if widget.winfo_width() != 1 else get_width(widget.master)