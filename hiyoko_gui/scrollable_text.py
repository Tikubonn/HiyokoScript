
import tkinter as tk 
import tkinter.ttk as ttk 
from .traceable_text import TraceableText

class ScrollableText (tk.Frame):

  def __init__ (self, master=None, *, scrollx=True, scrolly=True):
    super().__init__(master)
    self.text = None 
    self.scrollbarx = None 
    self.scrollbary = None 
    self.scrollx = scrollx
    self.scrolly = scrolly
    self.setup_widgets()

  def setup_widgets (self):
    text = TraceableText(self)
    text.grid(row=0, column=0, sticky=tk.NSEW)
    self.text = text
    if self.scrollx:
      scrollbarx = tk.Scrollbar(self, orient=tk.HORIZONTAL)
      scrollbarx.grid(row=1, column=0, sticky=tk.EW)
      text.config(xscrollcommand=scrollbarx.set)
      scrollbarx.config(command=text.xview)
      self.scrollbarx = scrollbarx
    if self.scrolly:
      scrollbary = tk.Scrollbar(self, orient=tk.VERTICAL)
      scrollbary.grid(row=0, column=1, sticky=tk.NS)
      text.config(yscrollcommand=scrollbary.set)
      scrollbary.config(command=text.yview)
      self.scrollbary = scrollbary
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=0)

if __name__ == "__main__": #test
  window = tk.Tk()
  text = ScrollableText(window)
  text.pack(fill=tk.BOTH, expand=True)
  buttonclear = tk.Button(window, text="Clear modified", command=lambda: text.text.set_modified(False))
  buttonclear.pack()
  text.text.set_modified(False)
  text.text.add_onupdate(lambda: window.title("modified={:d}".format(text.text.modified)))
  text.text.call_onupdates() #call manually for initialize window title.
  window.mainloop()
