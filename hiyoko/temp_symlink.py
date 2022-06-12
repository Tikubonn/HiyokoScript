
import os 
import tempfile
from pathlib import Path 

class TempSymLink:

  def __init__ (self, path):
    p = Path(path)
    tempp = Path(tempfile.mktemp(suffix=p.suffix))
    #tempp.symlink_to(p.absolute())
    os.link(p, tempp)
    self._path = path
    self._temppath = tempp
    self._closed = False 

  @property
  def path (self):
    if not self._closed: 
      return self._path
    else:
      raise ValueError("{!r} is already closed.".format(self)) #error 

  @property
  def temppath (self):
    if not self._closed: 
      return self._temppath
    else:
      raise ValueError("{!r} is already closed.".format(self)) #error 

  def __enter__ (self):
    return self 

  def __exit__ (self, errortype, errorvalue, backtrace):
    self.close()

  def close (self):
    if not self._closed:
      self._temppath.unlink()
      self._closed = True 
    else:
      raise ValueError("{!r} is already closed.".format(self)) #error 
