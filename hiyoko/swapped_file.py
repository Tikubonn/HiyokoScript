
import os 
import shutil
from pathlib import Path 
from tempfile import NamedTemporaryFile

class SwappedFile: #tmp

  def __init__ (self, path, mode, *args, **kwargs):
    self.file = NamedTemporaryFile(mode, *args, delete=False, **kwargs)
    self.destpath = path
    self.mode = mode 

  def __enter__ (self):
    self.file.__enter__()
    return self 

  def __exit__ (self, errortype, errorvalue, backtrace):
    result = self.file.__exit__(errortype, errorvalue, backtrace)
    if (errortype is None and 
        errorvalue is None and 
        backtrace is None):
      self.swap()
    else:
      os.remove(self.file.name)
    return result

  def __getattr__ (self, name):
    return getattr(self.file, name)

  def swap (self):
    destp = Path(self.destpath)
    os.makedirs(destp.parent, exist_ok=True)
    #os.rename(self.file.name, destp)
    shutil.move(self.file.name, destp)
