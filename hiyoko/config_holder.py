
from abc import ABC

class ConfigHolder (ABC):

  def __init__ (self, *, config):
    self._config = config

  @property
  def config (self):
    return self._config
