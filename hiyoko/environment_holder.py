
from abc import ABC

class EnvironmentHolder (ABC):

  def __init__ (self, *, environment):
    self._environment = environment

  @property
  def environment (self):
    return self._environment
