
from abc import ABC

class ParentHolder (ABC):

  def __init__ (self, *, parent):
    self._parent = parent

  @property
  def parent (self):
    return self._parent
