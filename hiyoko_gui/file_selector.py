
import subprocess
import tkinter as tk 
import tkinter.ttk as ttk 
import tkinter.filedialog
import tkinterdnd2 as tkdnd
from pathlib import Path 
from .config_holder import ConfigHolder 
from .language_holder import LanguageHolder 

class FileSelector:

  def __init__ (self, file=None, *, filetypes=[]):
    self._selectedfile = file 
    self._filetypes = list(filetypes)
    self._onupdates = list()

  def add_onupdate (self, func):
    self._onupdates.append(func)

  def call_onupdates (self):
    for onupdate in self._onupdates:
      onupdate()

  @property
  def selectedfile (self):
    return self._selectedfile and Path(self._selectedfile)

  @selectedfile.setter
  def selectedfile (self, file):
    self._selectedfile = file 
    self.call_onupdates()

  @property
  def filetypes (self):
    return self._filetypes

  def select_file (self, *, assave=False):
    initialfile = self.selectedfile and Path(self.selectedfile)
    initialdir = self.selectedfile and Path(self.selectedfile).parent 
    if assave:
      selectedfile = tk.filedialog.asksaveasfilename(
        initialfile=initialfile,
        initialdir=initialdir,
        filetypes=self.filetypes,
      )
    else:
      selectedfile = tk.filedialog.askopenfilename(
        initialfile=initialfile,
        initialdir=initialdir,
        filetypes=self.filetypes,
      )
    if selectedfile:
      self.selectedfile = selectedfile
    return bool(selectedfile)

  def clear (self):
    self._selectedfile = None 
    self.call_onupdates()

class FileSelectorWidget (ttk.Frame, ConfigHolder, LanguageHolder):

  def __init__ (self, fileselector, master=None, *, config, language, assave=False):
    ttk.Frame.__init__(self, master)
    ConfigHolder.__init__(self, config=config)
    LanguageHolder.__init__(self, language=language)
    fileselector.add_onupdate(self._onupdate)
    self.fileselector = fileselector
    self._assave = assave
    self._input = None 
    self.setup_widgets()

  def _onupdate (self):
    if self.fileselector.selectedfile:
      filestr = str(self.fileselector.selectedfile.absolute())
    else:
      filestr = ""
    self._input.config(state=tk.NORMAL)
    self._input.delete(0, tk.END)
    self._input.insert(0, filestr)
    self._input.config(state=tk.DISABLED)

  def select (self):
    if self.fileselector.select_file(assave=self._assave):
      self._input.config(state=tk.NORMAL)
      self._input.delete(0, tk.END)
      self._input.insert(0, str(self.fileselector.selectedfile.absolute()))
      self._input.config(state=tk.DISABLED)

  def open (self):
    if self.fileselector.selectedfile:
      if Path(self.fileselector.selectedfile).exists():
        command = ["start", "explorer", str(self.fileselector.selectedfile)]
        subprocess.run(command, shell=True)
      else:
        tk.messagebox.showwarning(
          self.translate("warning_open_unexist_file"),
          self.translate("warning_open_unexist_file_desc"),
        )
    else:
      tk.messagebox.showwarning(
        self.translate("warning_open_unspecified_file"),
        self.translate("warning_open_unspecified_file_desc"),
      )

  def _ondnd (self, event):
    file = Path(event.data).absolute()
    self.fileselector.selectedfile = file 
    self._input.config(state=tk.NORMAL)
    self._input.delete(0, tk.END)
    self._input.insert(0, str(file))
    self._input.config(state=tk.DISABLED)

  def setup_widgets (self):
    entry = ttk.Entry(self)
    if self.fileselector.selectedfile:
      entry.delete(0, tk.END)
      entry.insert(0, str(self.fileselector.selectedfile.absolute()))
    entry.config(state=tk.DISABLED)
    entry.grid(row=0, column=0, sticky=tk.EW)
    entry.drop_target_register(tkdnd.DND_FILES)
    entry.dnd_bind("<<Drop>>", self._ondnd)
    selectbutton = ttk.Button(self, text=self.translate("button_file_select"), command=self.select)
    selectbutton.grid(row=0, column=1)
    openbutton = ttk.Button(self, text=self.translate("button_file_open"), command=self.open)
    if self._assave:
      openbutton.config(state=tk.DISABLED)
    openbutton.grid(row=0, column=2)
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=0)
    self.grid_columnconfigure(2, weight=0)
    self._input = entry
    self.selectbutton = selectbutton
