
from abc import ABC

class ConfigHolder (ABC):

  def __init__ (self, *, config):
    self._config = config

  @property
  def config (self):
    return self._config

  def get_config (self, keys, value=None, *, shouldexists=False):
    conf = self._config
    for key in keys[:-1]:
      conf = conf.get(key, {})
    if shouldexists:
      if keys[-1] in conf:
        return conf[keys[-1]]
      else:
        raise KeyError("Could not find entry {!r} in config.".format(keys)) #error
    else:
      return conf.get(keys[-1], value)
