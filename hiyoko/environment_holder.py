
from abc import ABC

class EnvironmentHolder (ABC):

  def __init__ (self, *, environment):
    self._environment = environment

  @property
  def environment (self):
    return self._environment

  def get_environment (self, keys, value=None, *, shouldexists=False):
    env = self._environment
    for key in keys[:-1]:
      env = env.get(key, {})
    if shouldexists:
      if keys[-1] in env:
        return env[keys[-1]]
      else:
        raise KeyError("Could not find entry {!r} in environment.".format(keys)) #error
    else:
      return env.get(keys[-1], value)
