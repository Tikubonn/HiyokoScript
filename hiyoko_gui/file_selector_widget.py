
import tkinter 
import tkinter.messagebox
import subprocess
from .file_selector import FileSelector
from .language_holder import LanguageHolder 

class FileSelectorWidget (tkinter.Frame, LanguageHolder):

  def __init__ (self, defaultfile=None, master=None, *, language, filetypes=[], assave=False):
    tkinter.Frame.__init__(self, master)
    LanguageHolder.__init__(self, language=language)
    self._fileselector = FileSelector(defaultfile, filetypes=filetypes, assave=assave)
    self._setup_widgets()

  @property 
  def selectedfile (self):
    return self._fileselector.selectedfile

  def _select_file (self):
    self._fileselector.select_file()
    if self._fileselector.selectedfile:
      self._entry.delete(0, tkinter.END)
      self._entry.insert(0, str(self._fileselector.selectedfile.absolute()))

  def _open_file (self):
    if self._fileselector:
      subprocess.run([ "start", "explorer", str(self._fileselector.selectedfile.absolute()) ], shell=True, check=True)
    else:
      tkinter.messagebox.showwarning(
        self.translate("warning_open_unspecified_file"),
        self.translate("warning_open_unspecified_file_desc")
      )

  def _setup_widgets (self):
    entry = tkinter.Entry(self, width=30)
    if self._fileselector.selectedfile:
      entry.delete(0, tkinter.END)
      entry.insert(0, str(self._fileselector.selectedfile.absolute()))
    entry.grid(row=0, column=0)
    self._entry = entry
    selectbutton = tkinter.Button(self, text=self.translate("button_file_select"), command=self._select_file)
    selectbutton.grid(row=0, column=1)
    self._selectbutton = selectbutton
    if not self._fileselector.assave:
      openbutton = tkinter.Button(self, text=self.translate("button_file_open"), command=self._open_file)
      openbutton.grid(row=0, column=2)
      self._openbutton = openbutton
    else:
      self._openbutton = None 
