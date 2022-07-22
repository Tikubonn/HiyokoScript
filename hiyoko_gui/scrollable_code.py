
import tkinter as tk 
import tkinter.ttk
from abc import abstractmethod
from .scrollable_text import ScrollableText

class ScrollableCode (ScrollableText):

  def __init__ (self, master=None):
    super().__init__(master)
    self._lastindex = "1.0"
    self.text.add_onupdate(self._onupdate)

  @property
  def lastindex (self):
    return self._lastindex

  @property
  def curindex (self):
    return self.text.index(tk.INSERT)

  @property
  def modrange (self):
    minindex = min(self.lastindex, self.curindex) #tmp
    maxindex = max(self.lastindex, self.curindex) #tmp
    startindex = self.text.index("{:s} -1 lines linestart".format(minindex))
    endindex = self.text.index("{:s} +1 lines lineend".format(maxindex))
    return startindex, endindex

  @abstractmethod
  def update_highlight (self, span):
    pass

  def _onupdate (self):
    self.update_highlight(self.modrange)
    self._lastindex = self.curindex
