
import tkinter as tk 
import tkinter.ttk 
from .scrollable_listbox import ScrollableListbox

class ScrollableListboxAndInput (tk.Frame):

  def __init__ (self, master=None, *, scrollx=False, scrolly=True, onupdate=None):
    super().__init__(master)
    self.scrollx = scrollx
    self.scrolly = scrolly
    self.listbox = None 
    self.input = None     
    self._onupdates = list() 
    self.setup_widgets()

  def _set_input (self, value):
    self.input.delete(0, tk.END)
    self.input.insert(0, str(value))

  def _set_listbox (self, value):
    self.listbox.listbox.select_clear(0, tk.END)
    for index, item in enumerate(self.listbox.listbox.get(0, tk.END)):
      if item == str(value):
        self.listbox.listbox.select_set(index)
        self.listbox.listbox.see(index)

  def set_value (self, value):
    self._set_input(value)
    self._set_listbox(value)

  def get_value (self):
    return self.input.get()

  def add_onupdate (self, func):
    self._onupdates.append(func)

  def call_onupdates (self):
    for onupdate in self._onupdates:
      onupdate()

  def _onupdateinput (self, event):
    self._set_listbox(self.input.get())
    self.call_onupdates()

  def _onupdatelistbox (self, event):
    indexes = self.listbox.listbox.curselection()
    if indexes:
      self._set_input(self.listbox.listbox.get(indexes[0]))
      self.call_onupdates()

  def setup_widgets (self):
    listbox = ScrollableListbox(self, scrollx=self.scrollx, scrolly=self.scrolly)
    listbox.grid(row=0, column=0, sticky=tk.NSEW)
    listbox.listbox.bind("<<ListboxSelect>>", self._onupdatelistbox, add="+")
    entry = tk.Entry(self)
    entry.grid(row=1, column=0, sticky=tk.EW)
    entry.bind("<KeyRelease>", self._onupdateinput, add="+")
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=0)
    self.grid_columnconfigure(0, weight=1)
    self.listbox = listbox
    self.input = entry

import tkinter.font

if __name__ == "__main__": #test 
  root = tk.Tk()
  listboxandinput = ScrollableListboxAndInput(root)
  listboxandinput.pack(fill=tk.BOTH, expand=True)
  for family in tk.font.families():
    listboxandinput.listbox.listbox.insert(tk.END, family)    
  root.mainloop()
