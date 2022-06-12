
import tkinter
import tkinter.filedialog
from pathlib import Path 

class FileSelector:

  def __init__ (self, defaultfile=None, *, filetypes=[], assave=False):
    self._file = defaultfile
    self._filetypes = filetypes
    self._assave = assave

  @property
  def selectedfile (self):
    return self._file and Path(self._file) #tmp

  @property 
  def filetypes (self):
    return self._filetypes

  @property 
  def assave (self):
    return self._assave

  def select_file (self):
    initialfile = self._file
    initialdir = self._file and Path(self._file).parent 
    if self._assave:
      selectedfile = tkinter.filedialog.asksaveasfilename(
        initialfile=initialfile, 
        initialdir=initialdir, 
        filetypes=self._filetypes
      )
    else:
      selectedfile = tkinter.filedialog.askopenfilename(
        initialfile=initialfile, 
        initialdir=initialdir, 
        filetypes=self._filetypes
      )
    if selectedfile:
      self._file = selectedfile
    return bool(selectedfile) #if selected, selectedfile is not None.
