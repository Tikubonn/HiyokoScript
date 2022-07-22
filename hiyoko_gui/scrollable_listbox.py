
import tkinter as tk 
import tkinter.ttk 

class ScrollableListbox (tk.Frame):

  def __init__ (self, master=None, *, scrollx=False, scrolly=True):
    super().__init__(master)
    self.listbox = None 
    self.scrollbarx = None 
    self.scrollbary = None 
    self.scrollx = scrollx
    self.scrolly = scrolly
    self.setup_widgets()

  def setup_widgets (self):
    listbox = tk.Listbox(self)
    listbox.grid(row=0, column=0, sticky=tk.NSEW)
    self.listbox = listbox
    if self.scrollx:
      scrollbarx = tk.Scrollbar(self, orient=tk.HORIZONTAL)
      scrollbarx.grid(row=1, column=0, sticky=tk.EW)
      listbox.config(xscrollcommand=scrollbarx.set)
      scrollbarx.config(command=listbox.xview)
      self.scrollbarx = scrollbarx
    if self.scrolly:
      scrollbary = tk.Scrollbar(self, orient=tk.VERTICAL)
      scrollbary.grid(row=0, column=1, sticky=tk.NS)
      listbox.config(yscrollcommand=scrollbary.set)
      scrollbary.config(command=listbox.yview)
      self.scrollbary = scrollbary
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=0)
