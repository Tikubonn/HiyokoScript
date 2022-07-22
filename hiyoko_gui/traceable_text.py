
import tkinter as tk 
import tkinter.ttk as ttk 

class TraceableText (tk.Text): #変更を検知可能なテキスト部品です

  def __init__ (self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._lastcontent = None 
    self._onupdates = list() 
    self.bind("<KeyRelease>", self._onkeyrelease)

  @property
  def modified (self):
    return self.get("1.0", tk.END) != self._lastcontent

  def set_modified (self, state):
    if state:
      self._lastcontent = None 
    else:
      self._lastcontent = self.get("1.0", tk.END)
    self.call_onupdates()

  def add_onupdate (self, func):
    self._onupdates.append(func)

  def call_onupdates (self):
    for onupdate in self._onupdates:
      onupdate()

  def _onkeyrelease (self, event):
    self.call_onupdates()

  def insert (self, *args, **kwargs): #override
    super().insert(*args, **kwargs)
    self.call_onupdates()

  def delete (self, *args, **kwargs): #override
    super().delete(*args, **kwargs)
    self.call_onupdates()

if __name__ == "__main__":
  window = tk.Tk()
  text = TraceableText(window)
  text.pack(fill=tk.BOTH, expand=True)
  buttonclear = ttk.Button(window, text="Clear modified", command=lambda: text.set_modified(False))
  buttonclear.pack()
  text.set_modified(False) 
  text.add_onupdate(lambda: window.title("modified={:d}".format(text.modified)))
  text.call_onupdates() #call manually for initialize window title.
  window.mainloop()
