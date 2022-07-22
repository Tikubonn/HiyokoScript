
from hiyoko import ConfigHolder as CHolder

class ConfigHolder (CHolder):

  @property
  def hiyokoconfig (self): #avoid conflict to Tk.config.
    return CHolder.config.fget(self)

  def get_hiyokoconfig (self, keys, value=None, *, shouldexists=False):
    return CHolder.get_config(self, keys, value, shouldexists=shouldexists)
