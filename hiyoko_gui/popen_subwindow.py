
import sys 
import subprocess
import tkinter as tk 
import tkinter.ttk as ttk 
import tkinter.messagebox
from io import IOBase 
from abc import abstractmethod
from .layout import PADDING
from .language_holder import LanguageHolder 

class PopenSubWindow (LanguageHolder, tk.Toplevel):

  def __init__ (self, master, popen, *, language, title, text):
    LanguageHolder.__init__(self, language=language)
    tk.Toplevel.__init__(self, master)
    self.popen = popen
    self.progressbar = None 
    self.progressbarvar = tk.IntVar(self, 0)
    self.textvar = tk.StringVar(self, text)
    self.closebutton = None 
    self.cancelbutton = None 
    self.onsuccesses = list()
    self.onerrors = list()
    self.setup_widgets(title=title, text=text)

  def add_onsuccess (self, func):
    self.onsuccesses.append(func)

  def add_onerror (self, func):
    self.onerrors.append(func)

  def call_onsuccesses (self):
    for onsuccess in self.onsuccesses:
      onsuccess(self.popen)

  def call_onerrors (self):
    for onerror in self.onerrors:
      onerror(self.popen)

  def _update_loop (self):
    returncode = self.popen.poll()
    if returncode is not None:
      try:
        if returncode == 0:
          tk.messagebox.showinfo(
            self.translate("info_popen_success"), 
            self.translate("info_popen_success_desc"), 
            parent=self,
          )
          self.textvar.set(self.translate("popen_successed"))
          self.call_onsuccesses()
        else:
          tk.messagebox.showerror(
            self.translate("error_popen_error"), 
            self.translate("error_popen_error_desc"), 
            parent=self,
          )
          self.textvar.set(self.translate("popen_failed"))
          if isinstance(self.popen.stderr, str):
            print(self.popen.stderr, file=sys.stderr)
          elif isinstance(self.popen.stderr, IOBase):
            print(self.popen.stderr.read(), file=sys.stderr)
          self.call_onerrors()
      finally:
        self.progressbarvar.set(100)
        self.progressbar.config(mode="determinate", maximum=100)
        self.progressbar.stop()
        self.closebutton.config(state="enable")
        self.cancelbutton.config(state="disable")
    else:
      self.after(1000 // 60, self._update_loop)

  def destroy (self):
    try:
      self.popen.kill()
    finally:
      super().destroy()

  def setup_widgets (self, *, title, text):
    self.title(title)
    progressbarframe = ttk.Frame(self)
    progressbarframe.pack(fill=tk.X, padx=PADDING, pady=PADDING)
    label = ttk.Label(progressbarframe, anchor=tk.CENTER, textvariable=self.textvar)
    label.pack(fill=tk.X)
    progressbar = ttk.Progressbar(progressbarframe, mode="indeterminate", variable=self.progressbarvar, maximum=100)
    progressbar.start(1000 // 60)
    progressbar.pack(fill=tk.X)
    self.progressbar = progressbar
    buttonframe = ttk.Frame(self)
    buttonframe.pack(fill=tk.X, padx=PADDING, pady=PADDING)
    closebutton = ttk.Button(buttonframe, text=self.translate("button_close"), state="disable", command=self.destroy)
    closebutton.pack(side=tk.RIGHT)
    self.closebutton = closebutton
    cancelbutton = ttk.Button(buttonframe, text=self.translate("button_cancel"), command=self.destroy)
    cancelbutton.pack(side=tk.RIGHT)
    self.cancelbutton = cancelbutton
    self.after(1000 // 60, self._update_loop)

#test

if __name__ == "__main__":
  
  language = {
    "button_close": "button_close",
    "button_cancel": "button_cancel",
    "info_popen_success": "info_popen_success",
    "info_popen_success_desc": "info_popen_success_desc",
    "error_popen_error": "error_popen_error",
    "error_popen_error_desc": "error_popen_error_desc",
    "popen_successed": "popen_successed",
    "popen_failed": "popen_failed",
  }
  
  def exec_sleep (window):
    popen = subprocess.Popen(["sleep", "5"], shell=True, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    win = PopenSubWindow(window, popen, title="Sleeping", text="Sleeping until 5sec.", language=language)
  
  def exec_error (window):
    popen = subprocess.Popen(["py", "unexists-file.py"], shell=True, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    win = PopenSubWindow(window, popen, title="Always error", text="Always cause error.", language=language)

  window = tk.Tk()
  testbutton1 = ttk.Button(window, text="Test1", command=lambda: exec_sleep(window))
  testbutton1.pack(fill=tk.X)
  testbutton2 = ttk.Button(window, text="Test2", command=lambda: exec_error(window))
  testbutton2.pack(fill=tk.X)
  window.mainloop()
